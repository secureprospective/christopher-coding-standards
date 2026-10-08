# C0 — current gate baseline and verification limits

Owner: Bee. Date: 2026-10-08. This is source inspection, not new runtime/hosted enforcement proof.

## Candidate and inspection boundary

Implementation branch: `rebuild/quality-core-2026-10-08`; base HEAD `69e0658dcb5ff45806eb048dcaf7207df684d9f5`. Main is not modified. Existing `.project.yaml` is outside scope.

`c0-source-fingerprints.json` records 95 tracked source/config/fixture/instruction files, byte sizes and SHA256 values. At inspection, every recorded working file equaled its committed HEAD blob. It also records root-file/hook presence and all 18 workflow action references. Fingerprints establish inspected bytes, not trust or adoption.

Inspection used file reads, `git ls-files`, `git show HEAD:<path>`, `git rev-parse`, `git config --get core.hooksPath`, and standard-library metadata/JSON processing. No package installation, shipped script execution, product test, hook trigger, scanner run, VM launch or hosted API change occurred. C0 structural/link/fingerprint checks are document-integrity checks, not feature tests.

## Root local enforcement: observed, not inferred from templates

| Surface | Observed at this candidate | Consequence |
|---|---|---|
| Root `Makefile`, `package.json`, `.pre-commit-config.yaml` | Absent | Root `make lint/test` or package scripts are not executable project gates merely because AGENTS lists them. Do not run imaginary commands or count absent hooks as passing. |
| Default Git `hooks/pre-commit` | Absent; resolved via `git rev-parse --git-path hooks/pre-commit` | No repository Git pre-commit hook observed at the default location. This says nothing about external agent/runtime controls. |
| Effective `core.hooksPath` | No configured value returned | No alternate Git hook location discovered through this setting. Not evidence that every possible tool/runtime gate is disabled. |
| Root `biome.json`, `vitest.config.ts`, `astro.config.*` | Absent | Current security workflow's root-presence conditions select out substantive TS/Astro work. Configs under `templates/` do not satisfy those root probes. |
| `AGENTS.md`, `SYSTEM_MAP.md` | Kit root contains copy/customize placeholders and example utilities/services | These are not an accurate active-project profile/map. C1 must distinguish kit-maintenance instructions from shipped consumer templates and avoid phantom paths/commands. |
| `.claude/settings.json` | Tracked vendor settings exist | Configuration is not observed effective containment. No permission/bypass/sandbox test executed. Current user/developer guardrails remain live regardless. |

## Repository CI: configured source versus actual historical execution

All four workflows trigger on PRs to main/develop and pushes to main; `security.yml` additionally schedules weekly. A push to this implementation branch alone is not evidence they ran. No new hosted run was requested.

| Workflow / job | Source-configured work | Evidence/limit |
|---|---|---|
| `.github/workflows/security.yml`: `secrets — gitleaks` | Full-history checkout + Gitleaks action | Historical Oct8 audit observed success at main `93ee82a…`; no new scanner execution. `.gitleaks.toml` excludes README and docs Markdown broadly; success cannot prove those docs secret-free. |
| Same: `sast — semgrep` | `p/security-audit`, `p/secrets`, `p/owasp-top-ten` | Historical success only. Mutable action/ruleset sources do not establish immutable scanner identity or complete coverage. |
| Same: `sca — trivy` | Filesystem scan, CRITICAL/HIGH, ignore-unfixed; SARIF upload | Historical success only. This configuration excludes medium-severity findings and unfixed advisories; cannot claim every dependency risk was checked. |
| Same: `ts — lint`, `ts — test` | Root config probes; Node22/npm-ci/Biome/tsc/Vitest steps conditional on those probes | Root markers absent at inspected candidate. Historical exact-main job steps already showed substantive work skipped despite green conclusions. C12 must replace false-positive success with applicable real checks, not describe green as verification. |
| Same: `astro — check` | Root astro-config probe; conditional astro/prettier commands | Root config absent. Source-traced skip condition; no new step execution observed. |
| `.github/workflows/verify-templates.yml`: Python fixtures | Copies shipped pyproject snippet and clean/violating fixtures; installs matching Ruff/mypy versions; scans with Gitleaks | Historical job/steps success observed at audited main. Does not execute pytest, coverage, mutation or Pydantic integration. Trap suppresses diagnostics and accepts any nonzero Ruff/mypy exit: cannot prove intended diagnostic rather than arbitrary error. |
| `.github/workflows/verify-templates-go.yml`: Go fixtures | Copies `.golangci.yml` + fixtures, builds actual ifaceguard module, runs lint/vet/Gitleaks | Historical job/steps success observed. Does not establish full adopted-project build/test/race/mutation/bloat behavior. Negative lint/vet trap likewise accepts any nonzero exit without proving the reason. |
| `.github/workflows/verify-templates-bash.yml`: Bash fixtures | Installs matching tools, copies clean/violating shell fixtures, runs ShellCheck/shfmt/Gitleaks | Historical job/steps success observed. Does not execute Bats or test boundary helpers. Negative ShellCheck/shfmt trap suppresses diagnostics and accepts any nonzero error. Source job does not surface the template `.shellcheckrc`. |

