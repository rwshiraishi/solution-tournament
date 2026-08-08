# 0002 — What actually caps the executability score

Date: 2026-08-08. Status: accepted. Method: solution-tournament (full mode), then an
attribution experiment the tournament's red-team identified as outranking its own finalists.

## Problem
112 rounds of blind grading plateaued at 8.7–9.3 weighted. Executability was the lowest
dimension in 19 of the last 20 rounds. Incremental fixing grew the file ~125 words/round
(13,745 at round 63 → 19,928 at round 112) and roughly a third of each round's findings were
defects introduced by the previous round's fix.

## Rubric (user-selected, "load-first")
exec-load reduction .35 · regression immunity .25 · preserve earned dimensions .20 ·
implementation cost/risk .10 · durability .10
DQ rule (user-selected): "leaves edits unverified — does it mechanically validate the
document's own invariants before an edit lands?"

## Result
The incremental-edit-protocol candidate was REMOVED by the DQ rule (VERIFIED): a protocol run
by the agent whose lapse it targets, producing no artifact, leaves the disease intact.
Round 1: lint harness 7.40 · compiled countables 6.85 · spine split 5.50 · finding corpus 4.93.
Round 2 (crossbreed): manifest-compiled spine 8.19 · incremental extraction 8.15 · both
anchors 6.61 / 6.32. Both offspring beat both parents. Margin 0.045 → CLOSE PAIR, NO WINNER.
One offspring was dropped as LAUNDERED (a parent relabelled).

## Spike (criteria before build, PASS, zero discrepancies)
The countable inventory IS mechanically extractable: ~20 lines of generic regex reproduced all
seven per-phase box counts (9,4,6,6,7,9,7 = 48), the 11-counter list, and 21 threshold class
tokens, with no hand-written per-item rules.

## Red-team field-ceiling finding (the decisive one)
The whole field assumed density causes the deduction. But graders were quoting the document's
OWN sentence back as the finding. Nothing in the field distinguished "density causes it" from
"the confession of density causes it". The red-team named an attribution experiment as
outranking both finalists. It was run.

## Attribution experiment (4 arms x 3 blind graders, EXEC only, size held within 80 words)
control 7.4/7.8/7.8 = 7.67 · confession removed 8.1/7.8/7.9 = 7.93 (+0.27) ·
7 long sentences split 8.2/8.2/7.8 = 8.07 (+0.40) · worked example repaired 7.8/8.4/7.9 = 8.03 (+0.37)
Within-arm spread averages 0.42; largest between-arm gap 0.40.

CONCLUSIONS
1. All three interventions beat control; none separates from the others (differences sit
   inside grader noise).
2. The strong confession hypothesis is FALSIFIED — it produced the SMALLEST gain, and graders
   in that arm located the density anyway from other text. Acting on the hypothesis without
   testing would have deleted the honest self-assessment (which scores 9.5) for nothing.
3. The CHEAPEST intervention performed best: splitting sentences at existing clause
   boundaries, zero content change.
4. Executability graded in isolation runs 7.4–8.4 vs 8.4–9.1 graded alongside other
   dimensions. Dimension scores are NOT independent, so the arithmetic requiring EXEC 9.54
   for a 9.5 weighted is demoted to ESTIMATED. The 9.5 target may be unreachable on this
   rubric at any density.

## Pack corrections forced by the process (pack-v2)
- F10 said "6 phases"; the document has SEVEN exit-checklist phases. Demoted to ESTIMATED.
- F7's MEASURED tag was overclaimed (arithmetic over maxima assuming independence). Demoted.

## Applied
- Worked example: pre-commitment semantics were INVERTED against rule 2.11(b) — it committed
  the falsifying range where the rule requires the ENTAILED range. Repaired. This bug survived
  112 rounds of assessment.
- Seven 200+-word sentences split (longest 375 → 192; none over 200 remain).
- Three verbless/spliced sentences repaired.

## NOT applied
Both structural finalists (manifest-compiled spine; incremental extraction). They cost 3.0 and
6.25 on cost/risk and rest on a causal theory this experiment showed is only partly true.
Revisit only if the cheap wins fail to hold.

## Process honesty
Two late repairs occurred (cap-inheritor named at Phase 1.5 instead of Phase 0; cap
pre-commitments never printed at application time), which is two strikes — this run does not
claim a clean execution. The pre-registered expectation (spine split would win) was WRONG; it
placed third of four.
