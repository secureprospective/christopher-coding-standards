# Coding-standards rebuild — chunks and verification gates

Owner: Bee. Operator: Christopher. Date: 2026-10-08.

**Scope:** execution plan for the approved quality-first rebuild. C0 acceptance exercises/source baseline are in progress; no operational standards changed. Christopher requested independent subagent verification so this anti-slop repository is held to its own standard. That review requirement applies to this rebuild; it is not a new universal ceremony for consumer projects.

Base: checkpoint branch `docs/standards-rebuild-checkpoint-2026-10-08`, commit `69e0658dcb5ff45806eb048dcaf7207df684d9f5`. Existing untracked `.project.yaml` stays untouched. This plan does not authorize hosted setting changes, automatic publication, consumer enrollment or fleet rollout.

## Working shape

- **Bee is the sole implementation writer.** One coherent responsibility per chunk; no competing writers or unrelated cleanup.
- **A fresh-context, read-only reviewer subagent checks each candidate.** It receives the approved goal/criteria, actual files/diff, candidate identity and test evidence—not the author's conversation or a request to agree.
- **A chunk is not done because tests are green or the reviewer says OK.** Applicable machine checks AND independent review AND Bee's evidence-based disposition must clear.
- Work on an implementation branch after this plan is reviewed and the loop is summarized to Christopher. No experimental change to main.
- Reuse existing fixtures/tools before adding helpers. Chunk boundaries follow contracts/dependencies, not line counts or a calendar.

## Ordered chunks

The seven overlays are seven separate chunks. The TypeScript foundation clears before dependent overlays. Other overlays run sequentially as well; no parallel implementation is needed.

