# Canonical GitHub authority/workflow audit — 2026-10-08

## Verdict

**Do not activate autonomous push/draft-PR corridor yet.** Main has real status-check protections, but zero approving reviews are required, no mandatory code-owner review protects policy files, the current CLI credential has repository administrator access, and two required checks succeed without running their substantive TypeScript gates. Existing Python/Go/Bash fixture jobs execute successfully but are not required for merge.

This is an observed configuration audit, not an exploit test or proof any agent bypassed a control. It supplies planning requirements; it changes no authority or hosted setting.

## Scope, methods and evidence

Christopher explicitly authorized a read-only audit of the canonical standards repo's protections/rulesets, required reviews/checks, bypass permissions and push/PR workflow security. Consumers and fleet machines were not audited.

Target: `secureprospective/christopher-coding-standards` (public, personal-account owned), default branch main. Local and remote main both at `93ee82a346289f7fdf77a696a20a999ffcc61dc6`; remote rechecked at end. Existing local changes remained only untracked `.project.yaml` and parent-created `docs/planning/`.

Used installed native GitHub CLI 2.102.0, explicitly GET requests only, using its existing authentication. No raw credential file/token was read or printed. Response scope names and effective repo permissions were inspected, not credential values. No test/workflow triggered, branch created, PR changed, protection changed, credential changed, consumer touched, commit or push performed.

Evidence observation began `2026-10-08T21:15:52.732586+00:00`. Minimized API evidence: `~/scratch/coding-standards-github-audit-2026-10-08.json`, SHA256 `26e7c54a0e9d2896336e1847bdc637f75cda807d4116db3126788ff2aea9fbf3`. It records 20 API endpoint observations including five run/job-step inventories; two additional GETs confirmed repository metadata and final remote main. Public response payloads were minimized to settings, permission/scope names, refs, job identities/conclusions/steps and PR state; unnecessary PR bodies/profile/commit metadata and credential values are not retained.

Audit collector: `~/scratch/coding-standards-github-readonly-audit.py` (one-shot diagnostic, NOT proposed production tracker). Source inspection used committed workflow/config files at the same main SHA. Public upstream action metadata was fetched read-only to verify Semgrep image and checkout default behavior; current mutable tags are not proof of the exact historical action code used in older runs.

## 1. Hosted protection: observed state

`GET /repos/secureprospective/christopher-coding-standards/branches/main/protection` returned HTTP200.

| Control | Observed | Consequence |
|---|---|---|
| Required checks | Five contexts below; each bound to GitHub Actions app ID15368 | Names/app origin are constrained, but not an independent policy verdict or full template proof. |
| Strict/up-to-date check requirement | true | Helpful base freshness control. |
| Approving review count | **0** | Independent human approval is NOT mechanically required by this count. PR-review configuration exists; do not infer an actual direct-push bypass from this audit. |
| Dismiss stale approvals | true | Configured, but no minimum approval required. |
| Require code-owner reviews | false | No protected-owner review requirement for policy/workflow edits. |
| Require last-push approval | false | No independent latest-push approval required. |
| Enforce admins | true | Current protections apply to admin actions while intact. Administrator authority can still change settings; no mutation tested. |
| Linear history | true | Configured. |
| Force pushes | false | Prohibited on main. |
| Deletions | false | Prohibited on main. |
| Signed commits | false | Not required. Signatures would not prove code correctness/approval anyway. |
| Conversation resolution | false | Not required. |

Required contexts:
- `secrets — gitleaks`
- `sast — semgrep`
- `sca — trivy`
- `ts — lint`
- `ts — test`

Repository rulesets query, including parents, returned an empty list. Effective ruleset queries for main and a hypothetical `agents/audit-scope-probe` name also returned empty lists. **This does not mean main is unprotected:** classic branch protection exists independently. The hypothetical GET created no branch and proves no push authorization. Current branches: ten; main protected, nine others unprotected. No actual `agents/` namespace exists in this inventory, and no namespace-specific rule is returned by the ruleset API.

No CODEOWNERS file exists at `.github/CODEOWNERS`, root `CODEOWNERS` or `docs/CODEOWNERS` in the inspected main tree. Review labels/receipt fields alone cannot fill this missing enforcement.

## 2. Current authentication versus agent authority

The API credential available through this session's GitHub CLI reports repo permissions: admin, maintain, push, triage and pull all true. Returned OAuth scope names: `gist`, `read:org`, `repo`, `workflow`, `write:packages`.

