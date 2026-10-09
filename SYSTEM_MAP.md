# Standards kit map

This map describes the actual kit, not example application directories. Update relevant entries when artifacts/responsibilities change; mark uncertainty rather than inventing utilities.

| Path | Responsibility |
|---|---|
| `AGENTS.md`, `docs/INDEX.md` | Kit-maintenance instructions and task routing. |
| `docs/quality-contract.md` | Shared six-dimensional acceptance contract; portable to consumers. |
| `docs/architecture-review.md` | Optional task-scoped component/data-flow and preserving-debloat method; no engine or automatic refactor. |
| `templates/AGENTS.md`, `templates/SYSTEM_MAP.md` | Consumer instruction/map starting points, customized to actual project facts. |
| `templates/typescript/` | Base TS configs/snippets and schema example. |
| `templates/astro/`, `templates/cloudflare-workers/`, `templates/bun-ecs/` | Selected additive/specialized TS overlays; their READMEs define merge/runtime particulars. |
| `templates/go/`, `templates/python/`, `templates/bash/` | Language configs, examples and command interfaces. Go includes the existing ifaceguard analyzer; Bash includes strict-mode helpers/Bats examples. |
| `scratch/fixtures/` | Tracked deliberate clean/violating Python, Go and Bash inputs used by existing workflows. Not generated disposable output. |
| `tools/verify_fixture.py`, `tools/tests/`, `tools/README.md` | Maintainer-only exact-result/diagnostic checker, contract tests and fixture-use boundaries. Copied inputs/runtime environment remain caller-owned; no sandbox or automatic assembly. |
| `.github/workflows/` | Security workflow and Python/Go/Bash fixture workflows. Source configuration is not proof checks ran or reject the intended defect. |
| `.gitleaks.toml`, `.claude/settings.json` | Existing scanner/vendor settings; exclusions/runtime semantics constrain any enforcement claim. No sandbox established by these files. |
| `skills/` | Adoption proposal guidance and read-side GitHub helper skill. Global installation is operator-managed. |
| `docs/adr/` | Decisions and superseding rationale. ADR-0001 retains original history; ADR-0002 describes the approved quality-first migration. |
| `docs/review-roles.md` | Portable, authorization-scoped writer/reviewer/owner responsibilities. No fleet model mapping. |
| `docs/planning/` | Rebuild plan, frozen candidates, source fingerprints and acceptance/research evidence. Not a default consumer prompt load. |
| Legacy Codex/model guides, `docs/cross-pollination-log.md`, `docs/session-notes.md`, `HANDOFF-phase-1c.md` | Historical doctrine/receipts and optional historical logs. Not current model assignment, permissions or active quality policy. |
| `HANDOFF.md` | Current project baton, progress, next gate and material blockers. |

## Boundaries

There is no root application, ORM, database/client utility library, root package/Makefile test runner, tracker service or publisher broker. Examples under overlays are not live application services. Do not reference `internal/db`, `cmd/server` or similar template examples as existing kit code.

Consumers copy selected approved artifacts and preserve customizations; this repo does not update them automatically. Proposed tracking remains unselected/unbuilt. Existing mutable workflow refs/skipped root TS checks are known limitations, not solved by this map.
