#!/usr/bin/env python3
"""Passive analyzer for Hiworld/Jancar candata logs.

Parses one or more lines such as:
  19:48:18.129 TX:[5a a5 03 6a 05 01 31 a3 ]

The parser handles multiple concatenated 5A A5 frames inside one bracketed log
entry. It never transmits data and has no device I/O.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

LINE_RE = re.compile(
    r"(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2})\.(?P<ms>\d{3})\s+"
    r"(?P<direction>RX|TX):\[(?P<hex>.*?)\]"
)

KNOWN_TX = {
    0xFF: "ACK",
    0xCB: "TIME_SET",
    0x6A: "REPORT_REQUEST",
    0xA1: "MEDIA_DATA",
    0xA4: "MEDIA_CD_CDC",
    0x3B: "HVAC_CONTROL_STATIC_EXPECTATION",
}


@dataclass(frozen=True)
class Frame:
    time_ms: int
    timestamp: str
    direction: str
    raw: bytes
    line_no: int

    @property
    def cmd(self) -> int:
        return self.raw[3]

    @property
    def payload(self) -> bytes:
        return self.raw[4:-1]

    @property
    def checksum(self) -> int:
        return self.raw[-1]

    @property
    def checksum_expected(self) -> int:
        return (sum(self.raw[2:-1]) - 1) & 0xFF

    @property
    def checksum_ok(self) -> bool:
        return self.checksum == self.checksum_expected


def time_to_ms(h: int, m: int, s: int, ms: int) -> int:
    return (((h * 60) + m) * 60 + s) * 1000 + ms


def split_hiword_frames(data: bytes) -> list[bytes]:
    """Recover complete 5A A5 frames from one bracketed log entry."""
    out: list[bytes] = []
    i = 0
    while i + 4 < len(data):
        if data[i:i + 2] == b"\x5a\xa5":
            total = data[i + 2] + 5
            if total >= 5 and i + total <= len(data):
                out.append(data[i:i + total])
                i += total
                continue
        i += 1
    return out


def parse_lines(lines: Iterable[str]) -> list[Frame]:
    frames: list[Frame] = []
    for line_no, line in enumerate(lines, 1):
        match = LINE_RE.search(line)
        if not match:
            continue
        try:
            values = bytes(int(token, 16) for token in match.group("hex").split())
        except ValueError:
            continue
        t_ms = time_to_ms(
            int(match.group("h")), int(match.group("m")),
            int(match.group("s")), int(match.group("ms")),
        )
        ts = f"{match.group('h')}:{match.group('m')}:{match.group('s')}.{match.group('ms')}"
        for raw in split_hiword_frames(values):
            frames.append(Frame(t_ms, ts, match.group("direction"), raw, line_no))
    return frames


def parse_file(path: Path) -> list[Frame]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return parse_lines(handle)


def dedupe_adjacent(frames: Iterable[Frame], window_ms: int = 10) -> list[Frame]:
    """Collapse near-simultaneous duplicate captures even if an ACK interleaves."""
    out: list[Frame] = []
    last_seen: dict[tuple[str, bytes], int] = {}
    for frame in frames:
        key = (frame.direction, frame.raw)
        previous = last_seen.get(key)
        if previous is not None and abs(frame.time_ms - previous) <= window_ms:
            last_seen[key] = frame.time_ms
            continue
        out.append(frame)
        last_seen[key] = frame.time_ms
    return out


def request_target(frame: Frame) -> Optional[int]:
    if frame.direction != "TX" or frame.cmd != 0x6A:
        return None
    payload = frame.payload
    # Observed PSA/Hiworld report request: 05 01 <target_cmd>
    if len(payload) >= 3 and payload[0] == 0x05 and payload[1] == 0x01:
        return payload[2]
    return None


def classify_rx_provenance(
    logical_frames: list[Frame], request_window_ms: int = 500
) -> dict[int, str]:
    """Classify absence/presence of the known 0x6A polling mechanism.

    RX_NAO_SOLICITADO does not identify the physical producer. It only means no
    compatible known request exists inside the configured preceding window.
    """
    classifications: dict[int, str] = {}
    requests: list[tuple[int, int]] = []
    for idx, frame in enumerate(logical_frames):
        target = request_target(frame)
        if target is not None:
            requests.append((frame.time_ms, target))
            continue
        if frame.direction != "RX" or frame.cmd in (0xFF, 0xFE):
            continue
        compatible = [
            t for t, req_target in requests
            if req_target == frame.cmd and 0 <= frame.time_ms - t <= request_window_ms
        ]
        classifications[idx] = "RESPOSTA_SOLICITADA" if compatible else "RX_NAO_SOLICITADO"
    return classifications


def decode_hvac_31(frame: Frame) -> dict[str, object]:
    if frame.cmd != 0x31 or len(frame.payload) < 12:
        return {}
    d = frame.payload
    b0, b1, b2, b3, b4, fan = d[0], d[1], d[2], d[3], d[4], d[5]
    return {
        "power": bool((b0 >> 6) & 1),
        "max_ac": bool((b0 >> 5) & 1),
        "rear_hvac": bool((b0 >> 4) & 1),
        "auto_light_1": bool((b0 >> 3) & 1),
        "sync": bool((b0 >> 2) & 1),
        "ac": bool(b0 & 1),
        "recirculation": bool((b1 >> 4) & 1),
        "auto_recirculation": bool((b1 >> 3) & 1),
        "rear_defrost": bool((b2 >> 5) & 1),
        "front_defrost": bool((b2 >> 4) & 1),
        "wind_intensity": b3 & 0x03,
        "airflow_raw": b4 & 0x0F,
        "fan": fan,
        "left_temp_raw": d[6],
        "right_temp_raw": d[7],
        "outside_temp_c": (d[11] / 2.0) - 40.0,
    }


def summarize(frames: list[Frame], dedup_ms: int, request_window_ms: int) -> dict[str, object]:
    logical = dedupe_adjacent(frames, dedup_ms)
    provenance = classify_rx_provenance(logical, request_window_ms)
    tx = Counter(f.cmd for f in frames if f.direction == "TX")
    rx = Counter(f.cmd for f in frames if f.direction == "RX")
    hvac_events = []
    for idx, frame in enumerate(logical):
        if frame.direction == "RX" and frame.cmd == 0x31:
            hvac_events.append({
                "timestamp": frame.timestamp,
                "payload_hex": frame.payload.hex(" "),
                "provenance": provenance.get(idx, "INDETERMINADO"),
                "decoded": decode_hvac_31(frame),
            })
    one_a_events = []
    for frame in logical:
        if frame.direction == "RX" and frame.cmd == 0x1A and len(frame.payload) >= 11:
            value = (frame.payload[9] << 8) | frame.payload[10]
            one_a_events.append({"timestamp": frame.timestamp, "data_9_10_be": value})
    return {
        "frames_total": len(frames),
        "checksum_valid": sum(f.checksum_ok for f in frames),
        "checksum_invalid": sum(not f.checksum_ok for f in frames),
        "logical_frames_after_adjacent_dedup": len(logical),
        "tx_counts": {f"0x{k:02X}": v for k, v in sorted(tx.items())},
        "tx_semantics": {f"0x{k:02X}": KNOWN_TX.get(k, "UNCLASSIFIED") for k in sorted(tx)},
        "rx_counts": {f"0x{k:02X}": v for k, v in sorted(rx.items())},
        "hvac_0x31_logical_events": hvac_events,
        "hvac_0x31_requested": sum(e["provenance"] == "RESPOSTA_SOLICITADA" for e in hvac_events),
        "hvac_0x31_unsolicited": sum(e["provenance"] == "RX_NAO_SOLICITADO" for e in hvac_events),
        "tx_0x3B": tx.get(0x3B, 0),
        "rx_0x1A_candidate_field": one_a_events,
    }


def print_text(summary: dict[str, object]) -> None:
    print(f"Frames reconstruídos: {summary['frames_total']}")
    print(f"Checksums válidos: {summary['checksum_valid']} | inválidos: {summary['checksum_invalid']}")
    print("TX por comando:")
    tx_counts = summary["tx_counts"]
    tx_semantics = summary["tx_semantics"]
    for cmd, count in tx_counts.items():
        print(f"  {cmd}: {count:>4}  {tx_semantics[cmd]}")
    print(f"TX 0x3B observado: {summary['tx_0x3B']}")
    print(
        "RX 0x31 lógicos: "
        f"{len(summary['hvac_0x31_logical_events'])} | "
        f"solicitados={summary['hvac_0x31_requested']} | "
        f"não solicitados={summary['hvac_0x31_unsolicited']}"
    )
    for event in summary["hvac_0x31_logical_events"]:
        d = event["decoded"]
        print(
            f"  {event['timestamp']} {event['provenance']}: "
            f"power={int(d.get('power', False))} ac={int(d.get('ac', False))} "
            f"front_defrost={int(d.get('front_defrost', False))} "
            f"rear_defrost={int(d.get('rear_defrost', False))} "
            f"fan={d.get('fan')} payload={event['payload_hex']}"
        )


def self_test() -> None:
    sample = [
        "19:00:00.000 TX:[5a a5 03 6a 05 01 31 a3 ]\n",
        "19:00:00.064 RX:[5a a5 0c 31 45 10 00 01 06 04 fe fe 00 00 00 82 1a ]\n",
        "19:00:00.065 RX:[5a a5 0c 31 45 10 00 01 06 04 fe fe 00 00 00 82 1a ]\n",
        "19:00:01.000 RX:[5a a5 0c 31 04 10 00 01 06 00 fe fe 00 00 00 82 d5 ]\n",
        # Two valid frames concatenated in one logger bracket, as observed in real capture.
        "19:00:02.000 RX:[5a a5 01 ff a4 a3 5a a5 01 ff 31 30 ]\n",
    ]
    frames = parse_lines(sample)
    assert len(frames) == 6, len(frames)
    result = summarize(frames, dedup_ms=10, request_window_ms=500)
    assert result["checksum_invalid"] == 0, result
    assert len(result["hvac_0x31_logical_events"]) == 2, result
    assert result["hvac_0x31_requested"] == 1, result
    assert result["hvac_0x31_unsolicited"] == 1, result
    assert result["tx_0x3B"] == 0, result
    print("SELF-TEST PASS")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help="candata_*.log")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--dedup-ms", type=int, default=10)
    parser.add_argument("--request-window-ms", type=int, default=500)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        if not args.files:
            return
    if not args.files:
        parser.error("provide at least one candata log or use --self-test")

    all_frames: list[Frame] = []
    for file_path in args.files:
        all_frames.extend(parse_file(file_path))
    result = summarize(all_frames, args.dedup_ms, args.request_window_ms)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
