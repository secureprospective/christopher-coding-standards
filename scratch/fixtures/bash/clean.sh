#!/usr/bin/env bash

# Clean bash fixture — passes shellcheck, shfmt, gitleaks
# This file has no violations and contains no secrets.

set -euo pipefail

main() {
    local name="${1:-world}"
    local count=0

    for i in {1..3}; do
        echo "Hello, ${name}! (${i})"
        count=$((count + 1))
    done

    echo "Count: ${count}"
    return 0
}

main "$@"