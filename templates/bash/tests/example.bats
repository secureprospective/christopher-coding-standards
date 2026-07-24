#!/usr/bin/env bats
# shellcheck disable=SC2154 # BATS_TEST_DIRNAME etc. are injected by the bats
# runtime, not assigned in this file — shellcheck can't see that. `.bats`
# files are exempt from the lint target below for the same reason (bats'
# `@test "..." { }` syntax isn't plain bash); they're validated by `bats`
# itself, not shellcheck/shfmt.
#
# Test discipline example — the Bash overlay's analogue of the TS overlay's
# Vitest suite / Go overlay's `go test -race`. Exercises lib/strict-mode.sh
# directly (unit-level) and scripts/example.sh end to end (integration).

setup() {
  # shellcheck disable=SC1091
  source "${BATS_TEST_DIRNAME}/../lib/strict-mode.sh"
}

@test "require_arg fails on empty value" {
  run require_arg "foo" ""
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"missing required argument: foo"* ]]
}

@test "require_arg fails on unset value" {
  run require_arg "foo"
  [ "${status}" -eq 1 ]
}

@test "require_arg passes on non-empty value" {
  run require_arg "foo" "bar"
  [ "${status}" -eq 0 ]
}

@test "require_positive_int rejects non-numeric" {
  run require_positive_int "port" "abc"
  [ "${status}" -eq 1 ]
  [[ "${output}" == *"must be a positive integer"* ]]
}

@test "require_positive_int rejects empty value" {
  run require_positive_int "port" ""
  [ "${status}" -eq 1 ]
}

@test "require_positive_int accepts numeric" {
  run require_positive_int "port" "8080"
  [ "${status}" -eq 0 ]
}

@test "example.sh fails with no arguments" {
  run "${BATS_TEST_DIRNAME}/../scripts/example.sh"
  [ "${status}" -eq 1 ]
}

@test "example.sh fails with a non-numeric port" {
  run "${BATS_TEST_DIRNAME}/../scripts/example.sh" "not-a-port"
  [ "${status}" -eq 1 ]
}

@test "example.sh succeeds with a valid port" {
  run "${BATS_TEST_DIRNAME}/../scripts/example.sh" 8080
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"Starting on port 8080"* ]]
}
