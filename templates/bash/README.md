# Bash overlay

Copy and customize Bash boundary helpers, shell lint/format configuration and Bats examples. Use the shared quality contract and existing project idioms. This is not a shell sandbox, automatic adoption or proof of hosted enforcement.

## Units and ownership

| Unit | Purpose |
|---|---|
| `.shellcheckrc` | Bash mode, source resolution and five explicit optional checks; not all possible correctness/security checks. |
| `.pre-commit-config.yaml` | Pinned ShellCheck/shfmt/Gitleaks hooks. Merge with existing controls; configured hooks are not execution evidence. |
| `Makefile.snippet` | GNU Make/Bash/find/xargs lint, format and test recipes. Merge deliberately; preserve existing targets/settings. |
| `lib/strict-mode.sh` | Required-value and positive-decimal validation; process-owned strict options, IFS and ERR diagnostic trap. |
| `scripts/example.sh`, `tests/example.bats` | Reference CLI and real helper/integration assertions; adapt to the actual project. The example prints, it does not start a listener. |

Source the library only where its process-wide options/IFS/trap are appropriate. It replaces an existing ERR trap; do not blindly add it to a host shell, test driver or recovery-oriented library. Tests source it in a child Bash, not the Bats driver.

## Boundary contract

`require_arg NAME VALUE` accepts nonempty strings, including spaces/zero; missing/empty VALUE prints a named diagnostic to stderr and exits1.

`require_positive_int NAME VALUE` accepts ASCII decimal strings representing positive integers, including `08`/`0001` and values larger than machine integers. It rejects empty, all-zero, signed, fractional, exponent and malformed strings. Validation uses a nonzero-digit pattern, not arithmetic/octal conversion. It preserves the supplied string; no range or canonicalization is imposed. If later code requires bounded arithmetic, a real port range, authorized path or permission, validate that caller-specific contract separately.

Helpers terminate the calling process on rejection; they are not recoverable predicates. NAME is a caller-supplied diagnostic label, not external input. Never interpolate external values into shell commands, source paths or eval strings; quote argument expansions.

## Setup and adoption

1. Identify the owner-approved project/environment and existing checks/package/config rules. Install chosen trusted tool versions there, preferably in an isolated test workspace; record source identity/integrity. No automatic sudo/global install or computer-use changes.
2. Merge `.shellcheckrc`, selected pre-commit hooks and Makefile recipes. Copy/adapt the library/example/tests into actual project locations. Retain source-path comments if needed for static resolution.
3. Adapt the CLI pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/strict-mode.sh
source "${here}/../lib/strict-mode.sh"
require_positive_int "count" "${1:-}"
# Actual authorized work follows validation.
```

4. Run `make lint` and `make test` on the assembled copy. `make fmt` writes formatting changes; inspect them, then rerun lint/tests. Bats DSL is outside these `.sh` lint recipes; its behavior is exercised by Bats. GNU NUL-delimited discovery selects regular `.sh` files, preserves spaces/newlines/metacharacters in names, prunes `.git`/`node_modules`, and propagates discovery/tool failures. Symlinked scripts are not followed/checked; assess their real targets/ownership and adapt coverage explicitly rather than silently dropping a project's existing link-based checks. An empty `.sh` set is explicitly unverified, not a green tool run.
5. In a disposable Git copy, run `pre-commit run --all-files` with the copied hook configuration and a task-owned cache. Activate `pre-commit install` in a real project only under its owner's authority. Recheck actual runtime loading/coverage; hooks may not be installed or may be bypassed outside this procedure. This overlay grants no bypass permission.

Pinned sources retain ShellCheck wrapper0.11.0.1 (native0.11.0), shfmt3.13.1 and the Gitleaks8.30.1 hook definition. `gitleaks-system` requires an owner-installed verified Gitleaks binary on PATH (selected/tested8.30.1); the hook does not pin that binary automatically. It avoids the default hook's implicit unpinned Go SDK bootstrap. Resolve the full configured commits against intended official repos when selecting/updating dependencies; tags/hash text alone are not trust or compatibility proof. Do not blanket-upgrade or remove guards to manufacture green.

## Error behavior and limits

Sourcing enables `-Eeuo pipefail`; ERR is inherited into ordinary functions/subshells. Eligible failures report failing source file/line/status to stderr, without converting failure into success. Required-value/positive validation emits its own explicit exit1 diagnostic.

Bash suppresses ERR/errexit in handled conditions, including functions invoked in `if`/`&&`/`||` contexts. Pipelines, command substitutions and subshells have additional context rules; `-E` is not universal exception handling or a guarantee every failing subprocess aborts its caller. Explicitly inspect statuses where the contract needs it. Internal CLI diagnostics are not safe external API responses by default.

## Verification, not historical claims

Bats observes zero/negative/malformed/positive/leading-zero/large values, absence of success after rejection, literal metacharacters, original failure status/location and handled conditions. Run the actual copied tests; their presence alone proves nothing.

Verify lint/format on clean copied inputs and harmless deliberate violations in a separate disposable tree: ShellCheck must identify the intended rule, shfmt must produce the intended formatting diff, and no missing-tool/config error counts as either result. Keep failure output, exact candidate/config/lock identity and tool versions. Do not try to commit broken scripts or plant real credentials. The Gitleaks hook scans the staged Git diff, not the filenames selected by `pre-commit --all-files`; an empty staged diff is not a whole-tree scan. Use an explicit directory scan to check a full copied tree. A clean scan is not proof every possible secret would be detected; assess selected rules/exclusions with authorized non-secret test data separately.

Current rebuild evidence/status lives in the kit's HANDOFF and C4 records, not old phase checkmarks. Verification is candidate/environment-specific; no universal version/platform compatibility, total security, CI enforcement or publication authority is implied.
