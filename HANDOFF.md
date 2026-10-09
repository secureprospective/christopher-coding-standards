# HANDOFF

## Baton
Bee · 2026-10-08 · approved rebuild underway.

## Where it stands
Branch `rebuild/quality-core-2026-10-08`. C0/C1/C2/C3/C4 accepted; C4 is the first runtime overlay (Bash).17Bats tests, real Make/lint/format/hook/path/setup-failure checks passed on final copied source; fresh review CLEAR. Core/consumer templates, other overlays, workflows/root security configuration and fixtures unchanged by C4. No complete-kit release or publication.
Current evidence: `docs/planning/c4-acceptance-result.md`; earlier C0–C3 results. Frozen scope/candidate notes and `docs/planning/RESUME.md` are historical, not current progress.

## Next move
C5: TypeScript dependency/security/test compatibility. Reverify current advisory/fixed-version facts before selecting versions. Establish actual package-manager/lockfile and dependency compatibility on a copied fixture, with intended positive/negative checks and fresh review. C6/C7/C8 depend on accepted TS.

## Test environment
Christopher approved isolated tests on ClaudeOS, preserving computer-use setup. Profile `ssh claudeos`, user `claude`, Debian13/KVM. Owned workspace/provenance: `docs/planning/evidence/c3-vm-environment.json`, `docs/planning/evidence/c4-environment.json`. C4 selected Bash5.2.37/ShellCheck0.11.0/shfmt3.13.1/Gitleaks8.30.1/Bats1.14.0/pre-commit4.6.2; Python3.13.5. No sudo/global packages/system/GUI/config changes. Do not use old test@localhost profile or run product tests on Beelink.

## Blocked / limits
No C4 blocker. C5 tools/compatibility/commands still need establishing. Initial C4 pip/default Go caches were not confined; leave existing shared caches/initial SDK artifact untouched. Final Bash uses verified native Gitleaks system hook, not the checksum-unverified Go bootstrap. Subsequent child process caches are task-owned. Other versions/platforms, all-overlay fitness, containment and hosted enforcement remain unverified; tracking/publication/consumers/fleet decisions remain separate.

## Findings carried forward
C9: Go negative fixture suppresses advertised errcheck violation; prove intended diagnostics, not arbitrary failure.
C5/C12: npm-ci conflicts with pnpm-only consumer snippets; align installation/lockfile contract without bypassing guards.
C12: legacy fixture workflows suppress diagnostics/accept arbitrary nonzero; new checker/overlay does not fix wiring by existing.
C4 limits: ERR has Bash context suppression; only regular .sh discovery, so symlink targets require deliberate project coverage; harmless custom scanner rule proves wiring, not full default secret policy. Staged hook scanning is not whole-tree scanning.

## Rejected
Workflow-first machinery, worktree-as-sandbox, green skipped checks as verification, blind size/DRY quotas and code-golf. Existing ownership/publication/credential safeguards remain live; no publisher/App/broker, deployment or consumer rewrite authorized.
