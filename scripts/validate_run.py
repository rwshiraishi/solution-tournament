#!/usr/bin/env python3
"""Tournament-output validator for the solution-tournament skill.

The skill's BINDING machinery assumes "a reader holding this file" who
recomputes counts and spots absent artifacts. This script IS that
reader, deterministically, for the record's SHAPE and ARITHMETIC. It
cannot judge truth (the single-author caveat applies in full): a
transcript can pass this validator and still be wrong. What it closes
is the gap between "the file hopes someone checks" and "a command
checked".

Usage:
    python3 validate_run.py TRANSCRIPT_FILE [--mode lightweight|full]

Mode is auto-detected from the st:meta block when omitted. Strikes
found here count as degraded-execution strikes (SKILL.md, "Checklists,
ledgers, and degraded execution").

Exit codes: 0 pass, 1 strikes printed, 2 cannot parse/read.

Block formats are defined by templates/run-skeleton.md.
"""

import argparse
import pathlib
import re
import sys

TOTAL_TOLERANCE = 0.05
WEIGHT_TOLERANCE = 0.001
FULL_CHECKLIST_DENOMS = (9, 4, 6, 6, 7, 9, 7)
LIGHTWEIGHT_DENOM = 15
NO_EXEC_HASH_LINE = "hash unavailable — no execution tool"

# Threshold NAMES each mode's sweep line must contain (subsets of the
# authoritative enumerations; "each active counter" is one entry).
LIGHTWEIGHT_SWEEP_NAMES = (
    "decisive margin", "5.0 floor", "0.3 tiebreak band",
    "majority-OPINION weight stop", "recompute discrepancy",
    "pre-commitment width rule", "cap-magnitude-vs-margin", "each active counter",
)
FULL_SWEEP_NAMES = LIGHTWEIGHT_SWEEP_NAMES + (
    "plateau delta", "DISPUTED spread", "weight×spread", "NOISE",
    "1.5 ceiling", "spike size ceiling",
)

LIGHTWEIGHT_COUNTERS = ("reopen", "re-entry", "re-scores", "post-freeze mutation", "scoring rounds")
FULL_COUNTERS = LIGHTWEIGHT_COUNTERS + (
    "completeness", "fact requests", "read-only verifications", "red-team", "spike",
)

DISCLOSURE_BY_SHAPE = {
    "attended-full": None,  # baseline: no line required
    "attended-lightweight": "self-administered EXCEPT the user's checks",
    "autonomous-lightweight": "every safeguard in this run was self-administered",
    "preauthorized-autonomous-full": "no user check; subagent independence only",
}


def block(text: str, name: str) -> str:
    m = re.search(rf"```st:{name}\n(.*?)```", text, re.S)
    return m.group(1) if m else ""


def check_meta(text: str, strikes: list) -> tuple:
    meta = block(text, "meta")
    if not meta:
        strikes.append("st:meta block absent")
        return "", ""
    mode = (re.search(r"mode:\s*(\S+)", meta) or [None, ""])[1]
    shape = (re.search(r"run_shape:\s*(\S+)", meta) or [None, ""])[1]
    if mode not in ("lightweight", "full"):
        strikes.append(f"st:meta mode invalid: {mode!r}")
    if shape not in DISCLOSURE_BY_SHAPE:
        strikes.append(f"st:meta run_shape invalid: {shape!r} (expected one of {sorted(DISCLOSURE_BY_SHAPE)})")
    return mode, shape


def check_weights(text: str, strikes: list) -> dict:
    raw = block(text, "weights")
    if not raw:
        strikes.append("st:weights block absent")
        return {}
    weights = {}
    for line in raw.strip().splitlines():
        m = re.match(r"([\w][\w /-]*?)\s+([\d.]+)$", line.strip())
        if m:
            weights[m.group(1)] = float(m.group(2))
    if weights and abs(sum(weights.values()) - 1.0) > WEIGHT_TOLERANCE:
        strikes.append(f"weights sum to {sum(weights.values()):.3f}, not 1.0")
    return weights


def check_matrix(text: str, weights: dict, strikes: list) -> None:
    raw = block(text, "matrix")
    if not raw:
        strikes.append("st:matrix block absent")
        return
    for line in raw.strip().splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            strikes.append(f"matrix row malformed: {line!r}")
            continue
        name, scores_raw, total_raw = parts
        scores = dict(re.findall(r"([\w/-]+)=([\d.]+)", scores_raw))
        m = re.search(r"total=([\d.]+)", total_raw)
        if not m:
            strikes.append(f"matrix row {name}: no total")
            continue
        stated = float(m.group(1))
        missing = [d for d in weights if d not in scores]
        if missing:
            strikes.append(f"matrix row {name}: missing dimensions {missing}")
            continue
        recomputed = sum(weights[d] * float(scores[d]) for d in weights)
        if abs(recomputed - stated) > TOTAL_TOLERANCE:
            strikes.append(
                f"matrix row {name}: stated total {stated}, recomputed {recomputed:.3f} "
                f"(discrepancy > {TOTAL_TOLERANCE})"
            )


