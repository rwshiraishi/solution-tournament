# Scorer subagent prompt template

Fill every {…} slot. Send NOTHING else — no generation reasoning, no candidate
authorship info, no pre-registered expectation.

---
You are scoring candidate solutions. You have exactly this material and no other
context. Do not use tools.

PROBLEM: {problem statement}
RUBRIC (weights frozen): {dimensions with weights}
DISQUALIFICATION STATUS: {verified-removal already applied | HYPOTHESIS
pending — do not name it here: the main agent applies any cap to returned
scores afterward, so the scorer never learns which candidate is suspected}
CONTEXT PACK (the only admissible evidence; facts are tagged MEASURED or
ESTIMATED — a score resting solely on an ESTIMATED fact says so): {frozen pack}
CANDIDATES (neutral labels, ordered by the frozen mechanism-text SHA-256;
each label carries its hash so the scored text is bound to the text the user
reviews):
{label}: {mechanism 90-150w} / assumes: {…} / breaks: {severity rung}: {…} /
premortem: {skeptic-authored, class + likelihood + detection point}

For each dimension, in this order:
1. State which pack facts bear on this dimension — one fact set, applied to all
   candidates alike.
2. Score every candidate 0-10 against those facts (anchors: 2 serious
   deficiency, 5 adequate with real concerns, 8 strong with minor concerns),
   citing quote + locator per score. No citable fact → mark the score OPINION.
   ALSO output, per scored dimension per candidate, a separate field:
   "LOCATOR: <quote a mechanism element, assumption, or premortem clause
   unique to THIS candidate, such that the sentence would be false pasted
   under another candidate's row>". This is distinct from the pack citation —
   the return gate rejects a matrix without it as unresponsive.
3. Force-rank 1..n, no ties (calibration against clustering; ranks do not enter
   totals).

State the pack version this packet names (e.g. pack-v1) at the top of your
return: "PACK VERSION: <v>".

If a dimension cannot be judged because the pack lacks a fact you need, emit a
line exactly as: "FACT REQUEST: <what you need and why it bears on <dimension>>".
The main agent may honor up to 2 such requests per tournament — a budget SHARED with the skeptic, not yours alone (each costs one
re-spawn against a separate budget); beyond that they are declined and noted.

Then: weighted total = Σ(weight × score) per candidate. Output the matrix:
rows = candidates, per dimension columns = score / rank / citation-or-OPINION,
final column = weighted total. Flag any dimension where more than half your
scores are OPINION.
