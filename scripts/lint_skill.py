#!/usr/bin/env python3
"""Consistency linter for the solution-tournament skill files.

Converts the manual wiring audits (2026-08-13) into a repeatable gate.
Checks cross-file pointers, checklist denominators, arithmetic claims,
size claims, and secret hygiene. Run before every commit that touches
the skill:

    python3 scripts/lint_skill.py [--root SKILL_DIR] [--readme README_PATH]

Exit codes: 0 clean, 1 findings printed, 2 cannot run (missing files).
"""

import argparse
import pathlib
import re
import sys

MODE_FILES = ("references/lightweight-mode.md", "references/full-mode.md")
TEMPLATE_FILES = ("templates/scorer.md", "templates/skeptic.md", "templates/red-team.md")
FULL_TABLE_TOTAL = 48
LIGHTWEIGHT_BOXES = 15
CALL_CEILING = 18
SIZE_TOLERANCE = 0.15
LINE_CLAIM_TOLERANCE = 0.25
SECRET_PATTERN = re.compile(
    r"sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{20,}"
)
# Thresholds that exist only in full mode and must not appear in
# lightweight's box-9 enumeration as printable entries.
FULL_ONLY_THRESHOLDS = ("NOISE", "1.5 ceiling", "plateau delta", "DISPUTED spread", "weight×spread")


def strip_nested_parens(text: str) -> str:
    out, depth = [], 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return "".join(out)


def check_files_exist(root: pathlib.Path, findings: list[str]) -> None:
    for rel in ("SKILL.md", *MODE_FILES, *TEMPLATE_FILES, "scripts/cross_model_score.py"):
        if not (root / rel).is_file():
            findings.append(f"missing file: {rel}")


def check_mentioned_paths(root: pathlib.Path, findings: list[str]) -> None:
    for md in ("SKILL.md", *MODE_FILES):
        text = (root / md).read_text(encoding="utf-8")
        for rel in re.findall(r"(?:references|templates|scripts)/[A-Za-z0-9_-]+\.(?:md|py)", text):
            if not (root / rel).is_file():
                findings.append(f"{md} mentions {rel} which does not exist")


def check_mode_read_timing(root: pathlib.Path, findings: list[str]) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    for rel in MODE_FILES:
        name = pathlib.Path(rel).name
        if f"`references/{name}` — read it BEFORE Phase 0" not in skill:
            findings.append(f"SKILL.md no longer mandates reading {name} before Phase 0")
        header = (root / rel).read_text(encoding="utf-8")[:600]
        if "before Phase 0" not in header:
            findings.append(f"{rel} header timing disagrees with SKILL.md (must say before Phase 0)")


def check_full_table(root: pathlib.Path, findings: list[str]) -> None:
    text = (root / "references/full-mode.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (0|1|1\.5|2|3|4|5) \| (\d+) \|", text, re.M)
    if not rows:
        findings.append("full-mode.md checklist table not found")
        return
    totals = {phase: int(n) for phase, n in rows}
    if sum(totals.values()) != FULL_TABLE_TOTAL:
        findings.append(f"checklist table sums to {sum(totals.values())}, expected {FULL_TABLE_TOTAL}")
    for m in re.finditer(r"- \*\*Exit Phase ([\d.]+)\*\*: (.+?)(?=\n- \*\*Exit|\n\n|\n\|)", text, re.S):
        phase, body = m.group(1), m.group(2)
        count = strip_nested_parens(body).count("·") + 1
        if phase in totals and count != totals[phase]:
            findings.append(
                f"Exit Phase {phase} lists {count} boxes, table says {totals[phase]}"
            )


def check_lightweight_boxes(root: pathlib.Path, findings: list[str]) -> None:
    text = (root / "references/lightweight-mode.md").read_text(encoding="utf-8")
    try:
        section = text.split("## Consolidated checklist")[1].split("## Interaction budget")[0]
    except IndexError:
        findings.append("lightweight-mode.md consolidated checklist section not found")
        return
    boxes = re.findall(r"^(\d+a?)\. ", section, re.M)
    if len(boxes) != LIGHTWEIGHT_BOXES:
        findings.append(f"lightweight inventory has {len(boxes)} boxes, expected {LIGHTWEIGHT_BOXES}")
    for name in FULL_ONLY_THRESHOLDS:
        # They may be mentioned only inside the "cannot arise" exclusion sentence.
        for line in section.splitlines():
            if name in line and "NOT printed" not in line and "cannot arise" not in line:
                findings.append(f"full-only threshold '{name}' appears as printable in lightweight box list")