Action refs: **18 uses, 12 not full commit SHAs**, freshly counted from source in the fingerprint artifact. Security workflow grants `security-events: write` at workflow scope; fixture workflows grant only `contents: read`. Binary-download/checksum/ruleset trust gaps identified in retained audit remain relevant; no dependency identity/fetch verification was rerun here.

Historical hosted findings are preserved in `evidence/github-settings-and-ci-evidence.json` and `canonical-github-authority-audit-2026-10-08.md`: five required contexts, strict base/admin enforcement, zero required approving reviews; actual fixture jobs not required. Those findings concern main `93ee82a…` as audited October8, not current hosted state or this uncommitted C0 candidate. No assumption of changed protection or new publication authority.

## Seven overlay command contracts and coverage gaps

These commands are **shipped interfaces to inspect/test in the designated suitable VM later**, not results. They require assembled consumer projects, tool installations and actual fixture inputs. Do not execute deployment targets as validation.

| Overlay | Shipped source / command contracts | Unproven or source-visible gap; owning chunk |
|---|---|---|
| Bash | `templates/bash/Makefile.snippet`: lint = ShellCheck + shfmt; test = `bats tests/`. Hook config excludes Bats files. | Source `require_positive_int` accepts regex `^[0-9]+$`, which includes zero; a digit-only shape check is not positivity. Bats/helper paths not covered by current hosted fixture job. C4 must prove boundary behavior with actual tests and intended diagnostics. |
| TypeScript | `templates/typescript/Makefile` / package snippet: pnpm lint, typecheck, test, test:coverage; Stryker mutation targets. | No TS fixture workflow. Root security-job success skips real gates. Shipped Vitest/coverage `^3` cannot receive the retained advisory's stable fixed4.1.11 version; advisory/version/support facts must be freshly checked before C5 implementation. No install/coverage/Stryker compatibility exercise here. |
| Workers | Base TS merge + Workers package/vitest/wrangler configs; `wrangler types && tsc --noEmit`, Vitest in worker runtime. | Overrides to Vitest/coverage4.1 and old pool integration need compatibility/current official tooling verification. No hosted Worker fixture exists. Do not change compatibility dates casually or run `wrangler deploy`. C6. |
| Astro | Base TS merge + Astro package/Makefile/pre-commit snippets; prettier check `.astro`, `astro check`. | Root job skips. No base/non-React versus optional-React assembly/generated-type/formatter exercise. C7. |
| Bun/ECS | `bun run lint/typecheck/test`, dependency cruise, file-length/component checks, `check:all`. | Hard300-line cap conflicts with responsibility-first direction. Purity checker detects class declarations, method signatures and function-type property signatures—not full JSON serializability or absence of all behavior/state hazards. No Bun/ECS hosted fixture. C8. |
| Go | Makefile includes ifaceguard + filelen + bloat + golangci-lint; vet, `go test -race`, coverage, Wails build, engine-scoped Gremlins. | Fixture CI covers only subset. Makefile tool dependency list omits go.sum, although the tool's go.sum exists. Project-specific Wails/engine paths, bloat failure behavior and trailing-JSON handling need actual verification/narrowing. C9. |
| Python | Makefile lint/typecheck/test/coverage/pip-audit; mutmut command `run --paths-to-mutate=src/`. Strict mypy/pytest/Ruff/coverage config in snippet. | Fixture CI covers only selected lint/type vectors. Retained proposal questions current mutmut CLI/config and Pydantic typing support; command compatibility not established here. C10. |

No universal mutation test/race/coverage/file quota is adopted by this baseline. Current template commands are inventory, not a recommendation to preserve unjustified requirements. Existing quality/safety guarantees must be assessed before changing policy or weakening a gate.

## Initial failures/unknowns and disposition

- **Source-visible:** root project placeholders/phantom map; mandatory-context skip conditions; mutable action refs/broad privileges/exclusions; arbitrary-error negative traps; zero accepted by positive-integer helper; Bun hard cap and overbroad purity implications. These are not reported as newly reproduced runtime failures. Their appropriate chunks own repairs.
- **Historical execution:** audited main jobs/steps are retained evidence only, not current C0 test results.
- **Unverified:** suitable test VM availability/ownership; exact executable tool identities and downloads; all complete overlay installs/builds/behavior/coverage/mutation; actual containment; current hosted policy/job conclusions; live consumers.
- **C0 allowed checks:** authored Markdown structure/references, fixture IDs/oracle coverage, exact source/candidate fingerprints, diff scope and independent scenario/source review. No actual application behavior pass is claimed.
- **Later gate failure:** capture exact command/diagnostic and candidate; distinguish pre-existing behavior, candidate defect, tool setup and stale/flaky evidence. An inherited failure stays visible; fixing unrelated history is not demanded by C0. No silent suppression, fake negative pass or test weakening.

The applicable acceptance baseline is the operator-approved six-dimensional draft plus chunk plan; existing ADR history remains intact. C1 must make migration/superseding rationale explicit rather than treating unimplemented drafts as already-live enforcement.
