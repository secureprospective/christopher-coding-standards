# Go — explicit boundaries and selected tools

Adopt the [core contract](../../docs/quality-contract.md), preserving consumer rules. Current acceptance follows [HANDOFF](../../HANDOFF.md), not historical phase/project claims.

## Compose deliberately

- Select compatible Go/golangci-lint/native Gitleaks/pre-commit versions and verify provenance/integrity before running. Tested reference Go1.27.2/golangci2.14.0; this is not a mandate to upgrade existing applications. The linter must support the selected Go language/toolchain. Do not disable checksums or implicitly download a new Go SDK; set appropriate local toolchain policy during bounded verification.
- Merge `.golangci.yml`, hooks and Make targets with local rules. Default checks cover selected correctness/security analyzers and blank unchecked errors, not blanket complexity/global-variable/purity/DAG quotas. Local linter hook uses the owner's verified installed binary; immutable native Gitleaks-system avoids a separate Go bootstrap. Pins/locks/hooks are not authenticated approval, isolation or complete safety.
- Copy `schema/` and `playerid/` patterns into owner-selected packages. Read the domain rules: one non-null JSON object, tolerate provider unknown fields, validate required fields/finite numeric salary, then construct/normalize domain identifiers **before effects**. Owned clients may require a different unknown-field policy. Validation and a valid role/ID do not grant application permission. Reader/body limits, error redaction, persistence and authorization belong to the consumer.
- PlayerID is an example unsigned ASCII decimal protocol, trimmed and zero-padded to at least four digits, retaining platform-int range checks. Zero numeric ID is allowed; zero **struct value** is invalid and rejects JSON encoding. Direct string conversion does not compile, but zero values/empty literals still exist: New is not an unbypassable validation guarantee. JSON decoding validates through New and rejects without overwriting the receiver. Store canonical strings/validate reads deliberately; no database integration supplied.
- Generic build is `go build ./...`; retain a real application's Wails/server/etc build separately. Race-enabled tests need a supported platform/compiler; passing observed executions do not prove race-freedom. Coverage output is a selected reference floor, not correctness. `go test` with no test files is not meaningful verification: inspect actual discovery/cases.

```sh
go mod tidy             # deliberate dependency initialization/update
go mod verify           # observed module cache integrity, not authenticated approval
make lint
make format-check
make vet
make test
make test-coverage
make build
```

Review/commit consumer go.mod/go.sum; routine commands should not silently repair a stale lock. Configure frozen/read-only module policy explicitly. Coverage writes `coverage.out` and `coverage-summary.txt`; malformed/absent summary, invalid threshold and tool/test failure reject, not empty-as-zero/arbitrary-green. Default reference threshold80 may be deliberately adapted with rationale, not treated as a quality score.

## Optional policies, not universal bans

`tools/ifaceguard` is a separate pinned Go module for an owner-selected exported-signature policy. It reports selected bare/nested empty interfaces in exported function/method parameters/results; legitimate any boundaries and generic APIs exist. Read actual analyzer scope/tests and documented allow directive. Copy only if needed, keep module/sum/source together, then `make ifaceguard`; target rebuilds each invocation before vet, avoiding stale source/sum/toolchain binaries. The tested Unix recipe uses a fresh private space-free /tmp binary and cleanup: selected x/tools emits an absolute executable path that Go cannot parse if it contains spaces. This is not a noexec-/tmp/other-platform guarantee or authority to change permissions. Actual analyzer regression/good/bad/allow tests are needed before promising enforcement. Neither it nor a lint result authenticates policy compliance or prevents malicious bypass.

`bloat.sh` keeps a legacy filename but is now a **physical source inventory**, not a comment-share/tiny-file/duplicate ratchet. Copy to scripts/bloat.sh if useful; `make bloat` reports regular non-test Go files and fails missing discovery/I/O/traversal rather than suppressing analyzer errors. No baseline-update mode. It counts, not measures tokens/quality or demands splitting. Project-specific depguard/import rules may be merged with actual module/path identities and diagnostic probes; this generic kit no longer pretends TheWarRoom/Wails layers are every Go application's law.

Optional mutation testing needs a selected, installed/configured/exercised tool and source/runtime scope. The previously unexecuted gremlins wrapper is not a default correctness claim or automatic remote-code authorization; no generic mutation target promised here.

## Exercise real checks

Use a disposable authorized consumer. Call shipped decoder/validator/ID methods and a small actual/synthetic caller, covering valid/invalid/trailing/null input, unknown fields, finite numeric limits, constructor/JSON normalization/failed decode state and zero values. Require rejection before the caller's effect. Introduce one blank unchecked error and require errcheck's diagnostic (no nolint suppression); introduce an intended failing assertion/format violation and restore. For selected ifaceguard, test actual exported bad/good/allow signatures and normal typed interfaces/containers. Exercise installed read-only hooks and ordinary clean commit, not a simulated passing echo.

Other applications/platforms, complete SAST/secret detection, containment, concurrency safety, deployed/hosted enforcement and live consumer adoption are unverified by this reference. No publication, hosted protection change, push/main merge/deploy or fleet rollout follows.
