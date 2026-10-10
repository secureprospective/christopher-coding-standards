#!/usr/bin/env bash
# Legacy filename: optional source inventory, not a bloat/quality ratchet.
# No baselines, comment/tiny-file quotas or suppressed analyzer errors.
set -euo pipefail
if (($#)); then
  printf 'usage: bash scripts/bloat.sh (no baseline-update mode)\n' >&2
  exit 1
fi
list=$(mktemp)
trap 'rm -f -- "$list"' EXIT
find . -type f -name '*.go' ! -name '*_test.go' \
  ! -path './vendor/*' ! -path './tools/*' ! -path '*/node_modules/*' \
  -print0 | sort -z > "$list"
if [[ ! -s $list ]]; then
  printf 'inventory: no Go production files selected\n' >&2
  exit 1
fi
while IFS= read -r -d '' file; do
  awk 'END { printf "inventory: %s: %d physical lines\n", FILENAME, NR }' "$file"
done < "$list"
