# C5 — TypeScript reference accepted locally

Parent disposition: **ACCEPT within approved C5 reference scope.** Fresh review CLEAR, no source findings; applicable copied-reference checks actually executed on Christopher-authorized ClaudeOS. No push/merge/deploy, all-overlay release, hosted enforcement or consumer enrollment is authorized by this result.

## Candidate and review

- Base `6aec8f384bd2a91c2114234b04dc0231332f68ff`, branch `rebuild/quality-core-2026-10-08`.
- Frozen packet `c5-candidate.json`, SHA256 `5873996fd727eeeff2e26711174dd9a08fb1671cf7da472cf97c2fd786f01c0e`; tracked-diff SHA256 `3cd4cd9a4c16f7eaef7d58e37517949abc5f7910943cd9592d1ed8b631e0ca05`.
- Before closure edits, parent verified all37frozen inputs, all5session helpers, whole diff, all175protected tracked files and unrelated `.project.yaml` unchanged after review. No source mutation during review.
- Reviewer child `6e21c66e-10db-4ead-a3e5-bfec9b21ad72`, workflow `e6678e2a-a689-4f7a-b993-53eb87758b00`: **CLEAR — no concrete current in-scope P0/P1/P2 source issues**. Preserved byte-identical report: `evidence/c5-independent-review-2026-10-08.md`, SHA256 `7c9a84681a28d944b26be598e688f72ce48b49ad8caeefa06f10e954ff59e40f`.
- Review inspected actual source/diff, callers, tests, relevant dependencies/composition, evidence and session helpers. Reviewer did not replay commands, recompute hashes, authenticate artifacts/binaries/authority, or exhaustively audit every dependency. Bounded merge verdict is evidence, not authority.

## Parent correction of review arithmetic

The report incorrectly totals the correct per-path measurements as426→425physical lines. Parent independently summed the frozen nine-path measurements: **326→325physical lines**, **9,558→9,299Unicode code points**, **9,574→9,299UTF-8 bytes**. The supplied per-path rows and byte aggregate are correct; the report's line aggregate is not. Original report remains unchanged, with this explicit disposition. No product/config/input change or source re-review is needed for that report-only arithmetic correction. Counts include the replacement guard and unchanged reference Biome; tests/docs are separate. Counts are not tokens, performance results or a quality score.

## Established behavior and selected contracts

- Preserve exported schema/parser/type names, strict unknown-field rejection and parsed-data/null sync/async contracts. Remove validation-error logging. Tests call actual exports and demonstrate rejection before a small caller's effect without input mutation; they do not implement authorization, HTTP or persistence. A structurally valid admin role is not permission.
- Replace unpinned npx bootstrap with a dependency-free local Node guard reading the consumer's pin. Default remains pnpm10.34.3; intentional first lock initialization differs from normal frozen installation. Real wrong-manager guard probe rejects but **already creates package-lock.json**; no isolation/no-write/anti-bypass guarantee.
- Select paired Vitest/coverage4.1.11 outside GHSA-82fw-gwwq-j7x9's recorded affected stable range. TypeScript5/Biome2/Zod4/Stryker9 majors retained; Zod is a runtime dependency. Exact versions/reference lock establish the tested graph, not a universal lock for a partial snippet.
- Scoped `typed-rest-client>qs` override6.16.0 repairs the observed Stryker9.6.1→caller2.3.1→qs6.15.1 advisory path. Official metadata, current lock, no-reported-vulnerability audit and actual resolved qs advisory probes support the repair; no audit suppression/blanket override. Keep reviewing/removing the override only when upstream and actual lock permit.
- Typecheck includes tests; coverage explicitly includes intended production sources, including unimported ones. Make remains a thin configurable-manager wrapper; it does not change an npm/Bun project's manifest/guard/lock contract.
- Optional Stryker full script uses documented `--force`, explicit plugins work with pnpm layout and conservative concurrency1. Mutation is not mandatory or blanket correctness proof; schemas remain outside the reference mutation scope.
- Read-only local Biome hook uses the project's installed locked binary, avoiding a duplicate npm-resolved hook environment. Immutable Gitleaks-system hook uses the previously verified native8.30.1 scanner, not an automatic Go SDK bootstrap. Staged scanning/custom sentinel does not prove complete default secret detection or a directory scan.

