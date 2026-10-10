# Independent C0 review

Candidate: `docs/planning/c0-candidate.json`; supplied SHA256 `d6273c9cce20db96ccc32f4034e9a5dc817148c47606272f29d1048cbb147da3`.

Read-only inspection of actual untracked C0 documents and referenced source. **The review oracle was not read.** No tests, scripts, installations, hosted operations or repository edits were performed.

## Part 1 — independent case decisions

References are to `docs/planning/c0-review-cases.md`. Stated execution premises are accepted **within these synthetic exercises**, not attested as real execution.

| Case | Decision | Concrete reason / smallest correction |
|---|---|---|
| R01, line 9 | meets exercise contract | `Number.isFinite(n) && n > 0` implements the stated number-domain contract; direct tests cover positive, zero, negative and nonfinite values. Preserve the focused fix. |
| R02, line 28 | needs change | Production ignores the actor and writes cancelled status. The test mocks cancellation itself. Authorize before writing; test real cancellation rejection **and confirmed state preservation**, plus authorized success. |
| R03, line 51 | needs change | Correct bytes do not justify a factory, registry, abstract class and forwarding interfaces with no supplied responsibility. Remove redundant layers while preserving the CSV library/writer and output tests. |
| R04 A, line 59 | meets exercise contract | Supplied source inspection establishes one cohesive, pure decoder responsibility and relevant tests. Its 640 lines alone justify neither rejection nor forced splitting. |
| R04 B, line 59 | needs change | Request-derived SQL concatenation, unrelated effects/shared mutation and suppressed failures violate safety and ownership guarantees. Parameterize SQL, establish permission/effect ownership and preserve explicit failures with boundary tests. Length is irrelevant. |
| R05, line 69 | meets exercise contract | The adapter owns a necessary protocol conversion and validation boundary; exercised guarantees include authentication, malformed input and supported conversion. Deleting it loses useful architecture; unknown metadata is expressly permitted. |
| R06, line 77 | needs change | UUID validation does not establish ownership; deletion receives no authenticated actor or permission check. Authorize the target before deletion and test unauthorized rejection without state change. |
| R07, line 88 | needs change | `catch { return []; }` makes unavailable storage indistinguishable from successful empty data. Preserve a meaningful failure, translate it safely externally and test that route. |
| R08, line 101 | meets exercise contract | Current `trim()` already preserves internal spaces and satisfies the supplied direct tests. An evidenced no-change result needs no duplicate test/helper or production churn. |
| R09, line 113 | needs change | Behavior is preserved, but the compressed ternary/throwing IIFE increases reading burden without a demonstrated optimization benefit. Retain the clear existing function; no lost ledger persistence is evidenced. |
| R10, line 131 | needs change | Analytics adds an unapproved external disclosure of private rows and identity. Remove the send and unnecessary dependency; preserve the approved download flow. Merely updating the map would not authorize disclosure. |
| R11, line 139 | needs change | A boolean public API combines distinct charge/refund guarantees and repeated branching without shared policy or maintenance benefit. Retain separate semantic operations and the existing shared writer. |
| R12, line 147 | needs change | **The proposed deletion** breaks supported handling. The route is `dispatch → handlers.get("invoice.paid") → handleInvoicePaid`, with stated integration evidence. Preserve handler and entry; direct-call grep is insufficient. |
| R13, line 164 | meets exercise contract | The actual schema → pricing → safe response route preserves the requirement while removing unnecessary forwarding adapters. Documented rationale/current map are sufficient; do not restore mistaken initial scaffolding. |
| R14, line 172 | unverified | Checkout/probe success establishes no implemented behavior. Applicable candidate-bound lint/type/test evidence and inspectable implementation are missing. No code defect can be inferred from the packet. |
| R15, line 180 | needs change | Editable receipt/hash agreement establishes neither approval nor execution. Report matching recorded source separately; approval and executed checks remain unknown, with configured controls described independently. |

**Setup assessment:** no material ambiguity prevents these 16 judgments. Cases that supply responsibility traces rather than full programs are bounded premise-based exercises, not comprehensive implementation reviews. R14 deliberately supports only an unverified verdict.

## Part 2 — source baseline verification

### Correct

