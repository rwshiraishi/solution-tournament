# 0004 — Background-subagent report delivery (attended lightweight run, 2026-08-13)

**Problem.** Background subagents complete but reports never reach the main thread (three agents lost, nudges failed, scopes re-executed). TaskOutput-by-name errors even for live agents (reproduced by command: canary spawn + immediate blocking TaskOutput → "No task found").

**Rubric** (weights: defaults, user-approved): root-cause .30, robustness .25, maintainability .20, cost .15, risk/reversibility .10.
**Pre-registration:** "some form of synchronous-by-default wins" — **did NOT match the outcome** (user selected D+C composed; the pre-registered A finished third, capped).
**Mode verdict:** all full-mode triggers absent; lightweight, attended. Skip floor arguably cleared; run proceeded by user instruction (calibration data was itself a goal).

**Field** (n=3 grown to 4 by field-ceiling reopen — reopen counter spent):
- A sync-by-default (obvious; PARTIAL → root-cause capped 4, orig 7, magnitude 0.90, pre-committed C-robustness∈[6,10] → held at 7)
- B delivery-contract prompt (PARTIAL → capped 4, orig 5, magnitude 0.30, pre-committed C-root-cause∈[6,10] → held at 8)
- C mechanical harvest-on-idle (long shot; no cap)
- D Workflow-tool fan-out (added by reopen: in-process agent() returns bypass the broken channel entirely; no cap)

**Matrix** (self-scored unblinded; totals recomputed, both passes equal): D 7.75 · C 6.75 · A 6.55 · B 5.45. Margin D−C = 1.00, exactly at the >1.0 gate → **close pair**, surfaced as the run's top near-miss (distance 0.00). Contested dimension: maintainability (.20×|6−4|=0.40; rival root-cause 0.30).

**Red-team (self-administered, labeled):** no FATALs; severity gate passed both finalists (no data-loss rung, no high-likelihood correctness). Field-ceiling answer YES (Workflow) → the reopen above.

**Terminal:** close pair to the user → **"D + C composed" selected by user**; label: "selected by user; no evidence-floor gate fired for this finalist" (clearing re-run available: re-execute the F5 canary probe). Disclosure: self-administered EXCEPT the user's checks.

**Implementation (fidelity mapping, axis → artifacts):**
- D (orchestration substrate) → ~/.claude/rules/common/subagent-report-delivery.md §D
- C (retrieval/data model) → same file §C + ~/.claude/scripts/harvest_agent_tail.py
- adoption → memory/feedback_subagent_report_delivery.md

**Tests (motivating failure), verbatim:** `harvest_agent_tail.py canary-bg --session <session>` → `CANARY-OK-7391` (rc=0). Live fire: the same harvest recovered wire-refs' LOST 9-finding wiring report that two nudges had failed to retrieve — the fix retro-recovered real lost work during its own acceptance test. Validator: PASS (shape/arithmetic only). Repairs applied: none.

**Rejections carried (with blocker-checks):**
- A rejected as primary: blocker = serialization of genuine fan-outs; holds while `grep -c "Default to parallel" ~/.claude/rules/common/agents.md` ≥ 1.
- B rejected: blocker = unenforced compliance (observed failure class); not command-checkable — dated claim, never a standing block.

**Costs (counted):** 4 candidates authored + 1 canary evidence spawn, 1 scoring round, 0 in-run subagent calls, 3 user interactions (rubric, field check, terminal), reopen 1/1 spent.

## Appendix: verbatim candidate texts (frozen hashes)
A 1d4f0575d068baae5fe60570521bf490581ed4af71f9bffe7cdad0ca7dec939a · B a519eed745f8298fe17bd3fcb86f39daf4ca18af4e6c35f931122b25b6217c6e · C a7df7617d723ba51e9ea78a2d65fc12148178ad37d712146bc8e6440e45f232c · D (added post-reopen)

Any subagent whose deliverable is a report the main thread must consume - reviewers, verifiers, graders, auditors - is spawned with run_in_background:false, so the report returns in-band as the tool result and delivery cannot fail separately from completion. Background spawning remains for fire-and-forget work products (files written, commits made) whose success is checkable on disk. Where multiple independent checks are wanted, they are batched into a single synchronous agent's prompt rather than parallel background spawns. Implemented as a feedback memory plus an amendment to the parallel-first section of agents.md naming the report-bearing exception. Reversal is deleting the rule.

---
Every background spawn appends a standard contract block: name the agent at spawn; instruct that its FIRST action is SendMessage("STARTED") and its LAST action is SendMessage carrying the complete report - going idle without having messaged the report is defined as failure. Main-side rule: a missing STARTED within one turn, or an idle notification with no report received, triggers exactly one nudge, then the work is declared undelivered. Implemented as a reusable prompt snippet in a rules file plus the main-side handling rule. Delivery becomes push-based over the channel that empirically worked (F3) instead of the completion-notification channel that empirically did not (F1).

---
Stop depending on agent behavior for delivery. At spawn, record the agent_id from the spawn tool result. On any idle notification arriving without a report: first try TaskOutput with the RAW recorded id (name-based lookup is known-broken per F5; raw ids are untested); failing that, locate the agent's transcript file under the session directory and read only its TAIL - the final assistant message - since full transcripts overflow main context; only then nudge once. Implemented as a rules-file procedure plus a small helper script for the tail-read. Reports become retrievable even from a misbehaving or dead agent, and parallel-first spawning (F4) is preserved unchanged.

