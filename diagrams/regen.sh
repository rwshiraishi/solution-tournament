#!/usr/bin/env bash
# Regenerate the README diagram PNGs from their .mmd sources and update the
# sync stamp that CI verifies. This script is the only supported way to
# regenerate: running mmdc by hand skips the stamp and CI will fail.
set -euo pipefail
cd "$(dirname "$0")"

for name in pipeline rounds; do
  npx -y -p @mermaid-js/mermaid-cli mmdc -i "$name.mmd" -o "$name-light.png" -b transparent -s 2
  npx -y -p @mermaid-js/mermaid-cli mmdc -i "$name.mmd" -o "$name-dark.png" -b transparent -s 2 -c dark-config.json
done

./stamp.sh > .stamp
echo "Rendered 4 PNGs and updated .stamp"
