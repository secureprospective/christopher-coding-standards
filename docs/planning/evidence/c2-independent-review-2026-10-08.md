# C2 independent gate

## Review

**C2 verdict: CLEAR. Merge verdict: OK for this bounded documentation slice.**

No issues found.

- **Correct — grounded architecture:** `docs/architecture-review.md:7–19` scopes nodes to real responsibilities, contracts, state/effects and boundaries. It rejects mandatory classes/files, DAGs and purity rituals.
- **Correct — independent evidence:** `:23–42` requires tracing callers, transformations, ownership and dynamic routes; separates intent/source/execution/unknowns; permits better implementation without letting revised maps authorize unsafe effects.
- **Correct — preserving debloat:** `:46–61` protects necessary adapters and different semantic rules. Suggestions include guarantees, callers/effects, risks and targeted verification; no automatic rewrite authority.
- **Correct — honest economics:** `:65–75` includes replacement files, separates production from tests/docs and Unicode from bytes, distinguishes estimates from measurements, and rejects code-golf and extra ceremony.
- **Correct — optional routing:** additions at `README.md:32`, `SYSTEM_MAP.md:9`, `docs/INDEX.md:13` and `skills/adopt-coding-standards/SKILL.md:23` consistently expose an optional unit. The shared contract and consumer templates remain outside the diff; minimal consumer instructions require no method link.

This satisfies Q1–Q6 within C2: coherent requested guidance, economical structure, readable instructions, grounded ownership, preserved safety/authority and appropriately bounded evidence.

## Candidate and check evidence

Reviewed the actual working-tree diff and named source files against the supplied C1 baseline `d49e0ab`. The final diff inspection still shows exactly four tracked routing edits and the expected new C2 files; `.project.yaml` remains outside scope.

Packet identity supplied: `docs/planning/c2-candidate.json`, SHA256 `eae10296abfd8ae413232254f6e1b3c7eb8e85fa0930d1fd5b8d1a7345f7caf1`. I did not independently recompute hashes or inspect committed ranges.

I inspected `c2-checks.json` and the session helper’s assertions rather than accepting its green flags as semantic authority:

- Helper lines 21–47 check allowed paths, unstaged scope, structure, local links and byte equality of protected tracked files. The record reports 41 links and 140 protected files.
- Lines 60–88 assemble disposable minimal/extended Markdown consumers and require missing-contract findings from both the profile and method. The corrected missing-document branch at lines 52–54 prevents the prior `FileNotFoundError` from masquerading as intended rejection.
- Lines 91–102 distinguish physical lines, Unicode code points and UTF-8 bytes and include replacement helpers in E02.
- `c2-checks.json:739–794` separates documentation measurements from production changes and claims no production reduction.

The initial negative-probe failure is explicitly recorded at `c2-checks.json:795`; it is not a pass. These checks were **recorded execution evidence inspected here, not commands independently rerun by this reviewer**.

## Independent exercise judgments

Synthetic source/test results below are **scenario premises**, not newly executed results.

