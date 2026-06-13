# Go Overlay — Adoption Guide

Part of `christopher-coding-standards`, Phase 2. Companion to the
TypeScript (Phase 1C) and Astro (Phase 1D) overlays — same role, Go-specific
tooling. Written for TheWarRoom (AD-19: this overlay is the critical-path
prerequisite for B0) but model-agnostic and reusable by any Go project
adopting the standard.

---

## What this overlay adds

| Layer | Tool | What it enforces |
|---|---|---|
| Formatter | `gofmt` + `goimports` | Standard Go formatting, import grouping |
| Linter | golangci-lint v2 (`gosec`, `errcheck`, `staticcheck`, `depguard`, `gochecknoglobals`, …) | Security, correctness, and the three-layer architecture as build errors |
| Pre-commit hooks | pre-commit + golangci-lint + gitleaks | Blocks commits with lint failures or secrets |
| Boundary validation | Hand-written `Validate() error` (`schema/example.go`) | No struct-tag reflection; compile-time-safe parsing of MFL JSON |
| Test discipline | `go test -race` + coverage threshold | Concurrency bugs caught at commit time, not in production |
| Mutation testing | `gremlins` (scoped to `internal/engine/...`) | Proves tests assert, not just execute |

---

## Adoption steps

### 1. Install the toolchain

```bash
# Go 1.26+ (this overlay was built and verified against go1.26.4)
# golangci-lint v2.12.2, pre-commit, gitleaks v8.30.1
golangci-lint version   # should print "golangci-lint has version 2.12.2 ..."
pre-commit --version
gitleaks version
```

