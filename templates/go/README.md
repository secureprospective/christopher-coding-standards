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
| Domain ID safety | Struct-wrapped `PlayerID` (`playerid/example.go`) | AD-06: the bypass `playerid.PlayerID("99")` fails to **compile** — validation/normalization can't be skipped |
| Empty-interface guard | `ifaceguard` vettool (`tools/ifaceguard/`) | `interface{}`/`any` in exported signatures — the boundary-typing gap **no golangci-lint linter covers** |
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
schema/example.go     →  internal/schema/   (boundary-validation pattern)
playerid/example.go   →  internal/playerid/playerid.go   (AD-06 struct-wrap; see below)
tools/ifaceguard/     →  tools/ifaceguard/   (custom analyzer — keep it a SEPARATE Go module)
```

Merge `Makefile.snippet`'s targets into your project Makefile. The `lint`
target now depends on `ifaceguard`, which builds the vettool from
`tools/ifaceguard/` on first run (`go build` into `tools/ifaceguard/bin/`,
gitignored) and runs it via `go vet -vettool`. No manual build step — `make
lint` and the pre-commit hook handle it.

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

Run this after adoption to confirm every gate fires. **Three of the gates are
not golangci-lint linters** — depguard's siblings still are, but AD-06 is
enforced by the *compiler* and `interface{}`/`any` by the *ifaceguard vettool* —
so the test has three parts. (All three were re-verified green→red on
2026-06-13, the Confidence-80 session T1 re-run — see `Fable_Friction_Log.md`.)

### Part A — golangci-lint gates

Create `internal/scratch/bad.go` with one violation per lint gate:

```go
package scratch

import (
	"database/sql"
	"fmt"
)

var cache = map[string]string{} // gochecknoglobals — package-level var

func DoWork(db *sql.DB, userInput string) {
	db.Exec("INSERT INTO log VALUES (1)")                                   // errcheck
	q := fmt.Sprintf("SELECT * FROM players WHERE name = '%s'", userInput)  // gosec G201
	db.Query(q)                                                             // errcheck
}
```

For depguard, add a file actually located under `internal/ingestion/` (it
matches by path) that imports `internal/engine` — a cross-layer violation.

```bash
make lint    # golangci-lint flags every case above; exits non-zero
```

### Part B — ifaceguard gate (`interface{}`/`any` escape, Friction #10)

```go
// internal/scratch/bad_iface.go
package scratch

func Anything(v interface{}) interface{} { return v }
```

`make lint` runs `ifaceguard` *before* golangci-lint; it must report BOTH the
parameter and the result and exit non-zero. **golangci-lint alone stays silent
on this case** — that silence is the entire reason ifaceguard exists
(`interfacebloat` only checks interface *declarations*, not bare `any` in a
signature). Confirm the escape hatch too: add `//ifaceguard:allow` to a
function's doc comment and verify ifaceguard then passes it.

### Part C — AD-06 bypass (compile-time, Friction #6)

```go
// internal/scratch/bad_bypass.go
package scratch

import "github.com/secureprospective/TheWarRoom/internal/playerid"

var bypass = playerid.PlayerID("99")
```

```bash
go build ./...    # must FAIL: cannot convert "99" to type playerid.PlayerID
```

This never reaches the linter — the struct-wrap makes the bypass a *compile*
error, the strongest enforcement in the overlay: code that cannot be built
cannot be committed.

If any gate stays silent (or the bypass compiles), **stop and fix the overlay
before B0** — a silent gate means the build ships that class of bug undetected
(companion plan T1 pass criteria). Delete `internal/scratch/` after.

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

## Resolved: AD-06 / RISK-003 enforcement — struct-wrapped `PlayerID` (Gate 1, 2026-06-13)

**Decision (Confidence-80 session, Gate 1): struct-wrap, compile-time
enforcement.** Background: the companion plan (Section 3.3) originally proposed
a `forbidigo` rule banning the conversion `playerid.PlayerID("0531")` outside
`internal/playerid`. That does not work — `forbidigo` with `analyze-types: true`
matches the qualified identifier wherever it appears, including as a **type
reference** in a signature (`func f() (playerid.PlayerID, error)`), not just as
a **conversion call**. forbidigo has no call-vs-type-position distinction, so
any pattern narrow enough to catch the bypass also bans using the type at all
(Friction #6). The forbidigo rule was removed.

**The fix in this overlay** is `playerid/example.go`: `PlayerID` is a struct
with an **unexported `id` field**.

```go
type PlayerID struct { id string }
func New(raw string) (PlayerID, error) { /* validate + zero-pad to 4 digits */ }
```

Because the field is unexported, `playerid.PlayerID("99")` from any other
package **fails to compile** ("cannot convert untyped string constant to type
playerid.PlayerID"). `New` is the only way to obtain a value, so validation and
leading-zero normalization ("99" → "0099") can never be skipped. JSON
round-trips through `New` (`UnmarshalJSON`), and DB persistence happens at the
store boundary via `String()`/`New(text)` rather than `driver.Valuer`/
`sql.Scanner` — so the package imports no `database/sql`, keeping it inside the
three-layer law (the depguard `sql-confined-to-data-layer` rule confirmed this:
an earlier draft that implemented `Scan`/`Value` was correctly rejected).

This converts a lint-time social contract into a compile-time guarantee — the
standard this repo holds itself to elsewhere. Verified by Part C of the
verification test above (the bypass fails `go build`).

---

## Resolved: `interface{}`/`any` escapes — the `ifaceguard` vettool (Gate 2, 2026-06-13)

**Decision (Confidence-80 session, Gate 2): a small custom `go/analysis`
vettool.** Background: T1 confirmed NO enabled golangci-lint linter catches a
bare `interface{}`/`any` parameter or return (Friction #10) — `interfacebloat`
only checks interface *declarations* with too many methods. A bare empty
interface at a layer boundary turns off the type checker there, and for a
project with hard "zero scoring leak" rules that is a silent correctness hole.

**The fix** is `tools/ifaceguard/` — a self-contained analyzer module that
flags `interface{}`/`any` (bare or nested in `*`, `[]`, `[N]`, `...`, `map`,
`chan`) in the signatures of **exported** functions and methods only (an
unexported helper using `any` internally is not a boundary escape). It is run
as a vettool via `go vet -vettool`, wired into `make lint` and pre-commit.

- **Escape hatch:** a deliberate, legitimate empty-interface boundary (a generic
  marshalling helper, a `sql.Scanner.Scan(any)` implementation in the store
  layer) is suppressed with an `//ifaceguard:allow` directive in the function's
  doc comment. The directive is tool-specific so it can't be confused with
  `//nolint` or `//lint:ignore`.
- **Supply chain:** `ifaceguard` depends only on `golang.org/x/tools`, pinned by
  explicit version in `tools/ifaceguard/go.mod` with its hash locked in
  `go.sum` (committed). Re-pin to a new explicit version and re-commit `go.sum`
  to bump; never a mutable ref. Because the analyzer is our own code, it carries
  the same caution as any custom linter (Friction #8's depguard-glob lesson): a
  bug could make it silently not fire, so its `analysistest` suite
  (`ifaceguard_test.go` + `testdata/`) is the regression guard and must pass in
  CI before the overlay is trusted.

Verified by Part B of the verification test above (an exported `interface{}`
signature fails `make lint`; `//ifaceguard:allow` clears it).

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
