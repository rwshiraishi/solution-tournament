# 0003 — Blind-assessment loop terminated at 9.4

Date: 2026-08-09. Status: accepted. Stop condition: 9.2 weighted. Achieved: 9.4 (round 127).

## Final scores (round 127, single blind assessor, unchanged bundle)
exec 9.1 · failure 9.4 · false-security 9.6 · cost 9.7 · scope 9.6 → weighted 9.440

Every dimension at or above 9.1. Executability cleared 9.0 for the first time in the
resumed loop; cost 9.7 and false-security 9.6 are the highest recorded in 127 rounds.
The graded bundle is byte-identical to the live skill (verified by diff).

## Trajectory of the resumed loop (rounds 113-127)
8.8, 9.0, 8.9, 9.0, 9.1, 9.0, 8.8, 9.0, 8.7, 8.7, 9.0, 8.4, 9.0, 9.0, 9.4

The 8.4 trough was a cost collapse (6.8) caused by my own arithmetic; the recovery to
9.7 came from publishing a DERIVATION rather than corrected numbers.

## What actually moved the score

1. PUBLISH FORMULAS, NOT FIGURES. Three consecutive rounds found cost errors of mine —
   asserting a number, computing from the wrong input, then mispairing bounds (printing
   an "overstatement" of 0.9x, which is incoherent since a total is never below its own
   marginal). Patching a fourth number would have been the bandaid. Printing
   `overstatement = fixed/marginal + 1`, with an explicit instruction on which bounds to
   pair, moved cost 6.8 -> 9.2 -> 9.7 and let the next grader recompute everything.
   Same treatment fixed the objection ceiling: bound = label count L, computed per run.

2. SINGLE-SOURCE EVERY CONSTANT AND LABEL. A label fixed in the branch table but not in
   the phase prose left two copies mandating opposite text — and since the phase governs,
   the surviving copy was the one the table said misroutes readers. The fixed-share figure
   drifted into two places with different values. Both are now owned in one place and
   pointed at from the other.

3. STOP CALLING POLICIES DERIVATIONS. The pre-flight abort claimed a run was "a guaranteed
   STOP by rule" when no rule keyed any outcome to a trigger's presence. The Phase 5 review
   was called "independent" while channel 5's correlated-same-model caveat was applied
   rigorously everywhere else. Both now state what they are.

4. FIX THE EXAMPLE WHENEVER YOU FIX THE RULE. The worked round repeatedly lagged rules I
   had added: an inverted pre-commitment (committing the falsifying range where the rule
   requires the entailed one), a "field reduced" label on a whole field, missing cap audit
   marks. The trace is billed as the imitable model, so every lag teaches the opposite of
   the rule.

## Remaining known weaknesses (deliberately NOT fixed)
- Cognitive load is the dominant residual and is structural: ~17.4k words, 48 boxes,
  11 counters, two ledgers. Three of the four degraded-execution strike sources route
  through a sweep the file labels DISCIPLINE; only absent-line and denominator-mismatch
  strikes are reader-computable.
- Severity gate sub-rule (2) narrows to route 2 where route 1 is available to any concern
  naming a mechanism. Fails safe.
- The applicability table's "both modes" column header vs the full-mode-only scoping.
- First-read attestation is self-reported, so the strongest gate can fire on it.
These were live at the 9.4 grade and are listed so the next session does not rediscover
them as new.

## Why the loop stopped here rather than continuing
The stop condition was met. Beyond that, the attribution experiment (record 0002) showed
dimension scores are NOT independent — the arithmetic requiring exec 9.54 for a 9.5
weighted is an estimate, not a measurement — and roughly one finding per round across the
resumed loop was a defect introduced by the previous round's fix. Continuing has a
measured chance of moving the score down.

## Addendum (2026-08-09): three-grader panel — the stable measurement

After the loop closed, a confirmation round scored 8.9 against round 127's 9.4 on a
near-identical bundle, exposing that any single-grader number is a draw from a band. A
three-grader panel was run on one frozen bundle (sha f372e162, includes every fix through
round 128), median pre-committed as the score before any result arrived.

Grades: A 8.9 · B 8.7 · C 8.8 → **PANEL SCORE 8.8** (median weighted; raw medians 8.75)
Weighted spread across graders: 0.15 — versus 0.7 across recent single rounds.

Per-dimension medians: exec 8.0 · failure 8.9 · false-security 9.2 · cost 9.0 · scope 8.8

What this establishes:
- The skill's STABLE quality is ~8.8, not the 9.4 a favorable single draw produced. The
  9.2-9.4 readings were the top of grader variance, not a level the artifact holds.
- The panel is far tighter than single rounds (0.15 vs ~0.7 spread), confirming the median
  of three as the honest instrument for any future measurement.
- All three graders independently recomputed every arithmetic claim and found ZERO errors —
  the derivation-not-figures approach has fully held since round 125.
- All three named cognitive load as the dominant residual, in nearly identical words,
  quoting the file's own admission. That is the structural ceiling: below ~21.5k words it
  does not move, and the tournament's own attribution experiment (record 0002) showed the
  cheap remedies are already taken.

Recurring panel findings not yet addressed (small, recorded for a future session):
- Phase 2.9 redistribution can zero a dimension without the drop that Phase 0.4 mandates
- Full mode's published interaction floor of 3 includes a terminal-decision ask no rule
  mandates on a decisive run
- The Exit Phase 3 enumeration may omit the spike's changed-lines threshold; the scorer
  template's DQ status line omits PARTIAL
