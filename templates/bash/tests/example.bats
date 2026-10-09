#!/usr/bin/env bats
# Run the real library in child Bash: its strict options/IFS/trap must not
# modify the Bats driver. Command arguments are positional, never interpolated.

setup() {
  library="${BATS_TEST_DIRNAME}/../lib/strict-mode.sh"
  example="${BATS_TEST_DIRNAME}/../scripts/example.sh"
}

run_helper() {
  run bash -c 'source "$1"; shift; "$@"; printf "continued\n"' bash "${library}" "$@"
}

@test "require_arg rejects empty without continuing" {
  run_helper require_arg "foo" ""
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"missing required argument: foo"* ]]
  [[ "${output}" != *"continued"* ]]
}

@test "require_arg rejects missing value" {
  run_helper require_arg "foo"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"missing required argument: foo"* ]]
}

@test "require_arg preserves nonempty strings" {
  for value in "bar" "two words" "0"; do
    run_helper require_arg "foo" "${value}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "continued" ]
  done
}

@test "positive integer rejects zero and all-zero strings" {
  for value in "0" "00" "00000"; do
    run_helper require_positive_int "count" "${value}"
    [ "${status}" -eq 1 ]
    [[ "${output}" == *"count must be a positive integer"* ]]
    [[ "${output}" != *"continued"* ]]
  done
}

@test "positive integer rejects negatives and malformed strings" {
  for value in "-1" "+1" "1.5" "1e3" "12x" "abc" " 1" "1 " $'1\n2'; do
    run_helper require_positive_int "count" "${value}"
    [ "${status}" -eq 1 ]
    [[ "${output}" == *"count must be a positive integer"* ]]
    [[ "${output}" != *"continued"* ]]
  done
}

@test "positive integer rejects empty and missing value" {
  run_helper require_positive_int "count" ""
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"missing required argument: count"* ]]
  run_helper require_positive_int "count"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"missing required argument: count"* ]]
}

@test "positive integer preserves positives and leading zeros" {
  for value in "1" "8080" "08" "0001" "00100"; do
    run_helper require_positive_int "count" "${value}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "continued" ]
  done
}

@test "positive integer does not overflow on large decimal strings" {
  printf -v zeros '%0200d' 0
  run_helper require_positive_int "count" "1${zeros}"
  [ "${status}" -eq 0 ]
  [ "${output}" = "continued" ]
  run_helper require_positive_int "count" "${zeros}"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"count must be a positive integer"* ]]
}

@test "example rejects missing input with no success output" {
  run bash "${example}"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"missing required argument: port"* ]]
  [[ "${output}" != *"Starting on port"* ]]
}

@test "example rejects zero negative and malformed input before work" {
  for value in "0" "000" "-1" "not-a-port" "12x"; do
    run bash "${example}" "${value}"
    [ "${status}" -eq 1 ]
    [[ "${output}" == *"port must be a positive integer"* ]]
    [[ "${output}" != *"Starting on port"* ]]
  done
}

@test "example preserves exact positive and leading-zero output" {
  for value in "8080" "0008"; do
    run bash "${example}" "${value}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "Starting on port ${value}" ]
  done
}

@test "shell metacharacters remain data and cannot execute" {
  marker="${BATS_TEST_TMPDIR}/unexpected-file"
  value='$(touch "'"${marker}"'")'
  run bash "${example}" "${value}"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"port must be a positive integer"* ]]
  [[ "${output}" != *"Starting on port"* ]]
  [ ! -e "${marker}" ]
}

@test "ERR reports top-level failing file line and original status" {
  script="${BATS_TEST_TMPDIR}/failure.sh"
  printf '%s\n' 'source "$1"' "bash -c 'exit 7'" 'printf "continued\n"' > "${script}"
  run bash "${script}" "${library}"
  [ "${status}" -eq 7 ]
  [ "${output}" = "ERROR: ${script}:2 exited with status 7" ]
}

@test "ERR inherits into ordinary function calls" {
  script="${BATS_TEST_TMPDIR}/function-failure.sh"
  printf '%s\n' 'source "$1"' 'fail() {' "  bash -c 'exit 7'" '  printf "continued\n"' '}' 'fail' > "${script}"
  run bash "${script}" "${library}"
  [ "${status}" -eq 7 ]
  [ "${output}" = "ERROR: ${script}:3 exited with status 7" ]
}

@test "pipefail reports pipeline line and original failure" {
  script="${BATS_TEST_TMPDIR}/pipeline-failure.sh"
  printf '%s\n' 'source "$1"' "printf 'input\n' | bash -c 'cat >/dev/null; exit 7'" 'printf "continued\n"' > "${script}"
  run bash "${script}" "${library}"
  [ "${status}" -eq 7 ]
  [ "${output}" = "ERROR: ${script}:2 exited with status 7" ]
}

@test "handled command condition does not trigger ERR" {
  script="${BATS_TEST_TMPDIR}/handled.sh"
  printf '%s\n' 'source "$1"' "if bash -c 'exit 7'; then" '  printf "unexpected\n"' 'else' '  printf "handled\n"' 'fi' > "${script}"
  run bash "${script}" "${library}"
  [ "${status}" -eq 0 ]
  [ "${output}" = "handled" ]
}

@test "function used as a condition has Bash conditional suppression" {
  script="${BATS_TEST_TMPDIR}/handled-function.sh"
  printf '%s\n' 'source "$1"' "fail() { bash -c 'exit 7'; }" 'if fail; then' '  printf "unexpected\n"' 'else' '  printf "handled\n"' 'fi' > "${script}"
  run bash "${script}" "${library}"
  [ "${status}" -eq 0 ]
  [ "${output}" = "handled" ]
}
