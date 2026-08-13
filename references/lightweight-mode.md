# Lightweight mode — solution-tournament

Read this file when the mode verdict selects LIGHTWEIGHT, before Phase 0. A lightweight run loads SKILL.md plus this file, and fills `templates/run-skeleton.md` at output time — never `full-mode.md`, never the spawn templates (scorer/skeptic/red-team). SKILL.md governs shared rules; this file governs lightweight adaptations; a disagreement between them is a reported bug.

## What lightweight is

n=3, one scoring round, no subagents, unblinded self-scoring with an anti-favorite pass — never called "blind". No crossbreed rounds, no spikes, no cross-advocacy pass. Removals receive NO audit: self-authored removals stand unless Phase 2.11's falsification catches them, and that is the whole protection. Because it never crossbreeds, no NOISE sample ever exists: the 1.0 decisive gate is an uncalibrated convention applied to self-produced scores, and margins within 0.3 of 1.0 — on either side — are near-misses (box 9). Everything in SKILL.md applies except as adapted below.

## Phase adaptations

**Phase 0.** The pack the checkpoint froze is the pack: no late-fact protocol exists (no subagents to request one). Discovering the pack inadequate mid-run is a Phase 0 reopen or NO WINNER, never a quiet edit. Tag-tailoring to a held prior has no external check here: DISCIPLINE.

**Phase 1.** n=3.

**Phase 1.5.** The skeptic is the main agent: write ALL critiques and premortems before assigning any score — ordering discipline, not independence. Every DROPPED and REMOVED row carries "self-authored removal". Every abbreviated skeptic pass is self-administered and labeled.

**Phase 2.**
- Self-scores unblinded and says so in the output. Follow SKILL.md's numbered procedure exactly — including the forced 1..n ranking (n=3 self-scoring is precisely where 7–8 clustering happens) — writing the strongest case AGAINST each candidate before assigning any number. Templates are full-mode spawn material; never load them.
- Return gate: (a) completeness and "incomplete scoring" lapse (there is no return), and there are no ARITHMETIC CORRECTION rows. The recompute check (c) becomes: recompute the post-check total from the printed cells in a SEPARATE pass and print BOTH totals per row — the binding check is a READER recomputing from printed cells (SAC); under self-computation the demotion will essentially never fire from the agent's side — it is a reader-triggered rule, disclosure plus a hook. A discrepancy on either of the top two rows still makes the round a close pair. The responsiveness test (b) still binds — it matters MOST where author and scorer are the same agent — but autonomously its failure is self-declared: what a reader actually gets is the quoted locator to paste-test. An autonomous failed locator test is NO WINNER (SKILL.md step 0).
- Cite-before-score becomes an ARTIFACT: the per-dimension fact block prints as its own block BEFORE any score appears. A matrix printed above its fact block is a visible order violation a reader can see without trusting a sweep.
- HYPOTHESIS cap: the anti-anchoring separation is VOID (the self-scorer authored the DQ verdict and cannot be blinded to it); the cap still applies, flagged with the hypothesis and the original value.
- Struck cells read "STRUCK (self-verified against a self-authored pack)"; a recovery re-score reads "SELF-SCORED (rewrite, not repair: same agent authored the pack, the citation, and the strike)".
- No scorer combination exists; of Phase 2 step 7 only the shared re-score budget (2) applies.
- OPINION: the single self-scorer's mark alone makes a cell OPINION — the safeguard never switches off in the one-scorer configuration.
- Redistribution (2.9): forbidden. At weight ≥ 0.25 a majority-OPINION dimension is an autonomous STOP; below, the dimension keeps full weight and the round is a close pair labeled "majority-OPINION below the stop".

