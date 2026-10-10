# Standards kit routing

For writing/reviewing a change, read [quality-contract.md](quality-contract.md) plus the task's actual project/slice. Do not load every historical motif, research report or model profile. Root [AGENTS.md](../AGENTS.md) maintains this kit; consumers use [templates/AGENTS.md](../templates/AGENTS.md).

| Task | Relevant additional context |
|---|---|
| Find existing kit components / change ownership | [Actual kit map](../SYSTEM_MAP.md). |
| Propose consumer adoption/update | [Adoption skill](../skills/adopt-coding-standards/SKILL.md); [bounded cold start](consumer-cold-start.md); selected overlay README; preserve local instructions/config. No live enrollment implied. |
| Report adoption bindings/customizations/update needs | [Manual status](adoption-status.md); [C11 decision](planning/c11-tracking-decision.md). Unselected checker/catalog implementation deferred, unknowns not compliance/approval; no new receipt service or enrollment. |
| Maintain a language overlay | Only its `templates/<stack>/` files/README and affected callers/fixture/workflow. TS-dependent overlays also use the base TS merge contract. |
| TypeScript / Astro / Workers / Bun-ECS | [TS](../templates/typescript/README.md), [Astro](../templates/astro/README.md), [Workers](../templates/cloudflare-workers/README.md), [Bun/ECS](../templates/bun-ecs/README.md), as relevant. |
| Go / Python / Bash | [Go](../templates/go/README.md), [Python](../templates/python/README.md), [Bash](../templates/bash/README.md), as relevant. |
| Authorized delegation / independent review | [Scoped roles](review-roles.md); exact task/candidate/check evidence. No fixed vendor/fleet mapping. |
| Material design/data-flow/debloat review | [Task-scoped method](architecture-review.md) plus the actual project slice. Optional deeper context, not a default full-repo load or graph service. |
| Understand current core/migration decision | [ADR-0002](adr/0002-quality-first-acceptance.md); [ADR-0001](adr/0001-why-this-standard-exists.md) is original history, partly superseded after acceptance. |
| Verify copied fixtures | [Maintainer fixture checker](../tools/README.md), selected shipped inputs/config and actual tool commands in an approved environment. No automatic consumer payload or workflow replacement. |
| CI/security behavior | [Actual kit CI coverage/boundary](ci-checks.md), `.github/workflows/`, `tools/ci/` and `.gitleaks.toml`; [branch-protection guide](branch-protection.md) is a procedure, not evidence of current hosted settings. |
| Read-side GitHub inspection when needed | [GitHub helper skill](../skills/github-pr/SKILL.md). Read access is not publication authority. |
| Continue approved rebuild / inspect evidence | [HANDOFF](../HANDOFF.md), [chunk plan](planning/rebuild-chunk-plan-2026-10-08.md), relevant candidate/result only. [C0 result](planning/c0-acceptance-result.md), [C1 scope](planning/c1-scope.md). |
| Investigate an old doctrine/receipt | Historical Codex/full-lite/model profiles and optional session/cross-pollination logs only for that explicit question. Not active instructions or current claims. |

Add a route for new maintained responsibilities; mark stale/unknown context instead of guessing. A task not named here does not need an approval merely to inspect relevant source—ask only for a material scope/behavior/risk ambiguity.

**Status:** Follow [current handoff](../HANDOFF.md) and unit-specific acceptance evidence. Units clear separately; existence and historical green checks are not complete compatibility/enforcement proof. No complete-kit release. Tracking implementation deferred pending owner/source/catalog selection; manual status/proposals remain available, not automatic enrollment or approval.