def check_call_sum(root: pathlib.Path, findings: list[str]) -> None:
    text = (root / "references/full-mode.md").read_text(encoding="utf-8")
    m = re.search(r"Total: (\d+(?:\+\d+)*) = (\d+)", text)
    if not m:
        findings.append("18-call sum line not found in full-mode.md")
        return
    parts = [int(x) for x in m.group(1).split("+")]
    stated = int(m.group(2))
    if sum(parts) != stated or stated != CALL_CEILING:
        findings.append(f"call ceiling arithmetic broken: {m.group(1)} = {sum(parts)}, stated {stated}, expected {CALL_CEILING}")


def check_weights(root: pathlib.Path, findings: list[str]) -> None:
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"root-cause resolution (\d+)%.*?robustness[^ ]* (\d+)%.*?maintainability[^ ]* (\d+)%.*?performance/cost (\d+)%.*?risk/reversibility (\d+)%", text)
    if not m:
        findings.append("default weights sentence not found in SKILL.md")
        return
    if sum(int(g) for g in m.groups()) != 100:
        findings.append(f"default weights sum to {sum(int(g) for g in m.groups())}%, expected 100%")


def check_size_claims(root: pathlib.Path, findings: list[str]) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    claims = {
        "SKILL.md": r"this file \(~([\d.]+)k words / ([\d.]+)k chars\)",
        "references/lightweight-mode.md": r"lightweight-mode\.md` \(~([\d.]+)k words / ([\d.]+)k chars\)",
        "references/full-mode.md": r"full-mode\.md` \(~([\d.]+)k words / ([\d.]+)k chars\)",
    }
    for rel, pattern in claims.items():
        m = re.search(pattern, skill)
        if not m:
            findings.append(f"size claim for {rel} not found in SKILL.md Cost section")
            continue
        stated_chars = float(m.group(2)) * 1000
        actual = len((root / rel).read_text(encoding="utf-8").encode("utf-8"))
        if actual == 0:
            findings.append(f"{rel} is empty")
            continue
        if abs(actual - stated_chars) / actual > SIZE_TOLERANCE:
            findings.append(
                f"size claim drift for {rel}: stated ~{int(stated_chars)} chars, actual {actual} "
                f"(recount per the Cost section's own mandate)"
            )


def check_readme_line_claim(root: pathlib.Path, readme: pathlib.Path, findings: list[str]) -> None:
    if not readme.is_file():
        findings.append(f"README not found at {readme}")
        return
    m = re.search(r"~(\d+)-line stdlib-only transport", readme.read_text(encoding="utf-8"))
    if not m:
        findings.append("README line-count claim for the transport script not found")
        return
    stated = int(m.group(1))
    actual = len((root / "scripts/cross_model_score.py").read_text(encoding="utf-8").splitlines())
    if actual == 0:
        findings.append("cross_model_score.py is empty")
        return
    if abs(actual - stated) / actual > LINE_CLAIM_TOLERANCE:
        findings.append(f"README line-count claim stale: stated ~{stated}, actual {actual}")


def check_secrets(root: pathlib.Path, readme: pathlib.Path, findings: list[str]) -> None:
    paths = [root / "SKILL.md", *(root / f for f in MODE_FILES), *(root / f for f in TEMPLATE_FILES)]
    paths += list((root / "scripts").glob("*.py"))
    if readme.is_file():
        paths.append(readme)
    for p in paths:
        if SECRET_PATTERN.search(p.read_text(encoding="utf-8")):
            findings.append(f"possible secret material in {p.name}")


def lint(root: pathlib.Path, readme: pathlib.Path) -> list[str]:
    findings: list[str] = []
    check_files_exist(root, findings)
    if findings:
        return findings
    check_mentioned_paths(root, findings)
    check_mode_read_timing(root, findings)
    check_full_table(root, findings)
    check_lightweight_boxes(root, findings)
    check_call_sum(root, findings)
    check_weights(root, findings)
    check_size_claims(root, findings)
    check_readme_line_claim(root, readme, findings)
    check_secrets(root, readme, findings)
    return findings


def main() -> None:
    default_root = pathlib.Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=default_root)
    parser.add_argument("--readme", type=pathlib.Path, default=default_root / "README.md")
    args = parser.parse_args()
    if not (args.root / "SKILL.md").is_file():
        print(f"lint_skill: no SKILL.md under {args.root}", file=sys.stderr)
        sys.exit(2)
    findings = lint(args.root, args.readme)
    if findings:
        for f in findings:
            print(f"FINDING: {f}")
        sys.exit(1)
    print("lint_skill: clean")


if __name__ == "__main__":
    main()
