#!/usr/bin/env bash
# Demonstrates the boundary-validation pattern from lib/strict-mode.sh.
# Not meant to be adopted verbatim — copy the shape (strict mode + source +
# require_* validation before any real work) into your own scripts.

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/strict-mode.sh
source "${here}/../lib/strict-mode.sh"

main() {
  local port="${1:-}"
  require_positive_int "port" "${port}"
  echo "Starting on port ${port}"
}

main "$@"