---
D: For multi-agent verification fan-outs, use the Workflow tool instead of raw background Agent spawns: agent() calls return results in-process to the workflow script — schema-validated when a findings schema is passed — and the workflow's final return lands as one tool result in main context; the completion-notification channel is never involved. Single checks stay synchronous Agent calls. Requires the user's standing opt-in for orchestration (the tool's own gate), recorded once. Implemented as a rules amendment routing "2+ report-bearing checks" to a Workflow with a findings schema.

## Appendix: pack v1 (verbatim, sha256 f47d69a91dc1517fdddc1c1586e22df396edc037df3d0e1902d4d804bcc96d89)
# Pack v1 — background-subagent report delivery failure (ECC)

Problem: In this ECC setup, background subagents complete without their reports reaching the main
thread, forcing manual nudges, self-execution of their scopes, or lost work. Choose and implement a
durable fix.

Facts:
- F1 MEASURED (trace: this session, wire-refs / wire-math / wire-script, 2026-08-13 ~18:36-18:46):
  three background Explore agents spawned in parallel finished their work but only idle
  notifications reached the main thread; no report content ever arrived. Two SendMessage nudges per
  agent produced only further idle notifications. Their scopes had to be re-executed by the main
  agent.
- F2 MEASURED (trace: this session, python-reviewer spawn, run_in_background:false): a synchronous
  reviewer spawn returned its complete report in-band in one call (~172s, 76.5k subagent tokens).
  Synchronous delivery worked on the first and only attempt.
- F3 MEASURED (trace: this session, sec-review-script / py-review-script): two named background
  agents delivered full reports as teammate messages ~9-11 minutes after spawn, each after one
  nudge. Background delivery is intermittent, not uniformly broken.
- F4 MEASURED (command: grep -n "Default to parallel" ~/.claude/rules/common/agents.md): the config
  mandates parallel-first subagent execution, so "just never use background" conflicts with standing
  config unless that config is amended.
- F5 MEASURED (command: TaskOutput{task_id:"canary-bg", block:true} immediately after a successful
  background Agent spawn of that name, this session): errors "No task found with ID: canary-bg".
  The blocking-retrieval path fails by name even for a live agent, reproducibly. (Same error earlier
  today for sec-review-script by name and by name@session.)
- F6 MEASURED (command: TaskStop{task_id:"wire-refs"} et al., this session): TaskStop DOES resolve
  the same names ("Successfully stopped task: tv3g220ti"), returning an internal task id of a
  different format. Name resolution works in TaskStop but not TaskOutput: the retrieval defect is
  tool-specific, not a naming defect.
- F7 ESTIMATED: the completion-notification channel (task-notification with final output) is the
  designed delivery path for background agents; today it delivered idle notifications without
  content for Explore-type agents. Mechanism unconfirmed - could be agent-type-specific,
  harness-version-specific, or load-related.
- F8 ESTIMATED: cost of the failure per incident, observed today: 2-3 nudge round-trips plus
  re-execution of the agent's scope in main context (several thousand tokens plus wall-clock).

Constraints:
- Any fix must be implementable in this ECC config (CLAUDE.md, rules/*.md, memory, hooks, or spawn
  practice). No harness source access.
- Must preserve real parallelism where it matters (F4) or explicitly amend that config.
- Reversible strongly preferred; this is process config, not product code.

## Appendix: run skeleton as validated
# tournament run 0002 — background-subagent report delivery

```st:meta
mode: lightweight
run_shape: attended-lightweight
```

pack-v1 sha256 f47d69a91dc1517fdddc1c1586e22df396edc037df3d0e1902d4d804bcc96d89

```st:weights
root-cause 0.30
robustness 0.25
maintainability 0.20
cost 0.15
risk 0.10
```

```st:matrix
D | root-cause=9 robustness=8 maintainability=6 cost=7 risk=8 | total=7.75
C | root-cause=8 robustness=7 maintainability=4 cost=8 risk=6 | total=6.75
A | root-cause=4 robustness=7 maintainability=9 cost=6 risk=9 | total=6.55
B | root-cause=4 robustness=4 maintainability=7 cost=7 risk=8 | total=5.45
```

contested dimension (close pair D-C), printed as arithmetic: maintainability 0.20 × |6−4| = 0.40; nearest rival root-cause 0.30 × |9−8| = 0.30; no drop: single computation
field-size line: field grown after field-ceiling reopen, n=4 of 3; 0 removed

near-miss sweep: 8 of 8 thresholds evaluated — decisive margin (1.00 vs 1.0, distance 0.00, WITHIN band 0.3 — surfaced), 5.0 floor (n/a (shape) — close pair), 0.3 tiebreak band (1.00 vs 0.3, distance 0.70), majority-OPINION weight stop (0 vs 0.25, distance 0.25), recompute discrepancy (0.00 vs 0.05, distance 0.05), pre-commitment width rule (4.0 vs 5.0, distance 1.0), cap-magnitude-vs-margin (0.90 vs 1.00, distance 0.10, WITHIN band 0.3 — recorded, pre-committed so no demotion), each active counter (reopen 1 of 1, distance 0, WITHIN band — recorded, threshold-decided)

disclosure: self-administered EXCEPT the user's checks

counters: reopen 1 of 1 (spent by field-ceiling reopen, Phase 4 rule) · re-entry 0 of 1 · re-scores 0 of 2 · post-freeze mutation 0 of 1 · scoring rounds 1 of 1 · subagent-only counters n/a (no subagents)

checklist: 15 of 15
