#!/usr/bin/env python3
"""Validate the generic machine-readable HVAC protocol contract. Offline only.

Target-specific applicability lives in contracts/hvac_target_profile.json.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

ALLOWED_EVIDENCE = {"OBSERVED_SINGLE_FIELD", "OBSERVED_COMPOSITE", "NOT_OBSERVED"}
ALLOWED_PHYSICAL = {"PHYSICAL_PENDING", "PHYSICAL_PROVEN"}


def parse_hex(s: str) -> bytes:
    return bytes.fromhex(s.replace("0x", ""))


def checksum(body_without_checksum: bytes) -> int:
    if len(body_without_checksum) < 4 or body_without_checksum[:2] != b"\x5a\xa5":
        raise ValueError("invalid Hiworld body")
    return (sum(body_without_checksum[2:]) - 1) & 0xFF


def valid_frame(frame: bytes) -> bool:
    return len(frame) >= 5 and frame[:2] == b"\x5a\xa5" and len(frame) == frame[2] + 5 and checksum(frame[:-1]) == frame[-1]


def build_frame(cmd: int, payload: bytes) -> bytes:
    body = bytes([0x5A, 0xA5, len(payload), cmd]) + payload
    return body + bytes([checksum(body)])


def hvac_tx(subcommand: int, value: int) -> bytes:
    return build_frame(0x3B, bytes([subcommand, value]))


def decode31(frame: bytes) -> dict:
    if not valid_frame(frame) or frame[3] != 0x31 or frame[2] != 12:
        raise ValueError("need valid 0x31 length-12 frame")
    p = frame[4:-1]
    return {
        "front_power": bool(p[0] & 0x40), "max_ac": bool(p[0] & 0x20), "rear_power": bool(p[0] & 0x10),
        "auto": bool(p[0] & 0x08), "sync": bool(p[0] & 0x04), "ac": bool(p[0] & 0x01),
        "recirculation": bool(p[1] & 0x10), "auto_recirculation": bool(p[1] & 0x08),
        "rear_defrost": bool(p[2] & 0x20), "front_defrost": bool(p[2] & 0x10),
        "wind_intensity": p[3] & 0x03, "airflow_raw": p[4] & 0x0F, "fan": p[5],
        "left_temperature_raw": p[6], "right_temperature_raw": p[7], "outside_temperature_raw": p[11],
    }


OBSERVED_SEQUENCE = [
    "5A A5 0C 31 45 10 00 01 06 04 FE FE 00 00 00 82 1A",
    "5A A5 0C 31 45 10 10 01 0B 07 FF FE 00 00 00 82 33",
    "5A A5 0C 31 45 10 30 01 0B 07 FF FE 00 00 00 82 53",
    "5A A5 0C 31 45 00 20 01 06 04 FE FE 00 00 00 82 2A",
    "5A A5 0C 31 45 00 00 01 06 04 FE FE 00 00 00 82 0A",
    "5A A5 0C 31 45 10 00 01 06 04 FE FE 00 00 00 82 1A",
    "5A A5 0C 31 04 10 00 01 06 00 FE FE 00 00 00 82 D5",
    "5A A5 0C 31 45 10 00 01 06 04 FE FE 00 00 00 82 1A",
]


def logical_diff(a: dict, b: dict) -> set[str]:
    keys = {"front_power","max_ac","rear_power","auto","sync","ac","recirculation","auto_recirculation","rear_defrost","front_defrost","wind_intensity","airflow_raw","fan","left_temperature_raw","right_temperature_raw"}
    return {k for k in keys if a[k] != b[k]}


def validate_contract(data: dict) -> dict:
    errors = []
    warnings = []
    functions = data.get("functions", [])
    if data.get("status") != "DRAFT_PRE_F4":
        errors.append("status must remain DRAFT_PRE_F4 until F4 promotion")
    if len(functions) != 18:
        errors.append(f"expected 18 generic protocol operations, got {len(functions)}")
    ids = [f.get("id") for f in functions]
    if len(ids) != len(set(ids)):
        errors.append("function IDs must be unique")
    rx_layout = data.get("rx_layout", {})
    for f in functions:
        if f.get("runtime_evidence") not in ALLOWED_EVIDENCE:
            errors.append(f"{f.get('id')}: invalid runtime_evidence")
        if f.get("physical_link") not in ALLOWED_PHYSICAL:
            errors.append(f"{f.get('id')}: invalid physical_link")
        if f.get("rx") not in rx_layout:
            errors.append(f"{f.get('id')}: rx mapping {f.get('rx')} missing")
        for name, frame_hex in f.get("static_examples", {}).items():
            try:
                frame = parse_hex(frame_hex)
            except ValueError:
                errors.append(f"{f.get('id')}.{name}: bad hex")
                continue
            if not valid_frame(frame):
                errors.append(f"{f.get('id')}.{name}: invalid framing/checksum")
            elif frame[3] != 0x3B or frame[2] != 2:
                errors.append(f"{f.get('id')}.{name}: not 0x3B/2")
            elif hvac_tx(frame[4], frame[5]) != frame:
                errors.append(f"{f.get('id')}.{name}: generator mismatch")

    states = [decode31(parse_hex(x)) for x in OBSERVED_SEQUENCE]
    if any(not valid_frame(parse_hex(x)) for x in OBSERVED_SEQUENCE):
        errors.append("an observed 0x31 reference frame has invalid checksum")
    if logical_diff(states[4], states[5]) != {"recirculation"}:
        errors.append("recirculation ON is no longer a single-field observed transition")

    # Historical generic contract still contains a common_physical_link field.
    # It is no longer authoritative for target applicability after the owner
    # confirmed the vehicle has no rear defroster. The target profile is.
    if data.get("common_physical_link", {}).get("selected_action") == "rear_defrost_on":
        warnings.append("legacy generic contract contains rear_defrost gate; target gate is authoritative in contracts/hvac_target_profile.json")

    observed_single = sum(f["runtime_evidence"] == "OBSERVED_SINGLE_FIELD" for f in functions)
    observed_composite = sum(f["runtime_evidence"] == "OBSERVED_COMPOSITE" for f in functions)
    not_observed = sum(f["runtime_evidence"] == "NOT_OBSERVED" for f in functions)
    static_examples = sum(bool(f.get("static_examples")) for f in functions)
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "generic_protocol_operations": len(functions),
            "with_static_examples": static_examples,
            "observed_single_field": observed_single,
            "observed_composite": observed_composite,
            "not_observed_as_control_transition": not_observed,
            "target_profile": "contracts/hvac_target_profile.json"
        }
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("contract", nargs="?", default="contracts/hvac_behavior_contract.json")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    data = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    result = validate_contract(data)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("HVAC GENERIC CONTRACT:", "PASS" if result["ok"] else "FAIL")
        for k, v in result["summary"].items():
            print(f"- {k}: {v}")
        for w in result["warnings"]:
            print("WARNING:", w)
        for e in result["errors"]:
            print("ERROR:", e)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