**Important distinction:** this is the workstation/session credential, not the ephemeral Actions GITHUB_TOKEN. No credential value was exposed or changed. Scope names plus repo admin permission show that the available credential is broader than a push/draft-PR-only corridor; they do not prove every API operation was exercised.

A grant naming `agents/<task>` cannot technically restrict a credential with this authority by itself. The design must specify a genuinely separated/bounded identity or trusted broker and protected integration controls. A narrower repo token alone may still permit merge or workflow edits; verify exact permission semantics rather than asserting fine-grained tokens implement per-branch/per-action intent automatically.

Auto-merge is disabled, but that is not a mechanical human-only manual-merge boundary. No agent-specific principal, namespace enforcement, readiness restriction or human-only acceptance boundary was proven.

## 3. Configured checks versus observed execution

Four workflows are active in GitHub. Sampled latest20workflow runs all completed successfully. Source HEAD checks include successful scanner, conditional-language and fixture jobs. These are GitHub's observed historical outcomes, NOT newly rerun tests or a universal quality/security guarantee.

Key run evidence:
- Security schedule at exact HEAD, October5: https://github.com/secureprospective/christopher-coding-standards/actions/runs/37321377412
- Security push at exact HEAD, October3: https://github.com/secureprospective/christopher-coding-standards/actions/runs/37146041298
- Bash fixtures at exact HEAD: https://github.com/secureprospective/christopher-coding-standards/actions/runs/37146041244
- Go fixtures at exact HEAD: https://github.com/secureprospective/christopher-coding-standards/actions/runs/37146041230
- Python fixtures at exact HEAD: https://github.com/secureprospective/christopher-coding-standards/actions/runs/37146041227

**Confirmed no-op required checks:** security push and schedule job-step APIs show `ts — lint` and `ts — test` concluded success while Node setup, dependency installation, Biome, typechecking and tests were **skipped**. Their root configs are absent. `astro — check` similarly succeeded with substantive steps skipped, but it is not a required context.

Scanner execution steps for Gitleaks, Semgrep and Trivy were reported successful in sampled security runs. No raw logs/SARIF/findings were downloaded, so scan coverage, warning details, actual resolved tool/rule identities and exploitability are not independently established.

Python/Go/Bash fixture job APIs show their clean and negative fixture steps actually executed successfully. **None of these three contexts is in main's required-check list.** They can detect problems without themselves being a configured merge requirement. Current negative fixtures also count arbitrary nonzero exits as rejection; expected diagnostic attribution remains a source-level gap. All seven overlays still lack comprehensive fixture proof.

Legacy commit-status API returned pending with zero statuses; separate check-run evidence is populated. Do not mistake absent legacy statuses for failed or absent Actions checks.

## 4. Actions settings and workflow event surface

Observed hosted Actions settings:
- Enabled: true.
- Allowed actions: **all**.
- SHA pinning required by hosted policy: **false**.
- Default workflow token permissions: **read**.
- Workflows may approve PR reviews: **false**.
- External fork approval policy: `first_time_contributors`, not all external contributors.
- Selected-actions endpoint returned409Conflict, consistent with allowed_actions=all; it did not supply a restricted allowlist. No global API-access failure occurred.

Source at HEAD:
- All four workflows trigger on `pull_request` targeting main/develop and `push` to main.
- Only security has weekly scheduled trigger.
- No `pull_request_target`, `workflow_run`, `workflow_dispatch`, deploy job or environment declaration appears in these four files.
- Current `agents/*` pushes do not match push:[main], but opening/synchronizing a PR targeting main triggers the pull_request workflows. There is no draft guard in the inspected job definitions; draft is not a no-execution boundary.
- Template fixture workflows explicitly set contents:read.
- Security workflow grants contents:read, pull-requests:read and **security-events:write** at workflow scope, so scanner/language jobs inherit more than a read-only baseline; narrow to necessary job/use if adopted.
- Only secrets.GITHUB_TOKEN is explicitly referenced in source. This is NOT proof no repository secrets, organization integrations or other credential pathways exist; secret inventories were outside scope.

Good controls: no privileged pull_request_target pattern in inspected files, explicit read contents permissions, hosted default read and no GITHUB_TOKEN PR-review approval. These do not restrain the admin workstation credential.

## 5. Supply-chain and source-policy risks

