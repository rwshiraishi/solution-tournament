# Calibration protocol

Every threshold in the skill is a labeled convention, and the benefit side of its cost/benefit case is unmeasured. This protocol is how both get data. It costs nothing beyond using the skill.

## The protocol

1. Run the skill on real problems from the normal backlog — target 3–5 runs, mostly lightweight, at least one full run. Do not select problems to flatter the skill.
2. Let each run produce its decision record as the skill already mandates: countable costs, pre-registration vs. actual winner, near-miss count, terminal branch.
3. After each run, append one row to the table below.

## Run log

| # | Date | Mode | Problem (one line) | Pre-reg matched winner? | Terminal branch | Near-misses | NO WINNER? | Did any safeguard change the outcome? (which) | Record |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-08-08 | full | diagram sync strategy for this repo | — | decisive | — | no | filler early-exit bug caught; long-shot slot rule tightened | docs/decisions/0001-diagram-sync.md |

## Decision gates this data feeds

- **Threshold calibration**: after ~10 runs, check whether the 1.0 decisive margin, 0.3 bands, and 0.25 OPINION stop ever flipped an outcome near their values. Tune only from this table, never from intuition — and update the near-miss enumerations if any threshold moves.
- **Micro-tier decision** (Phase 4 of the 2026-08-13 weakness plan): if lightweight runs on small problems consistently show "no safeguard changed the outcome", build `tournament-lite` as a separate sibling skill (~1.5–2k tokens — a sibling is the only structure that escapes the fixed-load problem, since invoking this skill always loads SKILL.md). If the safeguards keep catching things, record that the micro tier is not warranted and close the question.
- **Mode boundary**: if full-mode triggers fire on problems that lightweight would have decided identically, loosen the trigger list; the reverse tightens it.