| Chunk | Bounded result | Verification required before clearing |
|---|---|---|
| C0 — Acceptance baseline | Assemble small representative review cases and record expected verdicts before changing operational standards. Record current gates, known failures/no-ops and affected surfaces. | Correct small fix and evidenced no-change accepted; weak-test green patch, unsafe valid input, swallowed failure, gratuitous framework and unreadable compression rejected for concrete reasons. Cohesive large code, necessary adapters and improved design not penalized. Reviewer inspects cases, independent verdicts and disagreements; no unsupported quality score. |
| C1 — Core contract and routing | One compact quality source of truth, task-scoped agent instructions and deliberate migration of contradictory guidance. Distinguish maintaining this kit from templates copied into consumers. Preserve history through superseding rationale where necessary. | Six dimensions retained; no universal size/DRY/dependency quotas or per-step approval ritual. Instructions agree across maintained entrypoints; kit guidance has no accidental template placeholders. Links resolve. C0 cases still distinguish quality correctly when reviewed under the actual new instructions. |
| C2 — Architecture/data-flow/debloat method | Integrate the approved small initial-flow slice, independently traced review and preserving debloat suggestions. No graph engine or mandatory new classes/files. | Exercise unexpected state/network effects, dynamic callbacks, different guarantees behind similar syntax and a better implementation than the initial map. Reviewer separates intent/source trace/exercised behavior/unknowns; suggestions identify preservation evidence. Reduction measurements include all affected production files and separate tests/docs; code-golf cannot pass. |
| C3 — Reusable verification fixtures | Reuse/repair the smallest existing fixture mechanism for assembling copied templates and retaining real command results. Add only indispensable shared fixture support, not a test platform. | A clean fixture succeeds; a deliberate relevant violation fails at the intended check with the expected diagnostic. Missing tools, failed installs or skipped steps cannot count as either result. Test-copy identity/environment is recorded; fixture scope excludes credentials and real consumers. |
| C4 — Bash | Correct boundary helpers and test/lint wiring, including positive-integer semantics. | Zero, negative, malformed and valid-positive cases observe the stated contract. Bats and ShellCheck actually run on copied shipped files. Reviewer checks shell/path handling and useful diagnostics, not just exit codes. |
| C5 — TypeScript | Bounded dependency/security and test-tool compatibility repair, including the known Vitest advisory; retain necessary lint/type/test/coverage capabilities. Reverify current advisory/version facts before choosing versions. | Clean copied fixture installs and runs applicable format/lint/types/behavior tests. Deliberate violations fail correctly. Vitest/coverage compatibility demonstrated; mutation tooling checked where shipped/promised, not imposed universally. No blanket upgrades or security suppressions. |
| C6 — Cloudflare Workers | Compatible worker-test integration using current supported tooling, based on accepted TypeScript contracts. | Copied worker fixture typechecks and runs representative worker behavior/failure tests in the intended runtime. Migration verified against current official docs; compatibility dates are preserved unless separately justified. |
| C7 — Astro | Correct optional framework integration, generated type handling and formatter guidance. | Supported minimal non-React fixture and optional React fixture build/typecheck/test as applicable. Current generated-file and Biome handling demonstrated; neither optional dependency nor generated output is treated as universally required source. |
| C8 — Bun/ECS | Align component/state ownership and actual checks with the quality contract; remove unsupported purity/snapshot/size claims. | Representative state flow and behavioral checks run under Bun. Cohesive code is not rejected by a hard file cap. Reviewer compares promised invariants with actual source and tests; evidence does not claim more than checks establish. |
| C9 — Go | Repair analyzer/dependency/CI assumptions and boundary correctness; keep project-specific integrations optional. | Copied fixture builds/vets/tests with reproducible dependency metadata. Intentional analyzer violation fails correctly. JSON trailing-data and relevant error paths tested; checks do not fail open. Wails/depguard assumptions are not exported to unrelated projects. |
| C10 — Python | Repair supported mutation-tool/config/type integration, including applicable Pydantic typing. | Copied fixture lint/type/behavior tests run. Shipped mutation command/config is exercised on a tiny relevant case if retained. An intentional typing/boundary defect produces the intended diagnostic; commands match current official documentation. |
| C11 — Tracking decision, then read-only slice | Confirm the still-proposed catalog/per-unit-baseline/checker design and necessary ownership/source rules before its implementation. If selected, build only deterministic offline status; keep customized-unit comparisons conservative. No model calls, updater, broker or registry service. | Selection/ownership uncertainty stops this slice, not otherwise-ready core/overlay work. If built, fixtures cover unchanged, stale, customized, mixed revisions, missing/unknown bindings and unsafe paths. Checker leaves consumers unchanged and preserves customizations. Freshness/provenance/configured controls/executed evidence remain distinct: editable receipt/hash never proves approval or passing checks. |
| C12 — CI integration | Wire accepted fixtures/checks into repository workflows so reported success means the relevant work ran; narrow privileges/pin references within the approved source seam. Hosted branch protection/settings remain unchanged. | Run workflow commands on the matching candidate; inspect exact-candidate hosted job steps only when publication/run authority exists. Applicable required TS checks cannot succeed by skipping substantive work. Map all seven overlays to actual coverage; flag checks not required by hosted policy. No claim that configured YAML proves hosted enforcement. |
| C13 — Whole-kit acceptance | Assemble core, chosen overlays, review method, adoption/update guidance and tracking into a disposable synthetic consumer; complete index/map/setup docs. Do not enroll real projects. | Cold-start reviewer follows shipped instructions, not planning drafts. Copy/customize/install/verify/track/dry-run update-proposal route works end to end, preserves custom rules and exposes missing evidence. Cross-chunk regressions and dangling/contradictory instructions checked; final diff contains only approved scope. Christopher receives actual results, unknowns and the integration decision. |

**Dependency rule:** C0 → C1 → C2 → C3; C5 → C6/C7/C8; all overlays → C12/C13. Tracking participates in final acceptance only if selected/built; an unresolved infrastructure choice does not hold core/overlay verification hostage. If a later fix changes a previously accepted shared contract, reopen the affected earlier gate and dependent checks. Do not pretend earlier acceptance still covers changed code.

## The repeated loop

```text
Define chunk: result + allowed surfaces + preserved guarantees + checks
    ↓
Implement the smallest complete change (Bee only)
    ↓
Run applicable checks in the designated suitable test VM
    ↓
Freeze candidate: base ref + diff + allowed untracked files + content hashes
    ↓
Fresh read-only subagent: inspect actual source, test oracles and evidence
    ↓
Bee classifies findings against the contract
    ├── concrete defect / material missing proof → fix or obtain evidence
    │       → rerun affected checks → freeze new candidate → re-review affected slice
    ├── optional/out-of-scope preference → record disposition, no speculative rewrite
    └── checks + review + disposition clear → accepted checkpoint → next chunk
```

