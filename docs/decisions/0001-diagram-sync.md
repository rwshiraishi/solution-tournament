# 0001: Enforce diagram source/PNG sync with a hash stamp checked in CI

Date: 2026-08-08. Status: accepted. Mode: lightweight tournament, one round.

## Problem

README diagrams are committed PNGs rendered from `diagrams/*.mmd`. Editing a
source without re-rendering leaves the README silently stale. Diagnosis was
labeled HYPOTHESIS: predicted from the manual recipe, not yet observed.

## Rubric (locked before generation, user-approved)

Root-cause 30%, Robustness 25%, Maintainability 20%, Cost 15%, Risk 10%.
Disqualification: documentation-only solutions score 0.

## Field and matrix

- A: CI bot auto-regenerates and commits PNGs on .mmd push.
- B: CI gate fails when a hash stamp (sources + config + PNGs) mismatches.
  Skeptic revision replaced byte-comparing re-renders (non-deterministic
  across machines) with the stamp.
- C: mermaid.ink URLs instead of PNGs. FILLER VERDICT: drift relocates into
  the README URLs rather than disappearing; loses robustness and cost.
  Dropped before scoring.

| Weighted | A | B |
|---|---|---|
| Root-cause (30) | 9 | 8 |
| Robustness (25) | 7 | 8.5 |
| Maintainability (20) | 7 | 9 |
| Cost (15) | 8.5 | 7 |
| Risk (10) | 8 | 9 |
| **Total** | **7.93** | **8.28** |

## Decision

B, by 4.4% (inside the 10% margin; surfaced to user rather than decided by
arithmetic). Tiebreak values: A optimizes contributor convenience, B optimizes
failure-loudness. A's premortem is a silent-green regen action, which is the
project's named enemy. A remains the documented fallback if contributor
friction proves real.

## Red-team findings and mitigations

- B's killer assumption: diagram editors can run node. Mitigation: CI failure
  message names the exact fix command.
- Stamp is a proxy for "regen ran", not "PNGs correct", and is gameable by
  hand-editing `.stamp`. Accepted for a cooperative repo; noted here.
- Regen and stamp must be one script (`regen.sh`) or raw `mmdc` runs produce
  confusing failures.

## Token spend

Approximately 15k output tokens end to end (lightweight, no subagents).

## Skill bugs this run surfaced (fixed in SKILL.md)

1. Filler rule said "fewer than 3 candidates means one reasonable answer";
   dropping C left two credible candidates and no leader yet. Threshold
   corrected to "fewer than 2".
2. The mandatory unconventional slot often IS the filler; noted in the skill
   so the slot is filled with a credible long shot, not a token weird idea.
