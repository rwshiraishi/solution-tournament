# Solution Tournament

A Claude Code skill that forces multiple genuinely different solutions to compete before any code gets written. Rubric first, blind scoring, adversarial pressure on every candidate, and a hard rule that symptom-patching scores zero.

The goal is a production-grade solution, not the first plausible one.

## The problem this solves

LLM coding assistants have a well-known failure mode: they commit to the first plausible approach. When that approach hits friction, they patch around it. Special cases accumulate. Errors get suppressed. A "temporary" flag ships to production.

Humans do this too. But an assistant does it faster, with more confidence, and without the nagging feeling that something is off.

This skill breaks that pattern structurally. It makes the assistant generate several solutions that differ on named architectural axes, subject each one to an adversarial skeptic, score them blind against a rubric that was locked before generation, and red-team the winner before implementation. Bandaid fixes are not just discouraged. They are disqualified by rule.

## The pipeline at a glance

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="diagrams/pipeline-dark.png">
  <img alt="Pipeline flow: mode choice, rubric approval, generation, skeptic pass, blind scoring, decision gate, red-team, implement" src="diagrams/pipeline-light.png">
</picture>

**Reading the diagram: amber nodes are decisions the user makes. Dashed-outline nodes are mechanical gates decided by rules and scores, with no judgment involved. Everything else is the LLM's work.**

The user touches the tournament at exactly two points: approving the rubric weights before generation (Phase 0), and approving the implementation plan before code is written (plan mode, for multi-file changes). Everything between those two points runs without the user, except that close calls and scorer disagreements are surfaced rather than silently resolved.

Node detail that used to live in the diagram, now here where it fits:

- **Pick mode** (LLM): lightweight is the default; full mode requires an explicit trigger (architecture, failed prior fix, high blast radius, or user request). When genuinely unsure, the LLM asks in one sentence.
- **Phase 0** (LLM proposes, user disposes): dimensions, weights, the disqualification rule, and a read of past decision records. Weights encode the user's values, which is why this is a user gate.
- **Structurally diverse?** (mechanical): each candidate must differ on a named structural axis. Paraphrases of one idea fail the check and force regeneration.
- **Margin over 10%?** (mechanical): the weighted score margin alone decides whether another round runs. Details in the rounds section below.
- **Phase 4** covers 10x scale, the 6-months test, the killer-assumption question, and the bandaid check.
- **Phase 5** requires tests for the motivating failure and writes the decision record to `docs/decisions/`.

Two loops can fire along the way: a **crossbreed loop** back into scoring when no candidate wins decisively, and a **runner-up loop** in red-team if the winner has a fatal flaw. Both are bounded.

## How it works

The pipeline is generate, score, crossbreed, implement. Six phases:

### Phase 0: Lock the rubric before generating

Scoring criteria are defined and weighted before any solution exists. This ordering is mandatory. Criteria chosen after seeing solutions become rationalizations for a favorite.

Default dimensions (adjustable per problem):

| Dimension | Default weight |
|---|---|
| Root-cause resolution (fixes the disease, not the symptom) | 30% |
| Robustness / production-readiness (edge cases, 10x scale, the 6-months-later test) | 25% |
| Maintainability / simplicity | 20% |
| Performance / cost | 15% |
| Implementation risk (blast radius, reversibility) | 10% |

The rubric goes to the user for approval before generation. Weights encode the user's values, not the assistant's. After approval, weights freeze for the round.

Phase 0 also defines a **disqualification rule**: any solution that treats a symptom while leaving the root cause intact scores 0 overall, regardless of how well it does on every other dimension. The symptom is named explicitly so the rule is checkable, not vibes.

Finally, it checks `docs/decisions/` for records of past tournaments in the same area, so rejected approaches stay rejected and constraints carry forward.

### Phase 1: Divergent generation

The skill generates n solutions (3 in lightweight mode, 5 in full mode) with structural diversity enforced:

- Each solution must differ from every other on at least one **named structural axis**: architecture, data model, dependency, algorithm class, or where the logic lives. Five paraphrases of one idea is a failed round and triggers regeneration.
- Slot #1 is reserved for the obvious approach, named explicitly so it cannot masquerade as several entries.
- At least one solution must be unconventional: something the assistant would normally self-censor as too weird or too ambitious.

Each candidate gets a mechanism description (150 words max), its assumptions, and what breaks it. Descriptions are equal length across candidates, because verbosity biases scorers.