For documentation-only chunks, use structural/link checks and representative review exercises; do not invent product runtime checks. A live-source trace and an executed behavioral result remain different evidence.

### Machine gate

- Before implementation, name the relevant commands/outcomes and preserved invariants. Add a regression test only where existing evidence does not already cover them.
- Run product/tool tests in the designated suitable VM, not the Beelink host. Availability/ownership must be established; do not boot or repurpose a shared VM automatically. If unavailable, the chunk is **blocked/unverified**, not green.
- Verify the tested copy matches the candidate, including relevant templates, tests, configuration and locks. Record runtime/tool versions, commands, exit status and meaningful output. A Git HEAD alone does not identify an uncommitted diff.
- New/changed enforcement needs a clean pass and an intended violating-case failure with the correct diagnostic. Test data deliberately violating rules is not itself a passing gate.
- Skipped steps, stale-code results, arbitrary nonzero exits and missing dependencies cannot substitute for evidence. No acceptance-weakening test changes to manufacture green.

### Independent review gate

Reviewer task covers all six quality dimensions within the changed slice: requested behavior, simplest sufficient design, human readability, responsibility/data ownership, safety and evidence. It inspects actual implementation/callers, tests/mocks and necessary configuration. It actively checks for unnecessary abstractions, duplicated business rules, missing failure paths, misleading checks and contradictory guidance.

Return only concise evidence-backed findings: location, violated contract/maintenance cost, smallest correction and verification needed. Verdict is **meets contract / needs change / unverified**. No finding quota; already-good code can pass unchanged. Parent disagrees only with a recorded source/contract-based reason, not a silent waiver.

Do not modify the candidate during review. Fixes invalidate the affected candidate evidence: rerun relevant checks and review the fix blast radius. Reviewer output is evidence, not permission to publish or proof that all bugs are absent.

### Acceptance and stop conditions

A chunk clears only when applicable checks actually pass, no valid material blocker remains, significant findings have dispositions, and candidate identity still matches what was checked/reviewed. Record a short result: candidate, verified behavior/checks, reviewer run/report, limitations and remaining notes. Checkpoint/commit only under existing authority; no known-broken commit, hook bypass or automatic push/merge/deploy.

No repeated human approval for routine in-scope fixes. Stop and ask only for changed behavior/scope, material new risk, an unapproved durable architecture/authority decision, unavailable verification or reviewer disagreement that cannot be resolved by evidence. Escalate required fleet/expert decisions to ClaudeBox. If a review-fix cycle repeats without narrowing a concrete failure, stop and diagnose rather than burn tokens endlessly.

A delegation/tooling failure blocks the review gate. Report exact failure/run/cwd/branch and preserve the diff; no silent switch to another execution protocol. Gates detect defects and make limits explicit; they do not guarantee a slop-free repository.

## Current state

Independent plan review **CLEAR**, with no issues found. Reviewer run: `05b73196-60f6-4405-acfd-35b1ef473595` (fresh context, read-only).
Reviewed plan SHA256: `53648cbd0a66dc2b59eaa2b0ebf5089ddb9926c6a9a518042fd705f0d433d65f`; checked unchanged before recording this outcome. The only subsequent plan edit is this status/provenance record, not the chunks or gates.
Report: `evidence/chunk-plan-review-2026-10-08.md`, preserved byte-identically from the returned artifact; SHA256 `3289d1ab2a9d503fc02dd0c65ff8940913eff4d7210dce5ff8b61dabb1bd0cfc`.

The loop has been summarized to Christopher and approved: **“excellence is the standard, not the goal.”** C0 is in progress on `rebuild/quality-core-2026-10-08`: synthetic acceptance cases, pre-recorded expected verdicts and current-source gate inventory. Independent C0 review must clear before C1. No operational standards, overlays, workflows, tracker or consumers changed.

Residual limits: plan review does not establish VM availability, exact executable gate commands/tool identities or authorized hosted execution. Establish those at their gates; no unexecuted verification is reported passing.

References: `rebuild-at-a-glance-2026-10-08.md`, `code-quality-acceptance-contract-draft-2026-10-08.md`, `architecture-dataflow-debloat-review-draft-2026-10-08.md`, and relevant sections of `evidence/overlay-audit.md` / `evidence/tracking-investigation.md`.