- **Scope is accurately constrained.** `c0-gate-baseline.md:9–11,61–65` separates fingerprint/document checks, historical execution and unexecuted runtime claims. No C0 executable overlay pass is asserted.
- **Root markers:** directory inspection confirms absence of the listed root Makefile/package/pre-commit/Biome/Vitest/Astro configuration markers. `AGENTS.md:7–13,65–70` contains project/command placeholders; `SYSTEM_MAP.md:11–39` explicitly supplies example paths/services, not an active kit map.
- **All four workflows were read.** Their trigger descriptions match source. TS/Astro work is conditional on root probes (`security.yml:92–107,115–128,139–162`), not template configurations.
- **Historical evidence remains historical.** Retained JSON shows a successful TS lint job at `93ee82a…` whose Node/install/Biome/typecheck steps were skipped (`evidence/github-settings-and-ci-evidence.json:913–975`). Fixture clean/trap steps have historical success records at lines `1766–1778`, `1874–1886` and `1982–1994`; these do not establish expected diagnostic attribution. Required contexts/review settings are recorded at lines `104–153`, not independently fetched here.
- **Action count is correct:** 18 executable `uses` references, 12 not full commit SHAs. The commented checkout example is not a nineteenth invocation. Workflow-scoped security write permission and fixture read-only permissions match source.
- **Scanner limits are accurately identified:** broad Markdown exclusions (`.gitleaks.toml:16–20`), mutable Semgrep sources and Trivy HIGH/CRITICAL plus ignore-unfixed configuration (`security.yml:55–76`).
- **Fixture caveats are real:** negative commands suppress diagnostics and accept arbitrary nonzero exits (`verify-templates.yml:101–110`, `verify-templates-go.yml:107–116`, `verify-templates-bash.yml:102–111`). Bash assembly copies fixtures but not `.shellcheckrc` (`verify-templates-bash.yml:84–86`).

### Seven-overlay accounting

| Overlay | Source inspection outcome |
|---|---|
| Bash | Makefile and hook inventory match. `strict-mode.sh:42` accepts zero; Bats tests omit a zero rejection case. Hosted fixture work does not exercise these helpers. |
| TypeScript | pnpm lint/type/test/coverage and Stryker interfaces match shipped sources. `^3.0.0` cannot select a 4.1.11 release; current advisory/support facts were not independently fetched. |
| Workers | Sources merge over TS, generate types before tsc and configure worker testing. The pool-package reference exists; supported-package/API compatibility remains unexecuted. |
| Astro | Additive Prettier and `astro check` commands/hooks match source. Optional framework assembly remains unverified. |
| Bun/ECS | Commands match. `check-file-length.ts:7,20–29` enforces a hard 300-line cap. Purity checks inspect the three stated AST shapes (`check-component-purity.ts:16,23,31`), not complete serializability. |
| Go | Listed lint/vet/race/coverage/Wails/Gremlins interfaces match. Build prerequisites omit `go.sum` (`Makefile.snippet:14`); JSON decoder performs only one decode (`schema/example.go:54–60`). Runtime behavior remains unverified. |
| Python | Ruff/mypy/pytest/coverage/audit/mutmut interfaces match. Hosted fixtures do not execute behavior, coverage, mutation or Pydantic integration. |

### Additional inspected-source findings — inherited, not C0 regressions

These warrant later repairs; they do **not** require operational changes during C0.

- **P2 — Go’s advertised negative vector suppresses itself.** `scratch/fixtures/go/violating.go:12–14` says errcheck must flag the unchecked error, then applies `//nolint:errcheck`. `verify-templates-go.yml:8` advertises that vector while line 107 accepts any failure. Historical green cannot establish errcheck rejection. **Smallest correction:** explicitly record this specific limitation in the baseline if desired; C3/C9 should use an unsuppressed, intended violation and assert its diagnostic. Removing suppression alone is not proof the blank assignment is checked.
- **P2 — consumer install contract conflicts with copied CI.** `security.yml:102,125,154` uses `npm ci`, whereas shipped TS/Astro snippets require pnpm through `preinstall` (`templates/typescript/package.json.snippet:5–7`; `templates/astro/package.json.snippet:3–5`). This is separate from today’s root-marker skips. **Smallest correction:** carry the mismatch explicitly into C12’s disposition and align installation with the selected consumer package-manager contract; do not disable the guard merely to obtain green.

The baseline already disclaims diagnostic proof and inventories both command families. These are concrete repair details, not evidence that its documentation/scenario acceptance must be rejected.

## Review

- **Correct:** representative cases distinguish real contract defects from valid simplicity, necessary adapters, cohesive larger code and evidenced no-change. Source inventory adequately distinguishes configuration, historical results and unknown enforcement.
- **Fixed:** none; read-only.
- **C0 candidate findings:** No issues found.
- **Merge verdict:** OK with notes, for this bounded documentation baseline only. Publication and next-chunk decisions remain with the parent/operator.

## Residual limits

- Candidate/file fingerprints and equality with committed blobs were **not independently recomputed**; supplied hashes are provenance. Parent should confirm frozen bytes still match before accepting the checkpoint.
- Git hook-path/config observations are recorded author evidence, not independently rechecked here.
- No current hosted settings, upstream package identities, permission containment, VM suitability or complete overlay behavior were verified.
- CLEAR does not establish executable enforcement, reliable future reviewer performance or a slop-free implementation.

**C0 verdict: CLEAR**