| Exercise | Judgment | Reason and preservation requirement |
|---|---|---|
| **R03** | **needs change** | Factory/registry/abstract class/interfaces only forward unchanged arguments (`c0-review-cases.md:51–57`). Collapse unsupported scaffolding to the existing CSV library/writer, retaining any necessary export entrypoint. Check callers, exact escaping/encoding bytes and affected writer/error contracts. Correct output alone does not justify the platform. |
| **R05** | **meets exercise contract** | Adapter owns required protocol validation and minor→major conversion (`:69–75`). Preserve ingress authentication, forward-compatible metadata and exact supported-currency conversion. Do not delete this meaningful boundary or impose universal unknown-field rejection. |
| **R09** | **needs change** | Compressed names and inline throwing IIFE worsen readability without demonstrated need (`:113–129`). Retain the clear implementation and positive-safe-integer/balance rejection checks. Both functions are pure; no persistence defect is shown. |
| **R10** | **needs change** | `publicAnalytics.send` exports private records outside the approved flow (`:131–137`), violating Q5 and authority boundaries. Remove the unapproved edge; verify actual callers and absence of that disclosure while preserving authorized CSV behavior. Stubbed output tests do not establish privacy. |
| **R11** | **needs change** | Boolean-driven `adjustBalance` mixes distinct charge/refund ownership and contracts without a shared policy (`:139–145`). Restore distinct public operations, retaining the shared low-level writer. Verify callers and existing authorization, rejection and state guarantees for each operation. |
| **R12** | **needs change** | Proposed deletion breaks the registry→lookup→callback route (`:147–162`). Retain handler/registration; preserve dispatch success and ledger-state evidence. No direct-call grep match cannot establish dead code. |
| **R13** | **meets exercise contract** | Schema→existing pricing function→safe response meets the pure-quote requirement without proposed forwarding adapters (`:164–170`). Keep updated rationale and valid/invalid/result checks; do not reintroduce stale-map scaffolding. |
| **E01** | **unverified** | Diagram alone establishes intent, not authorization/failure execution (`c2-review-exercises.md:23–27`). Relabel it; trace actual boundaries/callers and obtain candidate-bound success, denial, failure and preserved-state assertions where relevant. No implemented defect is observed. |
| **E02** | **needs change** | Whole-set totals remain **12 lines / 300 Unicode code points** before and after (`:29–41`). Correct the two-thirds reduction claim to zero reduction. Relocation may still help, but clarity and behavioral preservation are not established by counts. |
| **E03** | **needs change** | With LF included: before **1 line, 5 code points, 6 UTF-8 bytes**; after **1 line, 5 code points, 5 bytes** (`:43–47`). Characters did not decrease, and exact required output changed. Preserve U+00E9 and exact-output verification; these are text samples, not executed programs. |
| **S01** | **needs change — inherited C4 gap; runtime unverified** | Actual source only checks digit shape, admitting zero despite its positive-integer contract. Detailed trace and verification limits follow. This does not require a C2 runtime patch. |

## S01: independent actual-source trace

- `templates/bash/scripts/example.sh:6–10` enables `errexit`, `nounset` and `pipefail`, resolves its own directory and sources the nearby library—not a CLI-selected path.
- `templates/bash/lib/strict-mode.sh:15–21` changes settings in the sourcing shell, sets newline/tab `IFS`, and installs an `ERR` trap writing file/line/status diagnostics to stderr. It does **not** enable `errtrace`; blanket function-error diagnostic coverage must not be inferred. Explicit validation exits are their own rejection path.
- `example.sh:12–18`: `main "$@"` takes the first argument with an empty default, calls `require_positive_int`, then echoes `Starting on port …`.
- `strict-mode.sh:26–33`: `require_arg` rejects missing/empty values with a named stderr diagnostic and `exit 1`.
- `:38–46`: `require_positive_int` delegates presence checking, then rejects anything not matching `^[0-9]+$`. Quoted values are not executed as commands.
- Effects observed in source are shell settings/trap/functions, stdout/stderr and process termination. **There is no listener-starting operation, network effect or persistent state write.** Output wording proves none.

**Inherited contract gap:** `"0"` and `"000"` satisfy the sole regex and presence check. Digit-only shape therefore does not establish positivity (Q1/Q5). The smallest C4 correction is a positivity check without introducing overflow-prone conversion; preserve useful diagnostics and deliberately specify leading-zero semantics. Any actual port-range requirement belongs to the caller’s established domain contract, not an invented universal helper rule.

**Written tests:** `example.bats:17–62` covers missing/empty/nonempty arguments, alphabetic rejection, `8080` acceptance and three CLI paths. Some failures assert only status. No zero/all-zero, negative, mixed-numeric, numeric-limit or trap behavior cases are written. Test setup also sources the process-mutating library (`:12–15`).

**Required C4 evidence:** run candidate-bound Bats and ShellCheck on assembled shipped files in the designated suitable environment. Observe valid-positive acceptance, zero/negative/malformed rejection, correct diagnostics and absence of success output on rejection; verify supported error/trap behavior. No Bash/Bats execution was observed here.

## Remaining limits

No scripts, product tooling, installers or VM operations ran. No oracle or prior independent verdict/report was read. No repository file, metadata or HANDOFF was modified. Recorded check execution and fingerprints were inspected, not independently reproduced. C2 clearance establishes neither runtime fitness, whole-kit acceptance nor publication/enrollment authority.