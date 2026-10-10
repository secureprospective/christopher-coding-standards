# C1 — core contract and routing acceptance

Owner: Bee. Date: 2026-10-08. Content review **CLEAR**. This frozen note records the disposition before status finalization; [HANDOFF](../../HANDOFF.md) records the current final-review/checkpoint state. Acceptance is for this core/document-routing slice, not runtime compatibility, consumer enrollment or release.

## Reviewed candidate and disposition

- Base: C0 checkpoint `1ea1a0e`; branch `rebuild/quality-core-2026-10-08`.
- Original candidate: `c1-candidate.json`, SHA256 `c5273731da1a564abe85aca286da80a0a5e00735da32569c0e1bae44fbd9bf40`.
- Fresh-context reviewer: `e25f7836-28cf-4667-b2d8-5e3306bfdbfa`; verdict CLEAR, no issues found.
- Unedited original report: `evidence/c1-independent-review-2026-10-08.md`, SHA256 `6d886207cb09fc2ec000f1e382d1f26bd394aeee8d06e605c67ea8db9254705d`.
- All16 independent exercise judgments under the actual new contract agree with the pre-recorded oracle. Reviewer did not read it or previous verdicts. No expected answers or criteria changed to manufacture agreement.
- Parent verified all17 original artifacts, diagnostic-helper hash and tracked-diff hash after review. C0 cases/oracle/result remain byte-identical to base. No waived finding or material blocker.

## What changed

One shared six-dimensional contract; kit-maintainer versus consumer instructions/maps; task-scoped routing; customization-preserving adoption proposals; portable authorization-scoped review roles; ADR-0002's explicit migration rationale. Five historical guides retain their original bodies behind status banners; ADR-0001 remains untouched.

No runtime language templates/configs, fixtures, workflows, vendor permission files, dependencies, credentials, real consumers or hosted settings changed. `.project.yaml` remains untouched. No file/repo/worktree moved.

## Verification and limits

Document checks passed:61local links, structure/whitespace, profile placeholders absent from maintainer guidance, all six dimensions present, five original historical bodies retained,87protected baseline sources unchanged. Disposable Markdown-only consumer routing resolves correctly and rejects a missing required contract. These are document-integrity checks—not executable product/scanner/hook tests.

Measured initial default read sets: prior kit writing route5368words/34452bytes; new kit route including index1451words/11925bytes; consumer template+contract1100words/8589bytes. Exact paths/conventions are in `c1-checks.json`; post-status-finalization counts may differ slightly. No actual token savings, performance gains, reviewer accuracy rate or size quota claimed.

First check used an incorrect assumed protected-source count; the diagnostic was corrected to derive87from actual inventory coverage. No source failure was suppressed. Parent checks are independently inspected evidence, not independently recomputed by the reviewer.

Still unverified: runtime overlay install/build/behavior/coverage/mutation, intended fixture diagnostic attribution, test VM suitability, current hosted enforcement, containment and live adoption. Known Go trap and npm/pnpm issues remain assigned to C3/C9 and C5/C12 respectively. Review grants no publication authority.

## Finalization boundary

The initial candidate is immutable evidence of pre-acceptance source status. Finalization changes only candidate→accepted-core status notices and points readers at this result; it does not change the quality contract, review-role policy, consumer templates or runtime controls. A separate patch/frozen finalization record retains that delta. Recheck documents/protected sources and have the retained reviewer inspect the narrow delta before checkpointing.

Next: C2, the architecture/data-flow/preserving-debloat method, after finalization clears. Existing owner/fleet/commit/push/merge/deploy constraints remain live; no complete-kit release claimed.
