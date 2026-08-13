# Run skeleton — solution-tournament

Fill this skeleton IN FLOW as the run executes — never backfill it at the end (a skeleton filled from memory at output time is where dropped steps hide; same rule as the ledgers). The fenced `st:` blocks are machine-readable: `scripts/validate_run.py` parses exactly these formats, so keep the field syntax intact. Everything outside the blocks is the ordinary prose output the phases already mandate.

```st:meta
mode: <lightweight|full>
run_shape: <attended-lightweight|autonomous-lightweight|attended-full|preauthorized-autonomous-full>
```

Pack hash line (verbatim, one of):
pack-v1 sha256 <64 hex chars>
pack hash unavailable — no execution tool

```st:weights
<dimension-name> <weight>
<dimension-name> <weight>
```
(One line per rubric dimension; weights must sum to 1.0. Use the post-normalization values.)

```st:matrix
<candidate> | <dim>=<score> <dim>=<score> ... | total=<weighted total>
```
(One line per scored candidate, REMOVED/DROPPED rows excluded — they have no totals. Every dimension in st:weights must appear in every row. The validator recomputes each total from the cells; discrepancy > 0.05 is a strike.)

Mandatory single-line artifacts (exact prefixes; the validator greps these):

near-miss sweep: <n> of <n> thresholds evaluated — <every threshold name from the mode's authoritative enumeration, comma-separated, with per-name distances or "none within band">

disclosure: <this run shape's disclosure line from SKILL.md Definitions; attended-full prints none>

counters: <every counter that exists in this mode with spent/budget, · separated; lightweight ends with "subagent-only counters n/a (no subagents)">

gate-order diff: <N> ticks / <N> artifact IDs matched   (full mode only)

checklist: <X> of 15                                     (lightweight — one consolidated line)
checklist: 9 of 9 · 4 of 4 · 6 of 6 · 6 of 6 · 7 of 7 · 9 of 9 · 7 of 7   (full — seven pairs, table denominators)

Then run, where an execution tool exists:

    python3 scripts/validate_run.py <this file> 

and paste its verbatim verdict into the output. A validator STRIKE is a degraded-execution strike (SKILL.md). PASS certifies shape and arithmetic only — never truth (SAC).
