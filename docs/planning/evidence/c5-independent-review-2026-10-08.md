# C5 independent read-only review

## Review

**CLEAR — No issues found.**

- **Correct:** The bounded TypeScript rebuild meets Q1–Q6 on the supplied source and preserved reference-execution evidence.
- **Fixed:** None; this review made no edits.
- **Findings:** No concrete current in-scope P0/P1/P2 issues identified.
- **Merge verdict:** **OK with notes**, solely as bounded review evidence—not commit, merge, push or publication authority.

## Source and contract assessment

| Requirement | Assessment and evidence |
|---|---|
| **Q1 — Behavior** | `templates/typescript/schemas/example.ts:5–30` preserves exported names, strict unknown-field rejection and parsed-data/null contracts for both parser paths. Only validation-error logging is removed. `schemas/example.test.ts:20–59` exercises the real exports, roles, name limits, optional URLs, invalid inputs and caller-side no-action/input preservation on rejection. This is not authorization or persistence evidence. |
| **Q2 — Simplicity** | `scripts/check-package-manager.mjs:1–20` replaces an implicit unpinned download with a dependency-free local check. It reads the consumer’s manifest pin, compares the user-agent token and accommodates Corepack integrity suffixes. The Makefile remains thin script wrappers (`Makefile:1–35`). No unnecessary framework or abstraction was introduced. |
| **Q3 — Readability** | Responsibilities and limits are discoverable in `README.md:7–55`: initialization versus frozen installs, lifecycle-guard bypass/write limitations, parser versus authorization responsibilities, independent gate probes, optional mutation testing and composition boundaries. |
| **Q4 — Maintainability** | `package.json.snippet:3–37` coherently selects pnpm, local preinstall, runtime Zod and matched Vitest/coverage versions. `tsconfig.json:53–54` includes tests; `vitest.config.ts:12–30` separates test discovery from production coverage. Explicit Stryker plugins address pnpm resolution (`stryker.config.mjs:4–6`); cache, force, thresholds and conservative concurrency remain explicit. |
| **Q5 — Safety** | The selected Vitest/mocker4.1.11 is outside the recorded advisory’s affected range. The precise `typed-rest-client>qs` override, resolved lock and advisory probes support the qs repair without blanket overrides or audit suppression. `.pre-commit-config.yaml:3–19` uses read-only project-local Biome and an immutable native Gitleaks-system hook. No claim turns pinning, validation, hooks or lifecycle checks into universal safety or containment. |
| **Q6 — Evidence** | Preserved command logs show clean checks and intended diagnostic-specific rejections, with declared input hashes. Source-copy, runtime, hook and restored-mutation records agree on the declared candidate fingerprints. Historical failures remain separate from authoritative passing results. |

### Preservation and debloat

All nine affected production/config paths were inspected, including unchanged Biome and the new guard. Tests and documentation were assessed separately.

Recorded physical lines / UTF-8 bytes:

| Path under `templates/typescript/` | Base → candidate |
|---|---|
| `.pre-commit-config.yaml` | 18/869 → 19/769 |
| `Makefile` | 33/630 → 35/630 |
| `biome.json` | 54/852 → 54/852 |
| `package.json.snippet` | 29/995 → 38/983 |
| `schemas/example.ts` | 61/2266 → 30/1174 |
| `scripts/check-package-manager.mjs` | 0/0 → 20/786 |
| `stryker.config.mjs` | 47/1407 → 43/1479 |
| `tsconfig.json` | 54/1729 → 54/1684 |
| `vitest.config.ts` | 30/826 → 32/942 |

Aggregate: **426→425 lines; 9,574→9,299 bytes**. These are supplied measurements, not independently recomputed. Simplification removes logging, misleading commentary and duplicate/downloaded tool resolution while preserving or strengthening relevant guarantees.

## Execution evidence inspected

- `c5-runtime-checks.json:18–1378`: 30 matched expectations; 16 tests comprise 15 shipped schema cases plus one synthetic eligibility test. Clean reference coverage is 100%.
- Intended rejections include `noExplicitAny`, TS2322, formatter differences, an actual failing assertion, uncovered production-source thresholds, empty lint/test selection and guard/lock failures. GNU Make status2 is distinguished from underlying status1; the compiler probe itself reports status2.
- Full mutation execution uses `--force`; five synthetic mutants score100. Weak assertions score0 and fail the break threshold. `c5-restored-mutation.json` shows restored strong incremental/full checks scoring100.
- `c5-hook-checks.json:445–535,587–634,739–786,842–951`: actual clean ordinary commit, read-only Biome rejection, harmless custom-rule staged scanner rejection and restored clean state.
- `c5-npm-install-guard.json:1–36`: real dependency-free npm install rejects1 **after creating package-lock.json**. This does not establish a full npm dependency-graph install or no-write isolation.
- Official metadata records, selected lock entries, initial audit and qs repair audit/probes support dependency selection. The original lint, mutation CLI/plugin and lock-diagnostic harness failures were inspected and are not counted as passes.

## Scope and limits

Inspected the actual working-tree diff, all TypeScript artifacts, scope/check/copy/candidate manifests, relevant baseline fingerprints, decisive execution records and all five named session helpers. Reviewed Workers/Astro/Bun manifests and relevant README/config contracts plus `security.yml` only for carried compatibility boundaries.

The npm-ci/Node22 workflow remains **C12**; Workers/Astro/Bun composition remains **C6/C7/C8**. These are explicitly unaccepted dependent contracts, not C5 findings.

No product tools, shell commands, SSH, installation, VM changes or repository edits were performed. Unrelated configuration, credentials and agent files were not opened. I did **not** recompute packet/file/diff hashes, exhaustively audit every transitive package, authenticate approvals/receipts/binaries, inspect committed ranges or independently replay execution. Recorded protection of175 tracked files remains parent-attested.

Review identity: base `6aec8f384bd2a91c2114234b04dc0231332f68ff`; supplied packet SHA256 `5873996fd727eeeff2e26711174dd9a08fb1671cf7da472cf97c2fd786f01c0e`; supplied tracked-diff digest `3cd4cd9a4c16f7eaef7d58e37517949abc5f7910943cd9592d1ed8b631e0ca05`.

**Final verdict: CLEAR within C5’s approved reference scope.** Other platforms/versions, applications, schema mutation scores, default secret-policy completeness, containment and hosted/live-consumer enforcement remain unverified.