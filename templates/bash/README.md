# Bash Overlay — Adoption Guide

Part of `christopher-coding-standards`, Phase 2 (final overlay). Companion to
the TypeScript, Go, and Python overlays — same role, Bash-specific tooling.
Model-agnostic and reusable by any project with a `scripts/`/`bin/` tree of
shell scripts (deploy scripts, cron jobs, CI glue — the kind of code that
tends to accumulate outside a "real" language's guardrails).

---

## What this overlay adds

| Layer | Tool | What it enforces |
|---|---|---|
| Linter | shellcheck 0.9+ (`.shellcheckrc` curates the optional-check set) | Correctness bugs (unquoted expansion, unused vars, wrong test operators) and a handful of SAST-adjacent checks |
| Formatter | shfmt | Consistent indentation, `case` styling, redirect spacing |
| Pre-commit hooks | pre-commit + shellcheck + shfmt + gitleaks | Blocks commits with lint/format failures or secrets |
| Boundary validation | `lib/strict-mode.sh` (`require_arg`, `require_positive_int`) | No script proceeds on an empty/malformed input — the Bash analogue of the Go/Python/TS overlays' schema validation |
| Test discipline | bats-core | Unit + integration tests for shell functions and scripts |

**Why shellcheck's curated set, not `enable=all`:** the same reasoning as the
Go overlay's `linters: default: none` — `enable=all` includes a long tail of
style-opinionated optional checks with real false-positive noise. This
overlay enables five specific high-value ones (see `.shellcheckrc` for the
rationale on each) rather than everything.

---

## Adoption steps

### 1. Install the toolchain

```bash
# Debian/Ubuntu — apt ships current-enough versions of all three:
sudo apt-get install shellcheck shfmt bats
shellcheck --version   # verified against 0.9.0
shfmt --version         # verified against 3.6.0
bats --version          # verified against 1.8.2

pip install pre-commit  # if not already installed
```

**pre-commit version matters here:** the `shfmt` hook's manifest uses the
modern `stages: [pre-commit]` name. **pre-commit < ~3.2 rejects this with
`InvalidManifestError`** (confirmed 2026-07-24 against pre-commit 3.0.4).
Upgrade with `pip install --upgrade pre-commit` if you hit that error.

### 2. Copy files into your repo root

```
.shellcheckrc
.pre-commit-config.yaml
Makefile.snippet     →  merge targets into your project Makefile
lib/strict-mode.sh   →  keep as lib/strict-mode.sh (or your project's shared-lib location)
scripts/example.sh   →  reference only — shows the adoption pattern, not meant to ship as-is
tests/example.bats   →  reference only — same
```

### 3. Adopt the strict-mode pattern in every script

Every script should start:

```bash
#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/strict-mode.sh
source "${here}/lib/strict-mode.sh"
```

Then validate every argument/env var before using it:

```bash
require_arg "config_path" "${1:-}"
require_positive_int "port" "${2:-}"
```

### 4. Activate pre-commit hooks

```bash
pre-commit install
```

### 5. Re-pin hook SHAs if you bump versions

```bash
git ls-remote https://github.com/shellcheck-py/shellcheck-py v0.11.0.1
git ls-remote https://github.com/scop/pre-commit-shfmt v3.13.1-1
git ls-remote https://github.com/gitleaks/gitleaks v8.30.1
```

Replace the `rev:` values in `.pre-commit-config.yaml` with the full
40-character SHA. Never use a mutable tag (`@v1`, `@latest`) — the
trivy-action lesson (AGENTS.md hard rule).

---

## Verification test — deliberate violations

Run this after adoption to confirm every gate fires. Verified live against
the real tools during this overlay's build (shellcheck 0.9.0, shfmt 3.6.0,
gitleaks — full `pre-commit run`, not just standalone CLI output).

**Step 1:** Create `scripts/scratch_bad.sh` with one violation per gate:

```bash
#!/bin/bash
name=$1
echo Hello $name                          # shellcheck SC2086/SC2250 — unquoted expansion
password="hunter2hunter2hunter2"          # shellcheck SC2034 — assigned but unused
eval "echo $name"                         # shellcheck SC2250
aws_key="AKIAABCDEFGHIJKLMNOP"            # gitleaks — AWS access key pattern
if [ $name = "" ]
then
echo empty                                # shfmt — missing indent, `if/then` not collapsed
fi
```

(Do not use AWS's own documented example key `AKIAIOSFODNN7EXAMPLE` — every
overlay in this repo's gitleaks setup allowlists it by design as a known
false-positive. Any other `AKIA`-prefixed 20-char string will trigger.)

**Step 2:** Try to commit it:

```bash
git add scripts/scratch_bad.sh
git commit -m "test: verify gates"
```

**Expected — all three must fire:**
- shellcheck flags the unquoted expansions and the unused variable →
  pre-commit blocks the commit
- shfmt rewrites the `if`/`then`/indent block → pre-commit blocks the
  commit (`files were modified by this hook`)
- gitleaks flags the AWS key → pre-commit blocks the commit
- `make lint` exits non-zero standalone (not just inside pre-commit)

If any gate stays silent, stop and fix the overlay before trusting it in
production.

**Step 3:** Delete `scripts/scratch_bad.sh` and proceed.

**A note on the shfmt hook config** (found during this overlay's build): the
`shfmt` pre-commit hook's *default* args are `[--write]`. This overlay's
`.pre-commit-config.yaml` passes a custom `args:` list to set the indent/
style flags (`-i 2 -ci -sr`) — and a custom `args:` list **replaces** the
default rather than merging with it. The first draft of this overlay omitted
`-w`/`--write` from the custom list, which silently turned the hook into a
no-op: no diff, no fix, no failure, `Passed` on a misformatted file. Fixed by
including `-w` explicitly (see the comment in `.pre-commit-config.yaml`).
Caught only by running the deliberate-violation test through the actual
pre-commit hook, not by reading the config — the same lesson the Python
overlay's session-notes entry drew from the AWS-example-key mistake:
templates need to be run, not just written.

---

## Test discipline — bats-core

```bash
make test   # bats tests/
```

`tests/example.bats` demonstrates both unit-level tests (sourcing
`lib/strict-mode.sh` directly and calling `require_arg`/`require_positive_int`)
and integration-level tests (`run`-ing `scripts/example.sh` end to end and
asserting on `$status`/`$output`). All 9 assertions pass live against the
example files in this directory.

`.bats` files are excluded from the shellcheck/shfmt lint target — bats'
`@test "..." { }` syntax isn't plain bash, and shellcheck false-positives on
bats-runtime-injected variables (`BATS_TEST_DIRNAME`, `run`, `$status`,
`$output`). They're validated by `bats` itself, not the linter.

---

## Phase status

- ✅ Phase 1A — repo skeleton
- ✅ Phase 1B — language-agnostic templates
- ✅ Phase 1C — TypeScript overlay
- ✅ Phase 1D — Astro overlay
- ✅ Phase 2 — Go overlay
- ✅ Phase 2 (cont.) — Python overlay
- ✅ Phase 2 (cont.) — Bash overlay (this directory) — **Phase 2 complete**
- ⏳ Phase 3 — local-model selection guidance, dual-model architecture doc
