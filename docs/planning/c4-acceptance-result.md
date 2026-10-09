# C4 acceptance result — Bash

**Accepted for this bounded overlay on the tested environment.** Owner: Bee. Date: 2026-10-08. Current progress: `../../HANDOFF.md`.

Base: C3 local `5761c15`, branch `rebuild/quality-core-2026-10-08`. Frozen `c4-candidate.json` SHA256 `c8999c338a34f1d14bd8c9bac5d00541ada0aa9356a35fa3c5ec4c00aa83a8e2`,32inputs. Fresh read-only reviewer `2042cf7e-15b7-40e0-b484-09d8a7d0dade`: **CLEAR, no issues found**. Preserved report `evidence/c4-independent-review-2026-10-08.md`, SHA256 `cee4bd648d39d725b9a3100eb7f20f6018c6fbb16f0b1432ed5259654222b0d1`.

Bee verified all32frozen inputs,155protected tracked files, tracked-diff/session-helper hashes and unrelated `.project.yaml` unchanged after review. No candidate mutation during review. HANDOFF is progress-only outside explicit frozen source inputs; post-gate edits are closure/report records only. Reviewer clearance is evidence, not merge/publish authority.

## Established behavior

- Positive-decimal helper rejects zero/all-zero, negative, malformed and missing inputs. Existing positive digit strings, including leading zeros and201-digit values, remain accepted without integer/octal conversion. Required-value helper still accepts nonempty strings and explicitly exits1 on missing/empty values.
- Rejected reference CLI emits useful diagnostics without its success output. Literal shell metacharacters remain data; the observed marker file is not created. The example prints, not starts a listener.
- Eligible top-level/function/pipeline failures retain tested status7 and accurate source/line diagnostics. Errtrace is enabled; handled command/function conditions remain handled. Library process-wide options/IFS/ERR ownership and Bash suppression limits are explicit.
- Bats calls the actual copied library in child Bash, not mocks or the test driver. All17test methods pass on the final copy.
- Make lint/test/fmt and standalone ShellCheck/shfmt pass on clean shipped inputs. Intended violations produce actual SC2086 or formatting diff/modification. Empty source sets, missing tools and traversal errors fail rather than silently pass. NUL/argv handling works for space/newline/metacharacter names and a space-containing project root.
- Actual pinned hooks install/run in a disposable Git fixture; ordinary clean commits run the installed hooks. Lint/format negative probes fail correctly; no broken-code commit or hook bypass. Gitleaks-system uses the verified native binary with pass_filenames:false, avoiding implicit Go bootstrap. A harmless custom-rule staged sentinel rejects at that scanner; missing native binary fails setup. Whole-directory clean scan is recorded separately from staged-diff scanning.

Environment: operator-authorized isolated ClaudeOS, Debian13.7/KVM, Bash5.2.37, ShellCheck0.11.0, shfmt3.13.1, Gitleaks8.30.1, Bats1.14.0, pre-commit4.6.2, GNU Make4.4.1. Native archive digests/Bats source identity/PyPI bootstrap hashes were checked; no sudo/global package/system/GUI/config change.14preserved VM artifacts match remote hashes in `c4-vm-evidence-manifest.json`. Final records `evidence/c4-final-candidate-checks.json` and `evidence/c4-final-additional-checks.json` bind all7current copied files.41links, source scope, protected bytes and affected root/minimal-consumer routing checked.

## Failure disposition and scope

Pre-repair positivity tests4/8/10 failed for the known zero contract; the string-pattern change yielded12passes. ERR tests13/14/15 exposed line0/missing function diagnostics; formatter correction left14, then errtrace correction yielded17passes. These historical phases are not current passes.

The initial legacy Gitleaks hook bootstrapped an unpinned/checksum-unverified Go SDK. It is an unused historical test artifact, not retroactively verified or required by the final system hook. Initial pip/default Go caches were not explicitly confined; existing caches/SDK artifacts were left untouched, and subsequent process caches are task-owned. No pristine-VM claim.

The first system-hook trial failed because its upstream manifest passed filenames to a staged-repository scanner. The actual CLI failure is preserved, not counted as intended rejection. Explicit pass_filenames:false fixes that interface; affected and full final-copy checks reran successfully.

Checkpoint hygiene incident: the full staged whitespace check flagged two intentional Markdown two-space hard breaks at lines3/4 of the byte-preserved independent report. The outer shell lacked fail-fast chaining and still created local source checkpoint `e6ce2b3` after the Python check raised CalledProcessError. This sequencing mistake is not a passed check. With strict shell fail-fast enabled, all29other committed paths then passed `git diff --check HEAD^ HEAD`; the report was separately verified to have only those two valid hard breaks and its original SHA256 unchanged. No runtime/source defect or hook bypass occurred. This closure record is a follow-up metadata correction; reviewed source and evidence are unchanged.

Only Bash and two root status routes changed. Root status now follows HANDOFF, avoiding stale C1-era all-overlay language. Core/consumer templates, other overlays, workflows/root security configuration and fixture sources are byte-identical. No guard removed, blanket upgrade, graph/platform or consumer enrollment.

## Retained limits / next

Selected Linux/tool versions only; not universal compatibility. Make shell settings require deliberate merging; only regular `.sh` sources are discovered, so symlink targets need project-owned coverage adaptation. ERR is not universal exception handling, and large-string acceptance is not an unlimited-resource guarantee. Caller-specific numeric ranges/authorization remain caller responsibilities.

The custom scanner rule demonstrates wiring, not complete default secret detection. `pre-commit --all-files` does not make the staged-diff scanner inspect an entire tree. Bootstrap lock does not lock every transitive hook environment. Reviewer inspected source/recorded evidence, not rerun commands, recomputed hashes or authenticated downloads; Bee verified identities separately.

No other-overlay, actual CI/hosted enforcement, containment, complete-kit release, publication or live-consumer conclusion. Next C5: TypeScript dependency/security/test compatibility, with current advisory facts reverified and actual package-manager/lockfile contract demonstrated. Go errcheck repair remains C9; workflow traps/install safeguards and npm/pnpm CI alignment remain C12 with C5 input.
