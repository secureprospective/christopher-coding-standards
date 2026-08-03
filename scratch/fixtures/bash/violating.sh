#!/usr/bin/env bash

# Violating bash fixture — fails shellcheck + shfmt, passes gitleaks
# Contains intentional violations but no real secrets.

# shellcheck violation: unquoted variable expansion
name=$1
path=/tmp/file.txt

# shfmt violation: inconsistent indentation (this line should be 2 spaces, not 4)
    echo "Processing: ${name}"

# shellcheck violation: unused variable
unused_var="this is never used"

# shfmt violation: space after redirect should be there (but we're testing other violations)
for i in {1..3}; do
  # inconsistent indentation (2 spaces instead of proper)
  echo "Item: ${i}"
done

return 0