def check_pack_hash(text: str, strikes: list) -> None:
    if re.search(r"pack-v\d+ sha256 [0-9a-f]{64}", text):
        return
    if NO_EXEC_HASH_LINE in text:
        return
    strikes.append("no pack hash line (pack-vN sha256 <hex64>) and no no-execution-tool fallback line")


def check_sweep(text: str, mode: str, strikes: list) -> None:
    m = re.search(r"near-miss sweep:\s*(\d+) of (\d+) thresholds evaluated", text)
    if not m:
        strikes.append("near-miss sweep line absent or malformed")
        return
    if m.group(1) != m.group(2):
        strikes.append(f"near-miss sweep evaluated {m.group(1)} of {m.group(2)} — incomplete")
    names = LIGHTWEIGHT_SWEEP_NAMES if mode == "lightweight" else FULL_SWEEP_NAMES
    line = text[m.start():text.find("\n", m.start())]
    for name in names:
        if name not in line:
            strikes.append(f"near-miss sweep line missing threshold name: {name}")


def check_counters(text: str, mode: str, strikes: list) -> None:
    m = re.search(r"^counters:.*$", text, re.M)
    if not m:
        strikes.append("counters ledger final line absent")
        return
    names = LIGHTWEIGHT_COUNTERS if mode == "lightweight" else FULL_COUNTERS
    line = m.group(0)
    if mode == "lightweight" and "n/a (no subagents)" not in line:
        strikes.append("counters line missing the subagent-only 'n/a (no subagents)' entry")
    for name in names:
        if name not in line:
            strikes.append(f"counters line missing counter: {name}")


def check_checklist(text: str, mode: str, strikes: list) -> None:
    m = re.search(r"^checklist:(.+)$", text, re.M)
    if not m:
        strikes.append("checklist line absent")
        return
    pairs = re.findall(r"(\d+) of (\d+)", m.group(1))
    if mode == "lightweight":
        if len(pairs) != 1 or int(pairs[0][1]) != LIGHTWEIGHT_DENOM:
            strikes.append(f"lightweight checklist must read 'N of {LIGHTWEIGHT_DENOM}', got {pairs}")
            return
        if int(pairs[0][0]) < LIGHTWEIGHT_DENOM:
            strikes.append(f"checklist below denominator: {pairs[0][0]} of {LIGHTWEIGHT_DENOM}")
    else:
        denoms = tuple(int(b) for _, b in pairs)
        if denoms != FULL_CHECKLIST_DENOMS:
            strikes.append(f"full checklist denominators {denoms} != {FULL_CHECKLIST_DENOMS}")
            return
        for got, want in pairs:
            if int(got) < int(want):
                strikes.append(f"checklist phase below denominator: {got} of {want}")


def check_gate_order(text: str, mode: str, strikes: list) -> None:
    if mode != "full":
        return
    m = re.search(r"gate-order diff:\s*(\d+) ticks / (\d+) artifact IDs matched", text)
    if not m:
        strikes.append("gate-order diff line absent (full mode)")
        return
    if m.group(1) != m.group(2):
        strikes.append(f"gate-order diff mismatch: {m.group(1)} ticks vs {m.group(2)} artifact IDs")


def check_disclosure(text: str, shape: str, strikes: list) -> None:
    expected = DISCLOSURE_BY_SHAPE.get(shape)
    if expected and expected not in text:
        strikes.append(f"disclosure line for run shape {shape} absent: expected {expected!r}")


def validate(text: str, mode_override: str = "") -> list:
    strikes: list = []
    mode, shape = check_meta(text, strikes)
    mode = mode_override or mode
    if mode not in ("lightweight", "full"):
        return strikes or ["mode undetermined"]
    weights = check_weights(text, strikes)
    if weights:
        check_matrix(text, weights, strikes)
    check_pack_hash(text, strikes)
    check_sweep(text, mode, strikes)
    check_counters(text, mode, strikes)
    check_checklist(text, mode, strikes)
    check_gate_order(text, mode, strikes)
    if shape:
        check_disclosure(text, shape, strikes)
    return strikes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript", type=pathlib.Path)
    parser.add_argument("--mode", choices=("lightweight", "full"), default="")
    args = parser.parse_args()
    try:
        text = args.transcript.read_text(encoding="utf-8")
    except OSError as e:
        print(f"validate_run: cannot read transcript: {e}", file=sys.stderr)
        sys.exit(2)
    strikes = validate(text, args.mode)
    if strikes:
        for s in strikes:
            print(f"STRIKE: {s}")
        print(f"validate_run: {len(strikes)} strike(s) — shape/arithmetic only; truth not certified")
        sys.exit(1)
    print("validate_run: PASS — shape/arithmetic only; truth not certified (SAC)")


if __name__ == "__main__":
    main()