**Phase 3 — the lightweight routing row.**
1. Never crossbreeds. A TWO-candidate field is a close pair regardless of margin (SKILL.md Rule F3 restated here because it surprises).
2. Margin > 1.0 → decisive. With a user PRESENT, a decisive result requires ONE explicit confirmation before Phase 5: print the winner, its margin, the deciding dimension with its re-run output, and the disclosure line "self-administered EXCEPT the user's checks" — then ask. One interaction, inside the published 3–4 range. Autonomous decisive keeps its path with its label.
3. Margin ≤ 1.0 → close pair. User present: the choice goes to the USER with the matrix and the self-red-team findings — self-scored close calls are exactly where self-scoring fails; never resolve one alone with a user available.
4. AUTONOMOUS close call — ONE ordered procedure, no second route; a run satisfying an earlier step never skips a later one:
   - (4a) GATE FIRST: re-run ONE MEASURED fact bearing on the CONTESTED DIMENSION — the dimension with the largest absolute weighted score difference between the two finalists; ties to the higher weight; residual ties alphabetically by dimension name as printed in the rubric — with verbatim output in the record. CONFIRMS the pack → continue. CONTRADICTS → demote the fact to ESTIMATED, emit pack-v2 with the diff, NO WINNER. AMBIGUOUS = CONTRADICTS (the adjudicator authored both claim and command). Nothing re-runnable → NO WINNER. A command that fails to execute or exits nonzero IS "nothing re-runnable", not AMBIGUOUS — an error is the absence of evidence. Presence of output is not agreement.
   - (4b) Eliminate any finalist carrying a standing CONCERN at the DATA-LOSS rung or a HIGH-likelihood CORRECTNESS rung. Exactly one survives → it wins. None → NO WINNER.
   - (4c) Both survive → take the MORE REVERSIBLE (fewer files touched, no data migration, no schema change), judged against the pack, comparison printed.
   - (4d) Reversibility ties → NO WINNER, never a coin flip.
   - (4e) Label any result from this branch "close call, self-scored, unreviewed".
5. EXCEPT — replacing sub-rule 4's autonomous branch ONLY, never sub-rule 3's attended close pair — on a ZERO-EVIDENCE-OR-FIELD-INTEGRITY FAILURE: an evidence-floor failure, a zero-MEASURED pack, a failed responsiveness test, a majority-OPINION dimension at weight ≥ 0.25, an UNFALSIFIABLE removal on any path (2.11(d)), or a BROKEN REMOVAL PREMISE — each is NO WINNER outright. The first four share the zero-evidence shape; the last two are field-integrity failures, and the last is worse: the FIELD is suspect, and no self-administered re-run rehabilitates a culling known to rest on a falsified premise.

**Phase 4.** The main agent self-administers the standing questions, the pack-interrogation block, and the field-ceiling question — all findings labeled self-authored. There is no audit. The severity gate's rung is self-assigned and must NAME the premortem clause or pack fact it derives from; an anchor-less rung prints UNRUNGED and takes the DATA-LOSS default. The gate's row prints "severity rung self-assigned (lightweight)". Autonomously an unrunged CONCERN cannot be re-runged by the same agent — it clears only by route 2's named test command. The self-red-team is unbudgeted (no calls exist).

**Phase 5.** The implementation review is a self-review labeled SELF-ADMINISTERED.

## Autonomous honesty

Autonomous lightweight — the default mode — ends in NO WINNER on every close-pair, sole-survivor, majority-OPINION, unfalsifiable-removal, and severity-gate branch. An un-pre-committed removal routes UNFALSIFIABLE, so the EXPECTED outcome of an autonomous run that removes any candidate without a DQ pre-commitment is NO DECISION. Read that before running one unattended: the honest headline is "compare and report", not "compare and implement", unless the run stays clean and decisive. An autonomous lightweight run on a problem carrying ANY full-mode trigger is ABORTED PRE-FLIGHT (SKILL.md, Calibration).

## Consolidated checklist — 15 boxes, printed once at the terminal

Every box prints in EVERY run; a conditional sub-part that does not apply prints its exclusion inline ("decisive confirmation: n/a (autonomous)", "evidence-floor artifact: n/a — close pair, route named"), so the denominator is 15 in every run shape and never a judgment. Same @flow/@late tags and mismatch rule as SKILL.md's checklist section.

