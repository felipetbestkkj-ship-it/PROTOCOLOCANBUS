#!/usr/bin/env python3
"""Validate target-specific HVAC capability/profile facts. Offline only."""
from __future__ import annotations
import argparse, json
from pathlib import Path


def checksum(body_without_checksum: bytes) -> int:
    if len(body_without_checksum) < 4 or body_without_checksum[:2] != b"\x5a\xa5":
        raise ValueError("invalid Hiworld body")
    return (sum(body_without_checksum[2:]) - 1) & 0xFF


def valid_frame(frame: bytes) -> bool:
    return len(frame) >= 5 and frame[:2] == b"\x5a\xa5" and len(frame) == frame[2] + 5 and checksum(frame[:-1]) == frame[-1]


def validate_profile(data: dict) -> dict:
    errors = []
    owner = data.get("owner_confirmed", {})
    if owner.get("front_defrost") is not True:
        errors.append("front_defrost must be confirmed present on target")
    if owner.get("rear_defrost") is not False:
        errors.append("rear_defrost must be confirmed absent on target")

    gate = data.get("f3_one_shot_gate", {})
    if gate.get("action") != "recirculation_on":
        errors.append("one-shot gate must be recirculation_on")
    expected = bytes.fromhex("5A A5 02 3B 07 00 43")
    try:
        actual = bytes.fromhex(gate.get("predicted_tx", ""))
    except ValueError:
        actual = b""
    if actual != expected or not valid_frame(actual):
        errors.append("recirculation one-shot TX drifted or is invalid")
    if gate.get("predicted_rx_change") != "0x31 payload[1] bit4: 0 -> 1":
        errors.append("recirculation RX expectation drifted")

    generic = data.get("protocol_capabilities_not_target_features", [])
    rear = [x for x in generic if x.get("name") == "rear_defrost"]
    if len(rear) != 1 or rear[0].get("target_status") != "NOT_PRESENT_ON_TARGET":
        errors.append("generic rear_defrost capability must be marked NOT_PRESENT_ON_TARGET")

    return {"ok": not errors, "errors": errors, "gate": gate.get("action")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", nargs="?", default="contracts/hvac_target_profile.json")
    args = ap.parse_args()
    data = json.loads(Path(args.profile).read_text(encoding="utf-8"))
    result = validate_profile(data)
    print("HVAC TARGET PROFILE:", "PASS" if result["ok"] else "FAIL")
    print("- gate:", result["gate"])
    for err in result["errors"]:
        print("ERROR:", err)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
