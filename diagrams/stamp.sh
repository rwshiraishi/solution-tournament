#!/usr/bin/env bash
# Print a hash covering the diagram sources, render config, and rendered PNGs.
# regen.sh writes this to .stamp; CI recomputes it and compares. A mismatch
# means a source or PNG changed without running regen.sh.
set -euo pipefail
cd "$(dirname "$0")"
shasum -a 256 pipeline.mmd rounds.mmd dark-config.json \
  pipeline-light.png pipeline-dark.png rounds-light.png rounds-dark.png \
  | shasum -a 256 | cut -d' ' -f1
