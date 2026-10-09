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

set -Eeuo pipefail
IFS=$'\n\t'

# -E inherits ERR into functions/subshells. Bash still suppresses ERR/errexit
# in handled conditions; do not treat this as universal error handling.
# Report the failing command's location and preserve its original status.
trap 'printf "ERROR: %s:%s exited with status %s\n" "${BASH_SOURCE[0]:-$0}" "${LINENO}" "$?" >&2' ERR

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

# require_positive_int NAME VALUE — positive ASCII decimal string.
# Leading zeros are allowed; all-zero strings are not. No arithmetic
# conversion means large inputs cannot overflow or become octal.
require_positive_int() {
  local name="$1"
  local value="${2:-}"
  require_arg "${name}" "${value}"
  if ! [[ "${value}" =~ ^0*[1-9][0-9]*$ ]]; then
    echo "ERROR: ${name} must be a positive integer, got: ${value}" >&2
    exit 1
  fi
}