- 18 third-party action uses across four workflows: six literal40-character SHAs, **12 mutable references**, all in security.yml. Hosted policy permits them.
- Semgrep v1 action metadata currently invokes mutable Docker image `returntocorp/semgrep-agent:v1`; observed job API names confirm that image tag was pulled. Pinning only action wrapper would not fix the mutable image/rules dependency.
- Semgrep p/security-audit, p/secrets and p/owasp-top-ten registry packs are not tied to reviewed content digests in this source. Dynamic rules/advisory data can be intentional but need a documented trust/update policy.
- Verification jobs execute exact-version downloads for ShellCheck/shfmt/Gitleaks without literal digest verification; golangci tarball has a literal SHA256 check. Python installs ruff/mypy exact top-level versions without hash-locked transitive requirements; Go analyzer uses its own go.mod/go.sum. Action pins do not completely pin the execution graph.
- No checkout step sets persist-credentials:false. Current official checkout v4 metadata says default true: authentication is configured in local Git state during execution. Exact resolved checkout version/credential exposure in each historical run was not inspected. Restrict privileges and persistence where appropriate, not merely report absence of token text in a workflow.
- `.gitleaks.toml:16–20` broadly allowlists README/docs Markdown. A successful secret scan does not prove those distributed instructions/logs were scanned. Narrowing exclusions requires its own reviewed migration and positive/negative tests.
- Required context binding to GitHub Actions is useful, but does not authenticate a particular trusted workflow implementation. Without protected workflow/config ownership, check logic could be weakened in a candidate branch while still publishing the expected context. This is a design risk, not a tested attack.

Primary action metadata inspected:
- https://raw.githubusercontent.com/semgrep/semgrep-action/v1/action.yml
- https://raw.githubusercontent.com/actions/checkout/v4/action.yml

Repo-relative source evidence: `.github/workflows/security.yml:3–9,31–79,82–160`; `.github/workflows/verify-templates.yml:21–28,52–58,99–117`; `.github/workflows/verify-templates-go.yml:13–20,44–52,95–123`; `.github/workflows/verify-templates-bash.yml:16–23,43–58,102–118`; `.gitleaks.toml:16–20`.

## 6. Planning implications / recommended order

These are proposals only. No settings or credentials changed.

1. Keep autonomous external corridor inactive under current credentials/settings. Draft an authority model with separate tested candidate, commit, push/draft PR and human accepted integration states.
2. Select a bounded agent identity/credential or broker design that does not expose owner admin/workflow authority to ordinary tasks. Verify how human-only merge/readiness and branch namespace controls would actually be enforced; do not promise per-branch token restrictions without proof.
3. Establish genuine independent human acceptance and protected policy/workflow/receipt review, accounting for administrator/control-plane privileges. CODEOWNERS alone is not sufficient unless protected review requirements actually apply.
4. Align required checks with meaningful canonical-repo gates. Make existing Python/Go/Bash fixture contexts required if approved; replace irrelevant green TS no-ops with actual shipped-template validation/applicability evidence. Expand remaining overlays through isolated fixtures.
5. Harden Actions permissions, immutable supply-chain identities/checksums, scanner scope and hostile-PR behavior as bounded reviewed changes. Do not roll all upgrades together.
6. Resolve minimum local execution/credential/egress boundary before claiming corridor safety. This audit did NOT test that boundary.
7. Build the read-only tracking schema/checker only under separate implementation approval; source freshness, protected acceptance and gate execution remain independent states.

Do not enroll consumers, create namespaces, enable rulesets or alter hosted protection simply to make this proposal pass. One variable at a time, with owner approval and observed acceptance tests.

## 7. Remaining unknowns and limits

- No branch creation/push/merge/readiness/bypass operation was attempted; documented/effective API permissions are not tested exploits.
- No live OS sandbox, Pi/child permissions, network denial, secret exposure, credential storage or agent-specific identity baseline inspected.
- No secret inventory, integration/webhook/deploy-key audit, raw logs or SARIF finding review; no assertion of complete credential/security inventory.
- No mutation/compatibility tests run; seven-overlay safety is not established by historical green jobs.
- No consumer/fleet protections investigated; audit cannot generalize to TheWarRoom or TFM.
- GitHub controls can change after observation; approved rollout must revalidate current actor/settings/ref.

Original dossier, advisor file, operational standards, hosted configuration and consumer files remain untouched. Only Bee-owned audit/evidence/planning artifacts were added/updated. Current audit is not authority adoption.
