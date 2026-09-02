# Diagram sources

The README diagrams are pre-rendered PNGs so they display identically in every
browser. GitHub's in-browser Mermaid renderer measures text in a different font
than it displays, which truncated node labels (differently in Chrome and Safari),
so client-side rendering was dropped entirely.

## Diagrams

| Source | Purpose |
|---|---|
| pipeline.mmd | Tournament flow: mode selection through implementation |
| rounds.mmd | Scoring and crossbreed mechanics within each round |
| lifecycle.mmd | Phases 0–5 with decision points and outcome loops |

## Editing a diagram

1. Edit the `.mmd` source here.
2. Run `./regen.sh` (needs node; ~60s cold). It re-renders all PNGs and
   updates `.stamp`.
3. Commit the lot.

Do not run `mmdc` by hand: it skips the stamp and CI will reject the commit.

## How sync is enforced

`.stamp` holds a hash covering the sources, render config, and PNGs, written by
`regen.sh`. The `diagram-sync` workflow recomputes it on every push and PR that
touches `diagrams/` and fails on mismatch, so a `.mmd` edit cannot merge without
its re-rendered PNGs. `test-sync.sh` tests the detection itself. Rationale and
alternatives: `docs/decisions/0001-diagram-sync.md`.
