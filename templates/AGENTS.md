# Project instructions

Customize this profile and keep it short. Links resolve from the consumer repo root after copying, not this source-template directory. Do not claim adoption is complete with unresolved placeholders or imaginary checks.

- Project: `[project name]`
- Languages/exposure: `[actual languages; public/internal]`
- Standards source/baseline: `[chosen source revision, or explicitly unknown]` — metadata is not approval or execution proof.
- Verification: `[actual lint/format/type/test/security commands and when applicable]`. Missing relevant checks must be reported unverified, not passing.
- Project-specific constraints: `[real compatibility, ownership and authority rules]`

## Read and act

Read [docs/quality-contract.md](docs/quality-contract.md) for acceptance and [SYSTEM_MAP.md](SYSTEM_MAP.md) for actual components/utilities/state boundaries. Load only the task's relevant project/stack/design docs; do not load a whole historical doctrine by default. Document necessary local differences without silently dropping safety/behavior guarantees.

For an approved task, establish behavior, scope and preservation checks; implement the simplest complete change and resolve routine in-scope feedback. Ask when ambiguity changes behavior, scope, architecture, risk or authority—not for every permitted step. Spec Kit or another specification tool is optional if the project/operator chooses it; never initialize it automatically.

Tests must observe intended outcomes and material failure/state-preservation paths. Use actual configured gates and record results against tested candidate files/ref. Skipped/missing/stale checks and unresolved material failures are not success; do not bypass hooks, weaken tests to get green or commit known-broken operational code. Preserve meaningful failure results and real trust/authorization boundaries.

For material structural work, capture a small initial component/data-flow slice, independently compare actual source/evidence and explain justified changes. No mandatory class/files, diagram per function or size quota. Debloat remains preserving and readable, not code-golf or test deletion. Already-satisfied behavior permits evidenced no-change.

Operator/system instructions and this project's established ownership, commit/push/merge/deploy permissions remain live. These copied instructions grant no new credentials, delegation or publication authority. Preserve other agents' files/work; never force-push or send email without explicit permission. Check source/dependency identity and relevant configured security checks before relying on them; pin third-party CI actions/hooks to immutable refs.