1. pack file + tagged facts + printed hash
2. problem restatement + pre-registration sentence
3. normalized weights + provenance line
4. DQ falsifiable test + per-candidate verdicts (including any DQ pre-commitment row+range, and the execution-bar demonstration with verbatim output when any VERIFIED verdict stood)
5. mode verdict incl. user reachability + cap-inheritor line
6. candidates with named axes, mechanisms, premortems
7. verbatim field shown (or in record)
8. matrix (scores, ranks, locators/OPINION flags) + weighted totals + contested-or-deciding-dimension line printed AS ITS ARITHMETIC (weight × score-difference product for the selected and nearest rival dimension, never a bare name; printed TWICE — pre-drop and post-drop, pre-drop binding — when a dimension was dropped, else once with "no drop: single computation") + field-size line ("field reduced: n=X of Y, Z removed", or that the field was whole) — one box, four mandatory prints
9. NEAR-MISS SWEEP line over THIS list — lightweight's authoritative diff target — printing "<n> of <n> thresholds evaluated" with n counted from this box at print time; thresholds unreachable by RUN SHAPE (the decisive margin and tiebreak band in a close-pair or sole-survivor run) print "n/a (shape)" and still count, so the denominator never moves; "each active counter" is ONE named entry however many counters are live. The list: decisive margin [D, band 0.3] · 5.0 floor [D, 0.3] · 0.3 tiebreak band [D, 0.3] · majority-OPINION weight stop at 0.25 [D, 0.03 — weights live on 0–1] · recompute discrepancy at 0.05 [X, 0.02] · pre-commitment width rule at 5.0 [D, 0.3] · cap-magnitude-vs-margin comparison [D, 0.3] · each active counter [X, one integer unit]. Thresholds that cannot arise in lightweight (NOISE, the 1.5 ceiling, plateau delta, DISPUTED spread, weight×spread) are NOT printed. Each printed value names the matrix cell or output line it was read from; the subtraction is content-verifiable, the value itself attested (SAC).
10. evidence-floor re-run artifact (decisive only — deciding dimension named with per-cell provenance, MEASURED fact cited, re-run command + verbatim output + one relevance line "this output, had it read otherwise, would have moved <candidate>'s <dimension> score <up/down>"; file/trace facts carry the first-read attestation line "re-read location: first read in session" or "previously read this session", the second value routing to close pair by rule) — or the close-pair route named
11. self-red-team report + FATAL re-check results
11a. severity-gate determination (rung + likelihood + outcome) — the fifteenth box, numbered to keep neighbors stable
12. terminal decision + decisive confirmation (user present) + this run shape's disclosure line
13. tests with verbatim output + validate_run verdict (or "validator: NOT RUN — no execution tool") + implementation self-review (labeled SELF-ADMINISTERED) + decision record + index line
14. COUNTERS ledger final line, covering the counters that EXIST in lightweight: reopen (1) · re-entry (1) · re-scores (2) · post-freeze mutation (1) · scoring rounds (fixed, printed "1 of 1"); the subagent-only counters (completeness slots, fact requests, read-only verifications, red-team calls, spike attempts, reserved abbreviated-skeptic slot) print once as "n/a (no subagents)". Instantiate the ledger at Phase 0 as one fixed template line with every counter pre-listed at zero, updated IN PLACE at every spend.

Lightweight keeps ONE ledger (COUNTERS) and NO GATE-ORDER ledger — that ledger audits multi-agent interleaving, and a mode with no subagents has none. Lightweight's ordered-execution check is box 8's arithmetic print plus this fixed 15-box skeleton; its strike sources are the @late tag, a box count below 15, and an absent line.

The post-freeze mutation budget here caps a near-empty set (lightweight never crossbreeds and regeneration precedes the freeze — only regeneration beyond the once-per-run rule remains); it is kept for uniformity with full mode. A second agent-initiated mutation demotes the round to a close pair. User objections and re-admissions never touch it.

## Interaction budget

Agent-initiated: rubric checkpoint + verbatim field + exactly one terminal decision (close-pair / sole-survivor / decisive confirmation — mutually exclusive by construction) = 3 mandatory, plus at most ONE batched near-miss question = 3–4. If the pre-Phase-0 mode-uncertainty ask fired, 4–5.

Total exchanges: add user-initiated objections, capped at one per LABEL ISSUED — removed and dropped rows are objectable via re-admission, and regeneration issues fresh labels — so the bound is L = n + regenerated slots. Total = agent-initiated + L; compute L for the run at hand (n=3, no removals: up to 7; two removed and regenerated: L=5, up to 9–10). An objection is a reply to an artifact already shown, never a new agent ask. The severity-gate override and the survivor-floor decision are the CONTENT of the terminal-decision exchange, never separate asks. If the count feels high for the problem, the mode choice is wrong.

## Cost

0 subagent calls; ALL deliberation lands in the main thread. Countable marginal artifacts: 3 candidates × (90–150w mechanism + assumptions + breaks) + 3 critiques + 3 premortems (≤80w) + ~5 dimensions × 3 cited scores + matrix + self-red-team ≈ 2,000–3,500 words ≈ 5–10k tokens including surrounding reasoning (ESTIMATED — derived from the word bands, not measured). Fixed load = SKILL.md + this file; current figures live in SKILL.md's skip floor and are recounted on every material edit.
