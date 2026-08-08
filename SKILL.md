---
name: solution-tournament
description: Run a weighted, multi-round solution tournament before implementing anything nontrivial. Use whenever the user says "tournament", "run the tournament", "generate n solutions", "score the options", "compare approaches", "which option should we pick", asks for multiple approaches to be compared and the best implemented, is stuck, or when a previous fix attempt failed. Also trigger proactively when a task smells like it invites a bandaid fix (patching symptoms, special-casing, suppressing errors) — bandaid solutions are unacceptable and this skill exists to prevent them. Includes a skeptic pass and premortems on every candidate before scoring, and an empirical spike gate for close races. Has a lightweight mode, so do not skip it just because the problem seems medium-sized.
---

# Solution Tournament

A structured generate → score → crossbreed → implement pipeline. The goal is a production-grade solution, not the first plausible one.

## Calibration: pick the mode first

- **Lightweight mode** (contained bug, single-file change, reversible decision): n=3, one round, inline adversarial scoring (steelman the case against each before scoring), skip subagents. Everything else below still applies.
- **Full tournament** (architecture, cross-cutting change, high blast radius, previous fix failed, data-integrity stakes): n=5 default, subagent scoring, up to 3 rounds.
- **Lightweight is the default.** Full mode must be justified by an explicit trigger (architecture, failed prior fix, high blast radius, user request). When genuinely unsure, ask — one sentence, not a ceremony.

## Phase 0: Lock the rubric BEFORE generating

This ordering is mandatory. Criteria chosen after seeing solutions become rationalizations for a favorite.

1. Restate the problem in one paragraph, including the failure mode of the current approach if one exists.
2. Define 4–6 scoring dimensions appropriate to the problem. Defaults (adjust per problem):
   - Root-cause resolution (fixes the disease, not the symptom) — default weight 30%
   - Robustness / production-readiness (edge cases, failure modes, 10x scale, 6-months-later test) — 25%
   - Maintainability / simplicity — 20%
   - Performance / cost — 15%
   - Implementation risk (blast radius, reversibility) — 10%
