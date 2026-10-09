---
name: adopt-coding-standards
description: Propose or perform explicitly authorized, customization-preserving adoption of selected Christopher Coding Standards units into a project; distinguish kit-maintenance files from consumer templates and verify actual checks.
---

# Adopt Christopher Coding Standards

Default to an adoption/update **proposal**. Do not enroll consumers, overwrite files, install global skills or alter hosted controls merely because this skill was read. Execute only the target/scope authorized by its owner.

## Establish source, target and existing contracts

- Use the actual owner-selected standards clone/revision; no canonical machine path is assumed. Confirm source identity/revision and known acceptance status. A remote URL, version stamp or editable receipt alone is not approval or trust.
- Identify the actual target repo, ownership, branch/status and existing instructions/config/checks. Preserve other agents' work, local rules, package-manager/lockfile contracts and source history. Do not move repos/worktrees or read/write credential files.
- Read source `docs/INDEX.md`, `docs/quality-contract.md` and only selected overlay READMEs. Check acceptance per unit: content-reviewed core on the rebuild branch does not make unverified overlays or the complete kit a ready release. Missing compatibility/enforcement proof stays unverified; do not claim full adoption from successful copying.

## Select exact artifacts, then propose the merge

| Consumer destination | Source unit | Handling |
|---|---|---|
| `AGENTS.md` | `templates/AGENTS.md` | Merge with existing guidance; fill real project identity, actual verification commands, source baseline and local constraints. Never copy maintainer root AGENTS. |
| `SYSTEM_MAP.md` | `templates/SYSTEM_MAP.md` | Describe actual components/utilities/state/trust boundaries; mark unknowns. Never copy the kit root map or invented example services. |
| `docs/quality-contract.md` | `docs/quality-contract.md` | Preserve the shared requirements; reconcile real local specializations explicitly. Required consumer links must resolve. |
| Optional `docs/architecture-review.md` | `docs/architecture-review.md` | Propose for material design/data-flow/debloat work when useful. Requires the shared contract in the same docs directory; not a mandatory bootstrap unit or automatic refactor grant. |
| Selected language/runtime config/examples | Relevant `templates/<stack>/` | Merge according to its README, not a blanket directory overwrite. TS-dependent overlays preserve a compatible base/package-manager contract. All seven overlays exist; presence is not verified fitness. |

Retain or propose deliberate changes to the project's existing enforcement and publication controls. `.claude/settings.json`, `.gitleaks.toml`, security workflows and branch-protection settings are **not automatic copy steps**: assess runtime permissions, exclusions, identities, actual check coverage and installation compatibility first. Do not transplant known skipped checks or claim a symlink/deny file establishes containment. Do not initialize Spec Kit unless chosen by the owner/project.

Historical Codex/model-role guides and research/session archives are not required consumer payloads. If review/delegation guidance is needed, adapt `docs/review-roles.md` under the project's actual owner/permissions; it creates no launch or publication grant. An approved runtime may need a vendor-specific instruction entrypoint; verify its real loading behavior before adding it, rather than assuming filename parity/symlinks work.

## Verify and report

1. Show exact new/changed units and preservation/compatibility decisions. Material changes to task scope, behavior, risk or authority need clarification, not silent policy replacement.
2. Within authorized scope, apply the bounded merge without overwriting unrelated content. Respect applicable MPL notices when redistributing; do not replace the target's license.
3. Verify document routing/profile facts and applicable real lint/type/behavior/security checks in the designated suitable environment. New/changed gates need clean/intended-failure cases with the expected diagnostics. Unsupported commands, missing tools and skipped steps are not passes.
4. Report source bindings/customizations separately from configured controls, actual execution evidence and approval. Use [manual adoption status](../../docs/adoption-status.md) for conservative unknown/customized/mixed reporting and update proposals. Tracking implementation is deferred pending owner/source/catalog decisions; no checker/enrollment or new required receipt format exists. Do not invent authenticated receipts or adoption history.
5. Commit/push/merge/install/deploy only under existing authority; no hook bypass, force-push or known-broken operational commit.

Keep the report short: selected source/units; what changed/preserved; candidate-bound checks/review; specific unverified limits. A read-only proposal requires no automatic installation or destructive action.