**If `golangci-lint`'s own `install.sh` fails checksum verification for
v2.12.2/linux-amd64** — this is a confirmed bug in the script as of
2026-06-13 (it compares the tarball's hash against the `.sbom.json`
checksum entry, not the tarball's own entry). Work around it by downloading
the release asset and `golangci-lint-2.12.2-checksums.txt` directly and
verifying with `sha256sum -c`, then extracting the binary manually. Do not
disable checksum verification.

### 2. Copy files into your repo root

```
.golangci.yml
.pre-commit-config.yaml
schema/example.go   →  internal/schema/ (or your boundary-validation package)
```

Merge `Makefile.snippet`'s targets into your project Makefile.

### 3. Confirm the module path in `.golangci.yml`

The `depguard` rules are **pre-written for TheWarRoom's `internal/` tree**
(companion plan `Fable_TheWarRoom_code_plan.md`, Section 3.1) assuming module
path `github.com/secureprospective/TheWarRoom`. At B0, confirm `go.mod`'s
`module` line matches. If it differs, find/replace the prefix across every
`deny: pkg:` entry in `.golangci.yml` — `depguard` matches import paths by
exact prefix, so a mismatched module path means **the rules silently never
fire**. Verify with the deliberate-violation test (below) after any change.

### 4. Activate pre-commit hooks

```bash
pre-commit install
```

### 5. Re-pin hook SHAs if you bump versions

```bash
git ls-remote https://github.com/golangci/golangci-lint v2.12.2
git ls-remote https://github.com/gitleaks/gitleaks v8.30.1
```

Replace the `rev:` values in `.pre-commit-config.yaml` with the full
40-character SHA. Never use a mutable tag (`@v1`, `@latest`) — the
trivy-action lesson (AGENTS.md hard rule).

---

## Verification test — deliberate violations

Run this after adoption to confirm every gate fires. Create
`internal/scratch/bad.go` (any throwaway package) with **one violation per
gate**:

```go
package scratch

import (
	"database/sql"
	"fmt"
)

// 1. gochecknoglobals — package-level var.
var cache = map[string]string{}

// 2. errcheck — unchecked error.
func DoWork(db *sql.DB, userInput string) {
	db.Exec("INSERT INTO log VALUES (1)")

	// 3. gosec (G201) — SQL built by string concatenation.
	q := fmt.Sprintf("SELECT * FROM players WHERE name = '%s'", userInput)
	db.Query(q)
}

// 4. depguard — cross-layer import violation (see "AD-06" note above for why
// there is no forbidigo rule for playerid.PlayerID(...) bypass conversions;
// that is a compile-time concern for B0, not a lint-gate item here).

// 5. gocritic / interfacebloat — interface{} escape.
func Anything(v interface{}) interface{} { return v }
```

Then:

```bash
make lint        # must exit non-zero
git add internal/scratch/bad.go
git commit -m "test: verify G0 gates"   # pre-commit must block this
```

**Expected — every gate fires:**
- `gochecknoglobals` flags `var cache`
- `errcheck` flags the unchecked `db.Exec` / `db.Query`
- `gosec` (G201/G202) flags the `fmt.Sprintf`-built query
- `depguard` flags the cross-layer import violation
- `gocritic`/`interfacebloat` flags the `interface{}` parameters and return
- `gitleaks` would flag any hardcoded credential added alongside these
- `make lint` exits non-zero; `git commit` is blocked by the pre-commit hook

If any gate stays silent, **stop and fix the overlay before B0** — a silent
gate means the build ships that class of bug undetected (companion plan T1
pass criteria).

Delete `internal/scratch/` after verification.

---

## Known exception: `gochecknoglobals` and sentinel errors

`gochecknoglobals` (v2.12.2) has **no configuration options** — it flags
every package-level `var`, with no built-in exception for `var ErrFoo =
errors.New("...")`. This is the idiomatic Go sentinel-error pattern, and the
companion plan's own skeletons (Section 4, WF 6: `ErrInsufficientCap`) use
it.

**Resolution:** sentinel errors are the one documented exception. Declare
them as package-level `var` with an explicit `//nolint:gochecknoglobals —
sentinel error, compared via errors.Is` comment. Every other package-level
`var` (caches, config, mutable state — the actual failure mode this linter
targets) has **no exception** and fails the build. A weaker model adding a
`//nolint` for anything other than a sentinel error is a code-review finding,
not a config problem.

---

## Known limitation: AD-06 / RISK-003 enforcement (`playerid.PlayerID` bypass conversion)

**Confirmed 2026-06-13 by empirical baseline test.** The companion plan
(Section 3.3) proposed a `forbidigo` rule banning the conversion expression
`playerid.PlayerID("0531")` everywhere outside `internal/playerid` itself, to
stop callers bypassing the validating constructor `playerid.New()`.

This does not work. `forbidigo` with `analyze-types: true` matches the
qualified identifier `playerid.PlayerID` wherever it appears in the AST —
including as a **type reference** in a function signature
(`func ValidateRawID(raw string) (playerid.PlayerID, error)`), not just as a
**conversion call** (`playerid.PlayerID(raw)`). forbidigo has no
call-vs-type-position distinction. A pattern narrow enough to catch the
bypass conversion also bans using `playerid.PlayerID` as a type anywhere
outside its own package — which is the entire point of the type (AD-06:
"every domain struct uses `playerid.PlayerID` ... for an ID field"). This
rule has been **removed** from `.golangci.yml`.

**This is a real enforcement gap, not just a config problem.** Options for
B0, in order of preference:

1. **Struct-wrap (recommended, the plan's own "heavier alternative")** —
   `type PlayerID struct { id string }` with an unexported field. A bare
   `playerid.PlayerID("0531")` conversion from outside the package then fails
   to *compile* (you cannot convert a string to a struct type), so the
   bypass is closed at the type-checker level — no linter needed. Costs:
   every legitimate use must go through `New()` or an accessor method
   (`.String()`); slightly more ceremony than a string newtype.
2. **Custom `go/analysis` checker** — a purpose-built analyzer that walks
   `*ast.CallExpr` nodes specifically (not all expressions) and flags only
   conversion-call sites. More precise than forbidigo but is new code to
   write, test, and maintain — disproportionate for one rule.
3. **Code-review item, no tooling** — accept the gap, call it out explicitly
   in PR review checklists. Weakest option; relies on a human (or agy) catching
   it every time.

Recommend (1) for B0 — it converts a lint-time social-contract rule into a
compile-time guarantee, which is the standard this repo holds itself to
elsewhere (Section 3.2's StateReader/StateWriter write-lockout idiom is the
same move). Flag this to Christopher before B0 closes; it changes
`internal/playerid`'s public API shape from the Section 3.1/3.3 skeleton as
currently written.

---

## Errata: Section 4 WF 1B skeleton — unwrapped error return fails `wrapcheck`

**Confirmed 2026-06-13 by empirical baseline test.** The companion plan's WF
1B skeleton (Section 4) has the pattern:

```go
func validatePlayerID(raw string) (playerid.PlayerID, error) {
    return playerid.New(raw)
}
```

`wrapcheck` (default config, no exemptions added — see "What this overlay
adds") flags this: `playerid.New`'s error is returned directly across a
package boundary without `fmt.Errorf("...: %w", err)`. This is not a config
bug — `internal/playerid` and `internal/ingestion` are different packages,
and per-layer error context (which package/operation failed) is exactly what
`wrapcheck` is for. Section 3.3's own `normalize.Roster` example already
wraps correctly (`fmt.Errorf("normalize roster: %w", err)`); WF 1B's skeleton
is the inconsistent one.

**Resolution — update the WF 1B skeleton** to:

```go
func validatePlayerID(raw string) (playerid.PlayerID, error) {
    id, err := playerid.New(raw)
    if err != nil {
        return "", fmt.Errorf("ingestion: validate player id: %w", err)
    }
    return id, nil
}
```

No `.golangci.yml` change needed — `wrapcheck`'s defaults are correct as
configured. The companion plan's skeleton text should be corrected before B0
so a weaker model copying it verbatim doesn't inherit a lint failure on day
one.

---

## modernc.org/sqlite DSN syntax (Section 3.4 open item — resolved)

`modernc.org/sqlite` uses `_pragma=` parameters, **not** `mattn/go-sqlite3`'s
`_busy_timeout=` / `_journal_mode=` style:

```go
db, err := sql.Open("sqlite",
    "file:thewarroom.db?_pragma=busy_timeout(5000)&_pragma=journal_mode(WAL)&_txlock=immediate")
```

- `_pragma=<name>(<args>)` — each one becomes a `PRAGMA <name> <args>;`
  statement. Repeatable, `&`-separated.
- `_txlock=immediate` is accepted by the driver's connector for the write
  pool (`SetMaxOpenConns(1)`).

Confirmed against `pkg.go.dev/modernc.org/sqlite` 2026-06-13. Still verify
with the concurrency bench (companion plan Section 3.4) before blessing the
split-pool pattern — DSN syntax being correct does not guarantee the WAL
pragma is actually applied on the read pool under load.

---

## Mutation testing — `gremlins`

**Viability check, 2026-06-13:** `go-gremlins/gremlins` — latest release
`v0.6.0` (2025-12-06), repo pushed as recently as 2026-06-12, not archived.
**Verdict: viable, not deferred.** Pin to `v0.6.0` (Makefile target below);
re-check for a newer tag at B0.

```bash
make mutation-test   # go run github.com/go-gremlins/gremlins/cmd/gremlins@v0.6.0 unleash ./internal/engine/...
```

Scoped to `internal/engine/...` per the agy Go-architect recommendation
(companion plan Section 8B) — pure-logic packages are where a mutation score
has signal; I/O-heavy packages mostly produce noise.

**Not executed live in this session** — running a pinned third-party
`go run module@version` is an autonomous external-code-execution action that
this sandbox's permission policy requires explicit per-action authorization
for. Logged as friction; run it manually once, then it's cached locally.

---

## Phase status

- ✅ Phase 1A — repo skeleton
- ✅ Phase 1B — language-agnostic templates
- ✅ Phase 1C — TypeScript overlay
- ✅ Phase 1D — Astro overlay
- ✅ Phase 2 — Go overlay (this directory)
- ⏳ Phase 3 — local-model selection guidance, dual-model architecture doc
