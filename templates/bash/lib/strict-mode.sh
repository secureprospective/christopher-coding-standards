#!/usr/bin/env bash
# lib/strict-mode.sh — sourced preamble every script in an adopting project
# should start with. Mirrors the Go overlay's struct-wrapped playerid and
# the Python/TS overlays' Pydantic/Zod boundary validation: fail loud and
# early, don't let a bad assumption (an empty arg, an unset env var, a
# non-numeric "number") silently propagate into the rest of the script.
#
# Usage — first executable line after the shebang:
#   #!/usr/bin/env bash
#   set -euo pipefail
#   here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   # shellcheck source=lib/strict-mode.sh
#   source "${here}/lib/strict-mode.sh"

set -euo pipefail
IFS=$'\n\t'

# Report the failing file:line on any untrapped error instead of a bare
# "command not found" or silent non-zero exit — `set -e` on its own tells
# you a script failed, not where.
trap 'echo "ERROR: ${BASH_SOURCE[1]:-$0}:${BASH_LINENO[0]} exited with status $?" >&2' ERR

# require_arg NAME VALUE — fail loud if a required argument/variable is
# empty or unset. Boundary validation for script inputs: never let a raw
# external value (a CLI arg, an env var) reach business logic unchecked.
require_arg() {
  local name="$1"
  local value="${2:-}"
  if [[ -z "${value}" ]]; then
    echo "ERROR: missing required argument: ${name}" >&2
    exit 1
  fi
}

# require_positive_int NAME VALUE — require_arg plus a numeric-shape check.
# The Bash analogue of the Go/Python schema templates' "parseable number"
# validation on a raw string field before it crosses into business logic.
require_positive_int() {
  local name="$1"
  local value="${2:-}"
  require_arg "${name}" "${value}"
  if ! [[ "${value}" =~ ^[0-9]+$ ]]; then
    echo "ERROR: ${name} must be a positive integer, got: ${value}" >&2
    exit 1
  fi
}
