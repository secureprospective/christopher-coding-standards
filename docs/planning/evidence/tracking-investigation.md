# Standards tracking/update mechanism — investigation only
Date: 2026-10-08
Scope: christopher-coding-standards at main 93ee82a; local TheWarRoom and TFM Playbook evidence. No implementation, consumer edits, installs, hosted API calls, or fleet coordination performed.

## Recommendation
Use a small deterministic, on-demand checker/planner, backed by a tracked consumer receipt. Generate a registry view from receipts rather than maintaining a second authoritative database. Begin with reporting and safe update proposals, not unattended overwrites. Python standard library + Git should suffice for this first slice; both are locally available (Python 3.13.5 / Git 2.47.3). Portability on other machines remains unverified.

This is a preliminary design for operator approval, not a fleet-wide durable decision. No precise code size or token saving is benchmarked. Routine classification can require zero model calls; inspecting conflicts and interpreting behavior changes still needs a person/agent.

## Direct repository evidence
- ADR docs/adr/0001-why-this-standard-exists.md:34-53 defines canonical upstream, downstream copying, enforcement outside AGENTS, and outward updates.
- Adoption skill is a manual copying/customization checklist with no version receipt or sync process.
- templates/typescript/README.md:34-74 copies some files and merges package.json snippets, customizes formatter and compiler paths, and exempts Workers/Bun from base package-manager settings.
- templates/astro/README.md:65-66 explicitly replaces the base TS compiler config. Astro therefore cannot be represented as two independently authoritative writers for tsconfig.json.
- templates/go/README.md:47-73 copies/relocates files, merges Makefile targets, and requires project-specific depguard import prefixes. Blind recopy can erase intentional architecture law.
- Source .gitignore treats CLAUDE.md as local metadata. SYSTEM_MAP and feedback logs are customized/append-only material, not wholesale-update candidates.
- TFM's origin resolves to a local bare repo, and worktree list exposes six different refs. Remote URL alone cannot reliably identify projects. A stable explicit project ID is safer; local scanner can also group shared Git common directories.
- Read-only SHA256 comparisons: TheWarRoom ifaceguard.go matches current source byte-for-byte; .golangci.yml, hooks, bloat script differ. TFM Biome and hooks match; tsconfig, Vitest, Stryker differ. Differences do NOT prove noncompliance or reveal an adoption version. No existing receipt was found in bounded consumer search.

## Minimum mechanism (proposed files, not created)
1. Canonical distribution catalog: explicit source-to-destination mappings, stack composition/precedence, excluded examples/living docs, and ownership class. Schema validated; unique destination ownership; repo-relative paths only. Catalog must identify relevant shared rules so base/global changes are not missed.
2. Each consumer tracks `.coding-standards.json`: schema version, stable project ID, canonical Git source, selected stack(s), and entries containing accepted source commit, source paths/fingerprint, target path, ownership class, and last accepted destination fingerprint. Unknown provenance is explicit. Per-entry commits allow partial migrations; a single global SHA cannot honestly represent them.
3. One canonical checker/planner using stdlib + Git; it reads catalog/receipt and compares content against an explicitly selected approved source commit. No code loaded from receipts, no arbitrary shell commands, no automatic hook execution.
4. Generated registry report, not another editable source of truth. Initially scan supplied local checkout roots. A fleet-wide rollup would need ClaudeBox coordination and read-only access to registered locations; do not infer coverage outside reachable scanned roots.

Ownership classes:
- Managed: entire file intended to be upstream-owned and exact; limited early set, verified against source before enrolling.
- Customized: entire file has project settings or merged snippets; manual review or later reviewed migration.
- Reference-only: example code, SYSTEM_MAP, project profile, append-only logs; notify on upstream changes, never overwrite.

A raw source commit and fingerprints are provenance/byte-integrity data, NOT proof every rule is enforced. Gate verification must be reported separately, at a consumer Git ref with command/tool evidence, or shown as unknown. Avoid inventing a semantic compliance solver for the first slice.

## Deterministic classification
Compare (A) accepted upstream fingerprint, (B) selected upstream fingerprint, (C) current destination fingerprint, and (D) recorded accepted destination fingerprint.
- B=A and C=D: unchanged.
- B=A and C!=D: local drift since acceptance; may be legitimate, not automatically a violation.
- B!=A, C=D, managed and historically source-identical: clean replacement candidate.
- B!=A, customized OR C!=D: review required.
- Receipt/source/target missing or ancestry unavailable: unknown/missing; no guessed baseline.
- Both edited: review required; future three-way merge can propose a draft, never assert semantic safety just because text merges cleanly.

Content fingerprints are the freshness signal. A new source commit affecting only session history must not trigger updates to every consumer. Hash explicit source sets, with mapping boundaries. For merged snippets, a whole-target hash is conservative: unrelated package.json edits can cause review status but must never lead to overwriting it. Key-aware extraction/patching is an optional later refinement, not a requirement for trustworthy first tracking.