3. **Rubric checkpoint:** present dimensions and weights to the user for approval or adjustment before generating (use AskUserQuestion when available). Weights encode the user's values, not Claude's. Skip only if the user has pre-authorized autonomous runs; then state the weights and proceed. Weights freeze after this point in the round.
4. Define a **disqualification rule**: any solution that treats a symptom while leaving the root cause intact scores 0 overall regardless of other dimensions. Name what "the symptom" is for this problem so the rule is checkable.
5. Check `docs/decisions/` (or the project's equivalent) for records of past tournaments touching this area; carry forward relevant constraints and rejected approaches.

## Phase 1: Divergent generation (n solutions)

- Each solution must differ from every other on at least one **named structural axis** (architecture, data model, dependency, algorithm class, where-the-logic-lives). Five paraphrases of one idea is a failed round; regenerate.
- Solution #1 slot is reserved for the obvious approach — name it explicitly so it can't masquerade as multiple entries.
- At least one solution must be unconventional: something you would normally self-censor as too weird, too ambitious, or "not what they asked for."
- For each solution write: mechanism (≤150 words), what it assumes, what breaks it. Equal length across candidates — verbosity biases scorers.

## Phase 1.5: Skeptic pass (before scoring)

Every candidate faces an adversarial skeptic BEFORE anonymized scoring — pressure applied to all candidates equally and early beats pressure applied only to the winner late.

- **One batched skeptic call:** a single skeptic (fresh subagent in full mode; a clearly separated pass in lightweight mode) attacks ALL candidates in one pass — mechanism, assumptions, hidden costs — and produces critique → revision → premortem per candidate in that same call. Never one subagent per candidate; skeptic independence does not matter the way scorer independence does, because the skeptic is not ranking.
- Each solution then gets **one revision pass** with a hard guard: the revision may strengthen the solution but may NOT change its named structural axis. If answering the critique requires changing the axis, the solution stands as-is and the critique travels with it — this prevents the skeptic from sanding all candidates into the same safe shape.
- Each revised solution ships with a **premortem** (≤80 words): "It is 12 months from now and this solution failed in production. What happened?" Surviving critiques fold into it. Premortems are visible to the scorers.

## Phase 2: Blind adversarial scoring

Self-scoring by the generator is unreliable — scores cluster at 7–8 and drift toward the author's favorite. Counter it:

- Assemble a **context pack** for scoring: problem statement, locked rubric, disqualification rule, and the concrete constraints needed to judge feasibility (relevant file excerpts, interfaces, scale numbers, deadlines). Exclude all generation reasoning.
- **In Claude Code (full mode):** spawn a scoring subagent that receives ONLY the context pack plus the solutions and their premortems under neutral labels (A, B, C…) in shuffled order. For high-stakes rounds, spawn **two independent scorers** and aggregate by median rank per dimension; where the judges disagree sharply on a solution, surface that disagreement to the user — inter-judge variance is signal, not noise.
- **Lightweight mode:** score in a clearly separated pass, steelmanning the case AGAINST each solution before scoring it.
- Apply the disqualification rule first, before any scoring.
- Use **forced ranking within each dimension** (rank 1..n, no ties) plus a score; comparative judgment is more reliable than absolute scores.
- Compute weighted totals. Show the full matrix — never just the winner.

## Phase 3: Decision gate

- If the top solution wins by a clear margin (>10% weighted) AND survives the red-team below → implement it.
- Otherwise → crossbreed round: take the top 2–3 and generate z new solutions (default z=3), each explicitly naming which traits it inherits from which parents ("B's storage model + D's retry semantics"). Add one **mutation**: perturb one assumption (a constraint relaxed or tightened) in one offspring. Re-run Phase 2 with the same rubric.
- Maximum 3 rounds. If the top weighted score plateaus (<5% improvement round-over-round), stop and take the leader — further rounds are churn.

## Phase 4: Red-team before implementation

Before writing production code, attack the winner (via a fresh subagent when available). If the top two finished within 10% of each other, red-team **both in parallel** — the runner-up must not inherit the crown unexamined.

**Empirical spike gate (full mode, close races, spikeable problems only):** when the top two are within 10% and the problem is code (not strategy), build a minimal throwaway prototype of each — the smallest artifact that tests the killer assumption identified in its premortem — and let the micro-test results break the tie. Evidence outranks judgment. Cap effort explicitly (e.g., 30 minutes per spike); a spike that needs more than that is telling you the risk is real. Never promote spike code to production.

- What happens at 10x data / traffic / users?
- What happens in 6 months when the original context is forgotten?
- Which single assumption, if false, kills it? How would we detect that early?
- Is any part of this secretly a bandaid wearing a suit? (Special cases, silenced warnings, magic constants, "temporary" flags.)

If the red-team finds a fatal flaw, the runner-up (already red-teamed if the race was close) enters or continues Phase 4. If it finds fixable issues, fold the fixes into the implementation plan.

## Phase 5: Implement to production standard

- In Claude Code, enter plan mode first if the change touches multiple files or systems; get the plan approved before edits.
- Production standard means: tests covering the failure mode that motivated the tournament, error handling for the assumptions identified in Phase 1, no TODOs standing in for decisions.
- **Write the decision record** to `docs/decisions/` (create it if absent; use the project's ADR location if one exists): problem, rubric and weights, final score matrix, winner and why, runner-up, red-team findings and mitigations. Future tournaments read these in Phase 0 — this is how the process compounds instead of resetting.

## Output format

Every tournament ends with: the rubric with weights, the score matrix per round (compact table), the decision trail (who won, why, what was crossbred), red-team findings and mitigations, then the implementation. Never present only the winner without the matrix.

## Token discipline

The tournament's transcript competes with the implementation for context. Keep deliberation in subagents; only summaries, the matrix, and decisions return to the main thread. Decision records are ≤1 page. Log approximate token spend per tournament in the decision record — real usage data decides whether calibration thresholds move, not intuition.

## Related skills

- `council` — four-voice structured disagreement for ambiguous strategy/go-no-go calls; use this tournament when candidates are concrete implementations to score, council when the decision is directional
- `architecture-decision-records` — the Phase 5 decision record follows ADR conventions; use its format for `docs/decisions/`
- `tech-stack-evaluator` — when the "solutions" are technology choices (framework/database/cloud) rather than implementation approaches
- `verification-loop` — run after Phase 5 implementation before marking the winner done