### Phase 1.5: Skeptic pass

Before scoring, a single adversarial skeptic attacks all candidates in one batched pass: mechanism, assumptions, hidden costs. Each candidate then gets one revision pass with a hard guard: the revision may strengthen the solution but may not change its structural axis. This prevents the skeptic from sanding every candidate into the same safe shape.

Each revised solution ships with a **premortem** (80 words max): "It is 12 months from now and this solution failed in production. What happened?" Premortems travel with the candidates into scoring.

### Phase 2: Blind adversarial scoring

Self-scoring by the generator is unreliable. Scores cluster at 7 to 8 and drift toward the author's favorite. The skill counters this:

- A scoring subagent receives only a **context pack** (problem statement, locked rubric, disqualification rule, concrete constraints) plus the solutions under neutral shuffled labels (A, B, C). All generation reasoning is excluded.
- For high-stakes rounds, two independent scorers run and results aggregate by median rank. Sharp disagreement between judges is surfaced to the user as signal, not smoothed over.
- The disqualification rule applies first, before any scoring.
- Scoring uses **forced ranking within each dimension** (rank 1 to n, no ties) alongside scores, because comparative judgment is more reliable than absolute scores.
- The full weighted matrix is always shown. Never just the winner.

### Phase 3: Decision gate

If the top solution wins by a clear margin (over 10% weighted) and survives the red-team, it advances to implementation.

Otherwise, a **crossbreed round**: the top 2 or 3 candidates produce new offspring, each explicitly naming which traits it inherits from which parents ("B's storage model plus D's retry semantics"). One offspring gets a **mutation**: a single assumption perturbed. The same rubric scores the new field.

Maximum 3 rounds. If the top score plateaus (under 5% improvement round over round), the leader wins. Further rounds are churn.

### Phase 4: Red-team before implementation

Before production code, the winner faces a fresh adversarial pass:

- What happens at 10x data, traffic, or users?
- What happens in 6 months when the original context is forgotten?
- Which single assumption, if false, kills it? How would we detect that early?
- Is any part of this secretly a bandaid wearing a suit? Special cases, silenced warnings, magic constants, "temporary" flags.

If the top two finished within 10% of each other, both get red-teamed in parallel, so the runner-up cannot inherit the crown unexamined.

**Empirical spike gate:** for close races on spikeable problems, the skill builds a minimal throwaway prototype of each finalist, the smallest artifact that tests the killer assumption from its premortem, and lets the results break the tie. Evidence outranks judgment. Spikes are time-capped, and a spike that blows its cap is itself a signal the risk is real. Spike code never gets promoted to production.

### Phase 5: Implement to production standard

Production standard means: tests covering the failure mode that motivated the tournament, error handling for the assumptions identified in Phase 1, and no TODOs standing in for decisions.

The tournament ends by writing a **decision record** to `docs/decisions/`: problem, rubric and weights, final score matrix, winner and why, runner-up, red-team findings and mitigations. Future tournaments read these records in Phase 0. This is how the process compounds instead of resetting every session.

## Who decides what

Every decision in the tournament has exactly one owner: the user, the LLM, or a mechanical rule. Nothing is jointly owned, so nothing falls through the gap.

| Decision | Owner | How |
|---|---|---|
| Mode (lightweight vs. full) | LLM | Lightweight by default; full only on an explicit trigger. Asks the user when genuinely unsure. The user can always force full mode by requesting it. |
| Rubric dimensions and weights | **User** | LLM proposes, user approves or adjusts before generation. The single highest-leverage user decision: weights encode values. Skippable only if the user pre-authorized autonomous runs. |
| Disqualification rule (what counts as the symptom) | LLM | Proposed alongside the rubric, so the user sees it at the same gate. |
| Candidates, critiques, premortems, scores | LLM | Subagents in full mode, separated passes in lightweight mode. |
| Number of rounds | **Nobody** | Mechanical: score margin over 10% ends it, plateau under 5% ends it, round 3 ends it. No judgment involved. |
| Spike gate (build tiebreak prototypes?) | LLM | Opens automatically when the race is close and the problem is spikeable code. Effort is capped. |
| Close calls and scorer disagreements | **User** | Sharp inter-judge disagreement or a near-tie with a real tradeoff is surfaced with the matrix, not resolved silently. |
| Implementation plan (multi-file changes) | **User** | Plan mode approval before edits. |

