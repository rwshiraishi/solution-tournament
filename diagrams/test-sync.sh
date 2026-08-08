#!/usr/bin/env bash
# Test for the failure mode that motivated the sync check: editing a .mmd
# without regenerating must be caught, and regen.sh must clear it.
set -euo pipefail
cd "$(dirname "$0")"
check() { [ "$(cat .stamp)" = "$(./stamp.sh)" ]; }

check || { echo "FAIL: clean tree reports drift"; exit 1; }
echo "PASS: clean tree in sync"

printf '\n%%%% drift test\n' >> pipeline.mmd
if check; then echo "FAIL: edited .mmd not detected"; git checkout -- pipeline.mmd; exit 1; fi
echo "PASS: edited .mmd detected as drift"
git checkout -- pipeline.mmd

tmp="$(mktemp)"; cp pipeline-dark.png "$tmp"
printf 'x' >> pipeline-dark.png
if check; then echo "FAIL: modified PNG not detected"; mv "$tmp" pipeline-dark.png; exit 1; fi
echo "PASS: modified PNG detected as drift"
mv "$tmp" pipeline-dark.png

check || { echo "FAIL: restore did not clear drift"; exit 1; }
echo "PASS: restored tree back in sync"
echo "ALL PASS"