## Actual execution evidence

`c5-vm-evidence-manifest.json` binds18byte-identical VM artifacts; parent verified their recorded hashes. Source-copy/runtime/hook/final-restoration fingerprints agree on all11current overlay inputs and the reference lock.

- ClaudeOS Debian13.7, Node24.21.0, pnpm10.34.3, TypeScript5.9.3, Biome2.4.15, Zod4.6.5, Vitest/coverage4.1.11, Stryker components9.6.1; reused task-owned pre-commit4.6.2/native Gitleaks8.30.1. Existing Node/npm observed, not freshly authenticated binaries. No sudo/global packages/system/GUI/config changes or product execution on Beelink.
- `evidence/c5-runtime-checks.json`:30matched command expectations.16actual tests comprise15shipped schema cases plus1synthetic eligibility test; clean reference coverage100%. Frozen install, audit, lint/format/type/tests/coverage, Make manager override, resolved qs probes and full/incremental mutation executed.
- Separate intended `noExplicitAny`, TS2322, format, failing assertion, uncovered production source, empty lint/test selection, wrong/missing guard, missing/stale-lock and weak-mutation probes reject with expected diagnostics and unchanged declared-file snapshots. GNU Make failures return2; underlying tool contracts differ (compiler itself returns2, many other tools return1). Arbitrary nonzero/absent tools are not substituted.
- Five synthetic mutants score100 with strong boundary assertions and0with weak assertions; below-floor rejection is observed. `evidence/c5-restored-mutation.json` verifies restored strong tests score100 for cached and forced full checks. This is not an application/schema mutation score or model benchmark.
- `evidence/c5-hook-checks.json`:19supplemental guard/Git/hook/setup operations, including installed hooks, ordinary clean fixture commit, read-only Biome intended rejection, harmless custom-rule staged scanner rejection and restored clean state. No known-broken commit/hook bypass attempted; setup operations are not19product tests.
- `evidence/c5-npm-install-guard.json`: actual npm install on an isolated dependency-free fixture sharing declared pin/engine/preinstall and byte-identical guard. Intended exit1, declared files unchanged, second lockfile created. Not a full npm installation of the reference dependency graph.
- Parent static checks:5local links resolve;175protected tracked files and unrelated metadata preserved; candidate inputs/helper/diff hashes agree; authored tracked/untracked text whitespace checked. Byte-preserved raw VM logs and independent report are archival observations, not authored whitespace-normalized files. The returned report has no terminal newline; an initial authored-EOF assertion correctly stopped before staging/commit. Its exact identity was then checked separately, preserving the report rather than changing it. Authored EOF checks apply to the other paths; the complete staged Git whitespace check remains required.

## Failures retained and limits

Initial three-qs-advisory audit and format/import failures retained; repair then affected/full checks rerun. Broken `--incremental false` treated false as a missing config filename; explicit `--force` repaired it. Implicit plugin discovery found no checker in pnpm layout; explicit modules repaired it. Initial missing-lock harness expected NO_LOCKFILE, but full manifest checks overrides first and diagnoses LOCKFILE_CONFIG_MISMATCH; mismatch is recorded as failure. Criteria then reflect the specific implementation, with an additional minimal no-override missing-lock probe and stale-lock probe—not an arbitrary-error pass.

Only selected Linux/tool/reference behavior executed; manifest's Node24+ baseline is not proof of every newer version. Emitted Node application/library execution, browser environments, other platforms, full applications, complete dependency safety, default secret coverage, process-tree containment and hosted/live-consumer enforcement remain unverified. Existing C4 cache/bootstrap limitations remain; shared prior caches/artifacts were not cleaned and this is not a pristine VM.

C6 Workers, C7 Astro and C8 Bun own actual composition. C12 owns inherited npm-ci/Node22 workflow mismatch and legacy diagnostic suppression; no workflow changed by C5 and deleting the guard is not the repair. C9 owns the suppressed Go errcheck fixture. Closure edits affect this result/report preservation and progress-only HANDOFF, not the reviewed source. Next: C6 Workers compatibility on the approved environment, followed by fresh review.