## One round or many? One agent or many?

Two independent dials control how heavy a tournament gets. **Stakes** set the mode (how many candidates, whether subagents run). **Score margin** sets the round count (whether crossbreeding happens). They are decided at different times: the LLM chooses the mode up front, and the round count emerges from the scores with no one choosing at all.

### Dial 1: Stakes pick the mode (decided before the tournament starts)

| | Lightweight (default) | Full tournament |
|---|---|---|
| When | Contained bug, single-file change, reversible decision | Architecture, cross-cutting change, high blast radius, a previous fix failed, data-integrity stakes |
| Candidates | 3 | 5 |
| Skeptic pass | Inline: a clearly separated adversarial pass in the main thread | A fresh subagent attacks all candidates in one batched call |
| Scoring | Inline: steelman the case against each candidate, then score | A blind subagent sees only anonymized candidates + rubric |
| Scorers | 1 (self, in a separated pass) | 1 subagent; **2 independent subagents** for high-stakes rounds, aggregated by median rank |
| Red-team | Inline | Fresh subagent |
| Spike gate | Not used | Available for close races on spikeable problems |
| Rounds possible | Usually 1 | Up to 3 |

Lightweight is the default. Full mode requires an explicit trigger, so a typo fix never gets ceremony and a schema migration never skips rigor. Every principle (locked rubric, structural diversity, premortems, disqualification rule, full matrix) applies in both modes. What changes is who does the work: in lightweight mode the main thread wears different hats in separated passes; in full mode, independent subagents wear them, which buys real blindness at the cost of tokens.

### Dial 2: Score margin picks the round count (decided by the results)

One round is the normal case. Extra rounds are not "more thorough", they are a tiebreaker, and they only run when the scores say the race is genuinely close:

- **Clear winner (weighted margin > 10%)**: one round. Straight to red-team.
- **Close race (margin <= 10%)**: crossbreed round. The top 2 or 3 candidates produce offspring that explicitly name which traits they inherit from which parents, plus one mutation (a single perturbed assumption). The same frozen rubric scores the new field.
- **Plateau (top score improves < 5% round over round)**: stop, take the leader. Further rounds are churn.
- **Hard cap**: 3 rounds, no matter what.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="diagrams/rounds-dark.png">
  <img alt="Round-count flow: margin over 10 percent ends it, otherwise crossbreed until round 3 or plateau, close races red-team both finalists with optional spikes" src="diagrams/rounds-light.png">
</picture>

**Every gate in this diagram is mechanical (dashed outline): margins, round caps, and plateau thresholds decide, not judgment.** The user does not appear here at all, with one exception covered in the table above: when the stopped race is a genuine tradeoff, the finalists go to the user with the matrix and the red-team findings, as in the example below.

A close race also changes the endgame. When the top two finish within 10%, both are red-teamed in parallel, so the runner-up cannot inherit the crown unexamined if the winner falls. And in full mode, if the problem is code rather than strategy, the **spike gate** opens: a minimal time-capped throwaway prototype of each finalist tests the killer assumption from its premortem, and the measurements break the tie instead of judgment.

### Where the agents are (full mode)

Subagent boundaries exist for one reason: information hiding. The scorer must not see the generation reasoning, or it inherits the generator's favorite.

- **1 generator** (main thread): runs Phase 0 and Phase 1, holds full context.
- **1 skeptic subagent**: attacks all candidates in one batched call. One skeptic, not one per candidate, because the skeptic ranks nothing, so its independence buys little.
- **1 scoring subagent** (2 for high-stakes rounds): receives only the context pack and anonymized candidates. This is the boundary that matters most. Two scorers aggregate by median rank, and sharp disagreement between them is surfaced to the user as signal.
- **1 red-team subagent** (2 in parallel when the race was close).

Deliberation stays inside the subagents. Only summaries, the matrix, and decisions return to the main thread.

## When it triggers

Explicitly, when you say things like:

- "tournament" or "run the tournament"
- "generate 5 solutions and score them"
- "compare approaches" or "which option should we pick"

Proactively, when:

- A previous fix attempt failed
- You are stuck
- The task smells like it invites a bandaid: patching symptoms, special-casing inputs, suppressing errors

## Example

Say you report: "The dashboard query times out for accounts with more than 10k records. Previous fix (raising the timeout) didn't hold."