## Initial migration of existing consumers
1. Inventory in read-only mode and display `untracked/provenance unknown` for current copies.
2. Compare selected source/destination paths and present exact matches plus customized files.
3. After owner review, enroll confirmed managed exact matches; record customized acceptance as an explicit reviewed baseline, not a historical adoption claim.
4. Document any older-rule exceptions without pretending current source was applied. Older accepted source commits remain old until migration accepted.
5. Run relevant gates before claiming verified enforcement. Preserve honest `not verified` until checks actually execute.

Existing consumers' entry documents belong to their project owners/agents. This investigation is not permission to rewrite them or activate hooks.

## Update flow and controls
- `status`: offline by default against an available explicitly selected source snapshot; minimal summary/JSON, no model.
- `plan`: scoped file/key diffs and classification only; read-only default; no build/install.
- Later approved `apply`: exact managed replacements only on an approved clean branch/worktree, verifying expected hashes again immediately before writing; no automatic deletion or rename, symlink escape, reclassification, or overwrite of customized data.
- Advance each entry's accepted source only when its update/exception is explicitly accepted. Failed gates and partial changes must remain visible; validation results cannot be inherited across changed Git refs.
- On-demand first. A local timer/CI can later run `status` without tokens and notify only changes. Actual hosted PR automation requires explicit credentials/authority, consumer access, and a chosen central-versus-per-repo schedule.
- No daily LLM scan of all repository prose, no per-session network fetch, no moving branch as accepted version, no auto-merge.

Human-readable output should be brief, e.g. `project | ref | stacks | upstream changes | local edits | review needed | last verification`. One row per logical project for the chosen/default ref, with divergent worktrees visible on request rather than collapsed into a false single state. Explicit enrollment IDs plus Git common-directory grouping prevent duplicated worktree counts; distinct clones sharing an ID still retain observed refs and last-observed state.

## Alternatives checked
- Copier: real template lifecycle tool with answers file, Git template versioning, update/check-update, and conflict handling. Strong option if converting to fully rendered project templates. Existing projects are manually merged/customized and have no genuine generation receipt, so introducing Copier now requires template conversion and careful bootstrapping. Official docs explicitly prohibit fabricated/manual edits to its answers file because smart-diff assumptions break. More migration/runtime machinery than a narrow tracker.
  https://copier.readthedocs.io/en/stable/updating/
- Renovate: custom regex manager can track versions/digests in nonstandard files and propose version-pin PRs. Does not by itself propagate customized template content or prove enforcement. Good later for tool/action dependency versions; don't let a bot bump an `accepted_source` receipt without applying/reviewing associated rule changes.
  https://docs.renovatebot.com/modules/manager/regex/
- Git merge-file: supplies deterministic text three-way merge and conflict detection; useful for draft proposals where a genuine old baseline exists. Text conflict-free does not mean behavior preserved, and original unrendered source isn't an adequate base for heavily customized generation without extra provenance.
  https://git-scm.com/docs/git-merge-file
- Submodule/shared package: source binding is cheap, but copied hooks/config/merged package files still need integration; runtime loading across seven stacks adds portability and adoption work. Does not solve today's drift on its own.

## Acceptance checks before building anything beyond first slice
- Source history-only edit -> no updates for unchanged tracked rule content.
- Managed upstream-only edit -> clean proposal, no existing consumer mutation during status/plan.
- Local-only edit -> drift/review, never silent overwrite.
- Upstream+local edit -> review; source acceptance not advanced.
- Customized snippet -> preserves unrelated project keys; initial phase may simply refuse automatic modification.
- Astro/TS overlap -> unique effective compiler-config owner; shared TS rules still tracked.
- Workers/Bun composition -> no accidental pnpm guard injection.
- Missing/invalid receipt, source unavailable, malicious paths/symlink destinations -> explicit unknown/error and no writes.
- Six TFM worktrees -> one project identity plus divergent refs, not six adopters or a falsely uniform state.
- Partial adoption -> honest per-entry source revisions, not one misleading global current status.
- Rule version current + gates never run -> freshness current, enforcement unverified.

## Exact first implementation step after approval
Create and test the canonical mapping/schema and read-only status checker against temporary synthetic fixtures. Then produce an enrollment proposal for the two known consumers; do not change their tracked files before their owner approves. Add safe managed-file update planning only after classification is demonstrated. Broader modernization and automated PR delivery remain separate decisions.

## Decisions remaining
- Whether operator wants local visibility first (recommended) or an immediate fleet/hosted registry (requires coordination/access).
- Which files are genuinely managed versus customized, and which source ref/release is approved for rollout. Conservative default is customized/unknown.
- When to permit automated PR creation/replacement; no unattended mutation is implied by this investigation.
- Whether later template growth justifies Copier rather than maintaining narrowly scoped migration logic.
