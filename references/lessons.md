# Lessons ledger (living document)

Appended after every run (see SKILL.md "Self-improvement loop"). Statuses:
CANDIDATE → PROMOTED (two confirmations, or one airtight causal chain; edit the
skill, date-stamp, record `landed-in`) → DEMOTED (counter-evidence; revert the
edit, never silently delete). Guardrails: promotions may tighten but never
weaken BINDING rules, evidence bars, or adversarial phases; every rule cites its
run(s); mechanisms that produced nothing get recorded too.

## L-T1 — red-team-overturns-the-scored-winner — PROMOTED
- **Rule**: A pre-Phase-4 ranking is a hypothesis. Never skip or thin Phase 4 to
  save cost; it is empirically where the decision gets made.
- **Evidence**: 3/3 recorded DataSculpt runs (2026-07-14 craft-crux, 2026-07-28
  concept-execution, 2026-08-14 concept→execution gap) overturned the scored #1
  at red-team. 2026-08-14: the #1's central premise was false on 2/2 measured
  figures (falsified in one grep), its worked example fabricated, and three
  same-family scorers gave it 6.5 with zero spread; the eventual winner had been
  ranked last. The generate-and-score half has never yet produced a decision
  that survived adversarial review unchanged.
- **Landed-in**: SKILL.md Cost honesty (benefit-side paragraph).

## L-T2 — dont-rescore-a-hunted-field — PROMOTED
- **Rule**: A field already scored by novelty-hunt's full-mode panel enters this
  skill at the adversarial phases (1.5 skeptic, Phase 4) with scores carried and
  labeled; the middle scoring phases are skipped as duplication.
- **Evidence**: Run 2026-08-14: the two skills' scoring stacks specify the same
  blind weighted scoring; running both would have scored one field twice with
  correlated judges. The tournament's unique contribution in that run was the
  code-verifying skeptic and the red team.
- **Landed-in**: SKILL.md Related skills (novelty-hunt entry); novelty-hunt
  SKILL.md interop section (mirror rule L-N9).

## L-T3 — zero-spread-is-a-warning-not-corroboration — CANDIDATE
- **Rule (provisional)**: Same-model scorer agreement with zero spread on a
  high-scoring candidate should raise, not lower, the priority of executing that
  candidate's factual claims (bias channel 5 in the flesh). The file already
  states DISPUTED detects divergence, never shared error; this adds: near-zero
  spread on a leader is itself a cue to spend a spike or re-run on the leader's
  checkable claims.
- **Evidence**: Run 2026-08-14: zero spread across three scorers on a candidate
  whose premise one grep falsified. One run; the existing evidence-floor
  machinery partially covers this — needs a second observation to justify a
  BINDING addition.

## UNANSWERED
- **U-T1**: How often do the SCORING phases (vs the red-team) change the final
  outcome relative to just fixing the thing? No data; the benefit side of the
  cost table stays unpriced until run records accumulate.
- **U-T2**: Would cross-vendor scorers have produced spread on the 2026-08-14
  falsified #1? Needs a run with a second vendor configured (mirror of
  novelty-hunt U-N2).

## Run 2026-08-18 — DataSculpt, "density is an undeclared channel"

Full mode. 5 candidates + 3 crossbreed offspring, 2 scorers/round (one CROSS-TIER),
2 rounds, 6 calls before red-team. Weights defaults-approved. No removals all run.

### Mechanisms that EARNED their cost
- **Plateau rule — decisive, and the single most valuable thing the skill did.**
  No offspring beat the carried anchors (best offspring 5.150 vs anchor 5.875;
  bar max(0.5, NOISE=0.70)). That firing is what stopped the run and triggered a
  novelty hunt, whose first execution test then falsified the premise the whole
  tournament rested on. Without the plateau rule this run ships a fix that
  DELETES a real data channel.
- **Return-gate recompute (Phase 2 step 0c).** Caught arithmetic errors on 5 of 5
  rows from one scorer, up to 0.30 off, including both top rows. Mechanical catch,
  no judgment involved.
- **Cap pre-commitment.** Both round-1 cap premises were stated as falsifiable
  ranges before scores existed and both held (predicted the uncapped candidate's
  root-cause original in [7,10]; it scored 8,8 then 7,7).

### Findings

## L-T4 — the-pack's-FRAMING-is-unfalsifiable-inside-the-tournament — CANDIDATE
- **Rule (proposed)**: import novelty-hunt's Phase 3.5. Run a cheap execution
  test against the PROBLEM STATEMENT before Phase 2, not only spikes at Phase 4.
- **Evidence**: Run 2026-08-18. pack-v1's problem statement asserted that the
  wind map's density "reports FIELD CONVERGENCE" as an artifact of seeding. Every
  one of 8 candidates, both skeptic passes and all 4 scorer passes reasoned from
  that framing and none questioned it. A 4-render perturbation test (~80s, $0)
  showed the density field is invariant to sampler rate and phase (r = 0.9938 to
  0.9972, same hottest bin), i.e. the density is SIGNAL, not artifact — so the
  leading finalist's mechanism (flattening by evenly-spaced placement) would have
  deleted a true channel. The evidence floor validates FACTS; nothing validates
  the FRAMING those facts are assembled into. Bias channel 3 lists pack error but
  its only counter is red-team interrogation, which arrives after every score.

## L-T5 — named-axes-are-not-distinct-premises — CANDIDATE
- **Rule (proposed)**: at Phase 1, print the premise SHARED by every candidate as
  a required artifact, and treat a field that shares one as a failed generation.
- **Evidence**: Run 2026-08-18. Phase 1's "named structural axis" requirement was
  satisfied — five candidates on five genuinely different axes (where-the-logic-
  lives, L1 vocabulary, verification layer, a different invariant, mark ontology).
  All five were nonetheless the same question rotated: *where should the density
  constraint live?* The three crossbreed offspring inherited the premise and the
  plateau fired. A novelty hunt, explicitly barred from the premise, produced 21
  candidates in ~16 classes including the one that won. Axis-distinctness is
  satisfiable while premise-distinctness is not.

## L-T6 — caps-can-be-outcome-sized-and-self-refereed — CANDIDATE
- **Rule (proposed)**: when a cap's magnitude exceeds the round's margin, the
  pre-commitment must bind THE CAPPED CANDIDATE's own contested cell, not a third
  party's.
- **Evidence**: Run 2026-08-18. A PARTIAL cap moved one candidate's root-cause
  from a two-scorer mean of 7.0 to 4.0 — 0.90 weighted points — and flipped the
  round leader (uncapped 5.925 would have led 5.875). Both scorers had rated that
  cell 8 and 6; the main agent overrode both. The cap WAS pre-committed, but the
  commitment named a different candidate's row, so nothing in the matrix could
  falsify the contested judgment itself. Cap accounting caught the magnitude
  (printed 0.90) but the demotion clause only fires for UN-pre-committed caps.

### Interop
The two skills composed well in one direction: the tournament's plateau rule
DETECTED field exhaustion and handed off to the hunt, which produced the winner.
Recorded as the first observed instance of tournament→hunt escalation working.

### Cost
6 subagent calls pre-red-team; ~1 pack revision (v1→v2, honoring 1 skeptic fact
request); 1 protocol deviation recorded (declined the mandated skeptic re-spawn
against pack-v2, reason printed). Harvest via harvest_agent_tail.py required for
6/6 background spawns — none delivered its report in-band.
