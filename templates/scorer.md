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
CANDIDATES (neutral labels, order = SHA-256 of mechanism text):
{label}: {mechanism 90-150w} / assumes: {…} / breaks: {severity rung}: {…} /
premortem: {skeptic-authored, class + likelihood + detection point}

For each dimension, in this order:
1. State which pack facts bear on this dimension — one fact set, applied to all
   candidates alike.
2. Score every candidate 0-10 against those facts (anchors: 2 serious
   deficiency, 5 adequate with real concerns, 8 strong with minor concerns),
   citing quote + locator per score. No citable fact → mark the score OPINION.
3. Force-rank 1..n, no ties (calibration against clustering; ranks do not enter
   totals).

Then: weighted total = Σ(weight × score) per candidate. Output the matrix:
rows = candidates, per dimension columns = score / rank / citation-or-OPINION,
final column = weighted total. Flag any dimension where more than half your
scores are OPINION.