A typical assistant might raise the timeout again, or add a cache in front of the slow query. The tournament instead:

1. **Phase 0** names the symptom (slow query masked by timeout tuning) and locks the rubric. Any solution that adjusts timeouts without touching query cost scores zero. It also finds last quarter's decision record rejecting a read-replica approach and carries that constraint forward.
2. **Phase 1** generates five structurally distinct candidates: (A) add a composite index and rewrite the N+1 access pattern, (B) precompute aggregates into a summary table on write, (C) paginate the query and stream results to the client, (D) move the aggregation into a materialized view refreshed on a schedule, (E) the unconventional one: change the data model so the dashboard reads a purpose-built projection instead of the transactional tables.
3. **Phase 1.5** has the skeptic attack all five. B's premortem: "Write amplification made inserts slow; the summary table drifted from source during a partial outage and no one noticed for a week." That premortem travels into scoring.
4. **Phase 2** scores them blind. A wins on implementation risk, E wins on root cause and 10x robustness. They finish within 10% of each other.
5. **Phase 4** red-teams both. The spike gate builds a 30-minute prototype of each: A's index cuts the query from 9s to 400ms on production-shaped data; E's projection gets it to 80ms but the spike surfaces a migration cost the scorers underweighted. The user sees the matrix, the spike numbers, and the tradeoff, and picks A now with E recorded as the path if the account growth curve holds.
6. **Phase 5** implements A with a regression test pinned to the 10k-record failure case, and writes the decision record so the next tournament in this area starts from evidence instead of zero.

The output always includes the rubric, the score matrix per round, the decision trail, and red-team findings. You see why the winner won and what almost beat it.

## Why this beats just asking for options

You can always prompt "give me 3 options and pick the best." Here is what that gets you, and what the tournament does differently:

**Ad-hoc options converge; tournament candidates are forced apart.** Unstructured brainstorming produces three paraphrases of the same idea. The named-structural-axis requirement makes convergence a detectable failure that triggers regeneration.

**Ad-hoc scoring is motivated reasoning; tournament scoring is blind.** When the same context that generated the solutions also scores them, the favorite wins. Here the scorer sees anonymized candidates, a locked rubric, and nothing else.

**Ad-hoc criteria are post-hoc; the tournament rubric is locked first.** Criteria invented after seeing options get bent to justify a preference. Freezing weights before generation, with user approval, removes that degree of freedom.

**Ad-hoc picks skip the failure analysis; every tournament candidate carries a premortem.** Scorers judge each solution alongside a concrete story of how it dies in production.

**Ad-hoc processes reset; tournaments compound.** Decision records in `docs/decisions/` mean the tenth tournament in a codebase starts smarter than the first. Rejected approaches stay rejected. Constraints persist across sessions.

**And the structural difference from other review-style skills:** most quality skills inspect work after it exists (code review, verification loops, red-teaming a finished plan). The tournament applies pressure before and during solution selection, when changing course is cheap. It is anti-bandaid by construction, not by inspection: symptom patches are disqualified at the rubric level, and the "is this a bandaid wearing a suit" check runs before a single production line is written.

## Cost discipline

Deliberation stays in subagents. Only summaries, the score matrix, and decisions return to the main thread, so the tournament's transcript does not crowd out the implementation's context. Decision records are one page max. Token spend is logged per tournament, so calibration thresholds move based on real usage data, not intuition.

## Installation

Copy the skill into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/solution-tournament
curl -o ~/.claude/skills/solution-tournament/SKILL.md \
  https://raw.githubusercontent.com/rwshiraishi/solution-tournament/main/SKILL.md
```

Or clone and symlink:

```bash
git clone https://github.com/rwshiraishi/solution-tournament.git
ln -s "$(pwd)/solution-tournament" ~/.claude/skills/solution-tournament
```

Claude Code picks it up automatically. Invoke it with `/solution-tournament`, or just describe a problem worth competing over.

## Related skills

Works well alongside:

- **council**: four-voice structured disagreement for directional strategy calls. Use the tournament when candidates are concrete implementations to score; use council when the decision is a judgment call.
- **architecture-decision-records**: the Phase 5 decision record follows ADR conventions.
- **tech-stack-evaluator**: when the "solutions" are technology choices (framework, database, cloud) rather than implementation approaches.
- **verification-loop**: runs after Phase 5 to prove the winner actually works before marking it done.

## License

MIT
