# Coding standards rebuild — considerations and research log

Date: 2026-10-08
Owner/author: Bee, for Christopher. Status: planning input, NOT adopted standards or permission to build/deploy.

## Authority and inputs

Christopher requested serious rebuild planning: inspect the low-grade-model dossier, log everything worth considering, then commission a third subagent for a thorough accuracy/implementation research pass. The prior tracking-first proposal has NOT been approved. This request authorizes logging/research, not application code, gate changes, consumer enrollment, installations, or fleet-wide changes.

Inputs:
- Operator-supplied dossier: `~/fleet/docs/ai-coding-excellence-dossier-2026-10-08.md`, prepared October 8; 198 lines / 39,639 bytes; SHA256 `43a35ad7a0ab99ec12f9e30a1ceb9d90cfbd53b0a4be07899998a273c5cffe82`. Do not modify this other author's document.
- Canonical repo: main `93ee82a346289f7fdf77a696a20a999ffcc61dc6`, pull up to date. Pre-existing untracked `.project.yaml` untouched. No current HANDOFF.md.
- Prior recon: `~/scratch/coding-standards-recon.md`.
- Overlay proposal: `~/scratch/coding-standards-overlay-audit.md`.
- Tracking investigation: `~/scratch/coding-standards-update-mechanism-investigation.md`.
- Existing contracts: `docs/adr/0001-why-this-standard-exists.md`, `docs/multi-agent-roles.md`, `AGENTS.md`, `docs/INDEX.md`.

Paths above identify local investigation inputs; eventual distributable standards must not depend on machine-specific paths. This new planning doc lives under existing docs/, not a new top-level directory. It is not an operational instruction entrypoint. Existing index/ADR/governance files are deliberately not rewritten during this research pass. At integration, explicitly decide which planning artifacts belong in the task index versus archive; do not auto-load a large research log into every coding session.

## Evidence handling

The dossier contains plausible principles and numerous precise claims. Its authorship/model grade is not evidence that an individual claim is true or false. Treat all R1–R18 research claims and D1–D13 capability claims as UNVERIFIED until primary sources are checked. Separate observation, external evidence, proposal, and operator decision. An inaccessible source is unverifiable, not disproven. A citation containing the right words is not sufficient if its population, denominator, method, or dates do not match the claim.

Parent already independently verified the Vitest medium-severity advisory GHSA-82fw-gwwq-j7x9: stable affected versions >=2.1.0,<4.1.11, stable fix 4.1.11; and official npm deprecation of the Workers pool package in favor of @cloudflare/vitest-plugin. These are separate from the dossier's research statistics. No exploit reproduction, compatibility test, or full security inventory was run.

## A. Accuracy and research methodology — investigate before policy

| ID | Consideration / gap | Required research or disposition |
|---|---|---|
| E01 | R1–R18 may have mismatched titles, authors, dates, versions, measurements, or unsupported conference claims. | Check identity/first submission/revision and material claims against primary text; record exact sections/table/passages and status per citation. |
| E02 | Recent publication can describe old artifacts/models. | Preserve collection dates, tested models/harness versions, task types, and any human intervention. Never use historic sample prevalence as today's fleet rate. |
| E03 | Reported rates can be conditional on detected incidents, passing runs, reviewed PRs, or static taxonomy findings. | Verify denominators, units, overlapping classes, missing outcomes, sample selection and whether conclusions are observational/causal. In particular inspect R2 91.49%, R4 80.2%, R5 10.7%, R15 15.4%, R16 91.8%. |
| E04 | R14 register labels arXiv 2608... as July 31; metadata conventions alone cannot resolve date correctness. | Distinguish first submission, announcement, revision, and publication; report discrepancy only with source evidence. |
| E05 | Six-month-only cutoff is a dossier choice, not an operator instruction. It may omit foundational sandbox/injection/testing/update evidence. | Prioritize current material, but include earlier directly relevant primary evidence with dates; do not discard useful established controls solely by age. |
| E06 | Named authors/official docs do not by themselves prove human authorship or independent empirical validation. | Do not claim a source's human-only authorship without proof. Identify vendor reports, preprints, position pieces, datasets, and controlled experiments distinctly. |
| E07 | Negative instructions allegedly outperform positive directives (R8) in one setting; architecture-context exclusions in current ADR make similarly broad leaps. | Verify effect sizes, settings, task types and tradeoffs; no universal negative-only instruction law or automatic removal of useful project facts. |
| E08 | R9 skill harms and R16 defect taxonomy are not proof all skills regress quality or are malicious. | Verify attribution method, routing failures, efficiency overhead and taxonomy; evaluate applicability to a specific installed skill. |
| E09 | Existing ADR says all current LLMs are less secure than human code and that free tooling covers the same gates as paid offerings. | Audit universal/comparative claims and original citations before retaining; capability equivalence, incidence and guarantee are different. An ADR change needs an explicit superseding decision, not silent edits. |
| E10 | D1–D13 rolling URLs may describe unavailable/different products, APIs, release channels, or plans. | Verify exact surface/version/platform, enforceability, permissions and licensing. Codex plugins, API environments, CLI hooks, Copilot CLI and IDE agents are not interchangeable. Check whether MCP skills spec is stable/experimental and whether the deployed harness implements it. |

## B. Requirements, workflow and autonomy

| ID | Consideration / gap | Candidate design/evidence needed |
|---|---|---|
| P01 | Define what 'best possible' optimizes before locking architecture. | Proposed evaluation dimensions: correct intent/behavior, security, recoverability, maintainability, autonomy with bounded authority, human attention, latency and total tokens/cost. Ask Christopher which tradeoffs matter; lower tokens must not silently lower safety. |
| P02 | Make no-change a valid outcome without demanding a bug reproduction for every new feature or docs task. | Bug fixes: current-state reproduction or explained limitation; new work: inspect whether acceptance behavior already exists. Reproduction must not require running untrusted code on host. |
| P03 | Task contract should be small and task-sensitive, not twelve gates pasted into every conversation. | Behavior/acceptance/scope/risk/authority; reference static policy by ID and load relevant procedures lazily. Request approval only for material ambiguity or scope changes, not each permitted mechanical action. |
| P04 | 'Smallest patch' and fixed file/dependency budgets can encourage underimplementation or fragmented code. | Preserve complete acceptance behavior and adjacent regression checks. Use scope budgets as review signals, with explicit necessary exceptions; do not penalize legitimate migrations. |
| P05 | High-risk classification is useful but must have an executable trigger/owner, not just a list. | Auth, secrets, payment/privacy, migrations/deletion, infrastructure/network, dependency/build scripts, untrusted execution, policy/updater changes; assess privilege and blast radius. File paths alone miss indirect changes. |
| P06 | Human acceptance and external-write permissions are policy choices, not empirical laws. | Preserve Christopher's authority and email prohibition. Define separate permissions for local writes, branch/commit/push, PR, merge, deploy, irreversible changes; batch approvals only within declared scope. |
| P07 | Current single-vendor Builder and exclusive git prose conflicts with today's approved subagents and reports. | Design capability/ownership-based roles: one writer per shared seam/worktree, parent integration/acceptance, bounded independent review, collision prevention and durable handoff. Do not infer fleet topology from old docs. |
| P08 | Different model/context can improve review independence, but is not assurance by itself. | Reviewer should inspect actual diff/state and independent acceptance oracle, not simply repeat generator claims. False positives require triage; no agent can waive human/security approval. |
| P09 | Coding-quality checks don't cover all product requirements. | Task-sensitive observability, errors, performance/resource limits, accessibility, privacy and operational recovery checks; avoid mandatory logging for trivial/pure code or sensitive-data leaks in logs. |
| P10 | 'No new production dependency' can be overrestrictive; current ~15-line native heuristic can promote risky bespoke security code. | Dependency decision considers maintenance, correctness/security, transitive exposure, licensing, ecosystem support and scope—not line count alone. |

## C. Containment, extensions and hostile inputs

| ID | Consideration / gap | Candidate control / validation |
|---|---|---|
| S01 | Dossier groups worktrees with sandbox isolation. A worktree isolates Git changes, NOT host filesystem, process, network or secrets. | Separate concurrency isolation from security containment. Verify OS/container/VM boundaries with canary deny tests and record actually active policy/platform. Never call worktree-only execution sandboxed. |
| S02 | Instructions, hook outputs, MCP metadata, downloaded docs and repo files can be attacker-controlled. | Explicit trusted policy chain; untrusted content is data, not permission. Enumerate protected paths and policy bypass risks; prefer argv execution, constrained network, credentials outside execution boundary. |
| S03 | Agents/build/test code can read environment variables and mounted homes even when model tools deny direct reads. | Threat-model subprocesses, installers/build scripts, credential helpers, SSH agents, Docker socket, caches and network egress. Restricted tooling is not sufficient if bash has broad capabilities. |
| S04 | Hook enforcement and failure modes are runtime-specific. | Verify deny/block semantics, return codes, async timing, fail-open/fail-closed and emergency behavior per deployed harness. Completion hooks are not always pre-action authorization. Scope this first to actual Pi/Claude execution, not every marketed runtime. |
| S05 | Pinning protects identity, not safety; opaque action SHAs and fetched scanner rule bundles need review/update channels. | Record source, artifact digest, approved provenance, dependency/endpoint/tool authority, owner and rollback. Address transitive dependencies, rulesets/config downloads and compromised releases, not just top-level tags. |
| S06 | New MCP/skill/hook must not auto-activate from instructions or receipts. | Separate discovery from activation; signed/checksummed source is still untrusted behavior. Consent, least-privilege scope, schema/payload validation, size/time limits, logs and revocation. |
| S07 | Security checks can leak data or execute PR-controlled configs with elevated tokens. | Read-only/minimal CI tokens, fork-event handling, no privileged pull_request_target execution of untrusted code, no production secrets in fixture jobs, bounded scanner outputs/artifact retention. |
| S08 | Severity-only gate overlooks medium findings with real exposure and medium-risk dependency examples such as Vitest. | Combine severity, applicability/exploitability, reachability, provenance and blast radius; track existing vs new findings. Exceptions: named owner, rationale, compensating controls and expiry. No automatic allowlisting to make checks pass. |
| S09 | Free-tooling-first is an accepted repo invariant, while some CodeQL/dependency-review/private-repo capabilities have license/plan conditions. | Check actual licensing/private-repo use and network/offline requirements. Keep documented free fallback; do not promise equivalent detection or require paid SaaS without operator decision. |
| S10 | Credential redaction is insufficient if stored traces contain private code, prompts or tooling details. | Minimum evidence, access/retention/deletion policy, redact before persistence, separate artifact secrets from agent-accessible data. Trace collection itself requires a threat model. |

## D. Behavior evidence, gates and evaluation

| ID | Consideration / gap | Candidate verification / limits |
|---|---|---|
| V01 | Test presence/coverage count does not prove intended behavior; syntactic assertion scanning cannot solve oracle quality. | Expected observable result, failure path, no mocking the behavior under test by construction, independent oracle review; review test changes and justified expectation changes. |
| V02 | Tests legitimately change when behavior changes. | Prohibit unjustified weakening for green, not all changed/deleted assertions. Independently approve replacement acceptance behavior, fixture migrations and intentional compatibility changes. |
| V03 | Stronger tests must be proportionate. | Critical boundaries: integration/contract/property/fuzz/mutation; quick targeted checks during iteration, comprehensive applicable merge CI. Universal mutation or whole-fleet five-run gates can consume large time/tokens without corresponding risk reduction. |
| V04 | Existing universal 80% coverage and length gates conflict with behavior/risk doctrine. | Keep coverage as an explicitly scoped floor/signal if useful; no proof-of-quality claim. Responsibility/complexity checks and meaningful tests over arbitrary slicing. Operator must resolve Bun 300-line exception. |
| V05 | Any nonzero exit can mean tool broken rather than planted violation caught. | Clean control first, expected diagnostic/rule/exit attribution, separate infrastructure error from code failure; actually run hooks plus CLI on shipped config. |
| V06 | Claimed gates differ from configured/executed/required/passing ones. | Track each state separately, at a precise Git ref with runtime/tool/config/lock identity and event applicability. Verify hosted protections/required-check names and bypass privileges instead of trusting setup docs. |
| V07 | Agent-written reports and logs can overclaim or be tampered with. | Prefer harness/CI-captured exit/status/postcondition and bounded artifact hashes over self-attestation. Reports list changed files, ran/observed/skipped checks, uncertainty and residual risk without flooding context. |
| V08 | Failed or timed-out mutating tools can already have effects. | Read postcondition before retry; distinguish dispatch/tool/protocol failure; idempotency keys for supported external writes; never generic blind retry. Ambiguous state blocks repeated irreversible action. |
| V09 | Flaky tests need classification, not 'retry to green'; stochastic systems can have intentionally statistical tests. | Preserve seeds/failures; separate environment, nondeterministic behavior and assertion defects; define bounded investigation and quarantine policy with owner/expiry. |
| V10 | Five trials is a screening suggestion, not evidence-based universal sample size. | Representative paired tasks, independent fresh runs, record all outcomes, explicit confidence/power/decision uncertainty. Pilot targeted tasks first; expand only when expected benefit justifies cost. |
| V11 | Benchmark success can ignore full environment reconstruction/deploy/no-change truthfulness. | Internal eval set: actual setup/build/test paths, already-fixed issue, ambiguous intent, unsafe dependency, injected instruction, tool timeout/partial write, test-oracle weakness and recovery. No deploy to production for evaluation. |
| V12 | A/B every model/skill/tool equally can become ceremony. | Risk-based change evaluation: lightweight static review/config smoke for mechanical pin changes; paired task evaluation for instruction/skill/harness changes likely to alter agent behavior. Isolate one experimental variable; report known residual confounders. |
| V13 | Rollback isn't simply reverting source after data migration or external action. | Separate reversible code/config rollback, data restoration, side-effect compensation and incident stop/revoke; prove the applicable recovery route before high-risk rollout. |

## E. Tracking, distribution and token economy — challenge prior proposal

| ID | Consideration / gap | Proposed path / unresolved issue |
|---|---|---|
| U01 | Prior canonical catalog + consumer receipt + deterministic checker remains a candidate, not selected architecture. | Compare minimal hand-built tracker against Copier or established alternatives; include migration/maintenance burden and actual needed semantics, not just initial code size. |
| U02 | One source SHA hides partial adoption and customized config merges. | Per-entry accepted source + content fingerprints, selected stack composition with one effective owner per destination, explicit exceptions. Source identity is not compliance evidence. |
| U03 | A receipt can claim fresh rules without edits/tests; bot bump can create false provenance. | Accepted source advances only for applied/reviewed item; separate observed bytes, accepted customization, active checks and last tested ref. Never treat manifest update itself as rule migration. |
| U04 | Existing copies have unknown adoption history. | Read-only enrollment proposal, identify byte-identical source matches, owner review for customized baseline; do not invent historical source version or mass overwrite consumers. |
| U05 | Updater is a privileged supply-chain/deletion surface. | Trusted fixed tool implementation; source policy/config treated as data; path/ownership/symlink validation, no arbitrary commands, expected-hash guards, staged branch proposals, no automatic deletion/rename or hooks. Verify before retries. |
| U06 | Shared docs/history changes shouldn't cause every consumer to update. | Fingerprints of explicitly relevant distributed units; avoid source-log churn. Notifications scoped to selected overlays plus actually shared rules. Semantically irrelevant config comments may still produce conservative diff notices. |
| U07 | Central registry can drift, duplicate worktrees, miss offline/private projects or expose local paths. | Generate observed view from authoritative receipts; explicit stable project ID, Git common-dir grouping, per-ref differences, last observation and coverage limits. No fleet-wide claims from local scan. |
| U08 | Canonical source decisions affect all consumers, but local exceptions can become permanent forks. | Document override ownership, expiry/review triggers and compatible migrations; define common minimum versus stack/project rule; no automatic enforcement of unsupported stack defaults. |
| U09 | Literal hashes/SHA changes don't reveal semantic rule impact. | Small change note: applicability, compatibility, required migration/verification and rollback; generate only mechanical diffs, human accepts policy semantics. Tags/releases optional; immutable source binding required regardless. |
| U10 | Zero model calls for detection is achievable, not zero cost/time/network for whole update process. | Offline routine checks against approved snapshots, one-line/no-op output, event-based notifications, lazy task routing, prompt/trace retention limits; review only changed units. Measure total tokens, latency and human intervention, not prompt length alone. |
| U11 | Dossier omits deployed Pi routing/skills/hooks/subagents environment. | Research portable core plus actual harness adapters; inspect documented Pi capabilities without editing other agents' configs. Vendor-specific hooks remain tested adapters, not canonical blanket guarantees. |
| U12 | Fleet rollout/registry/identity is outside Bee's unilateral authority. | Before durable fleet decisions: ClaudeBox context/coordination and expert review per standing rules, with Christopher's authorization and owner-approved handoff. Third researcher is evidence input, not that approval. |

## F. Overlay candidate log — retain alongside rebuild research

No blanket latest-version refresh. Previous scout proposals need executable proof and approved pins; static readings are not passing builds.

| Stack / shared seam | Candidates | Required proof / decision |
|---|---|---|
| TypeScript | Patched Vitest/coverage floor 4.1.11; aligned hook pins; pnpm-aware CI; actual coverage execution; test typechecking. | Official advisory independently checked. Major migration/Stryker compatibility/lockfile resolution and true exposure require tests. No unsupported latest-version claim. |
| Astro | React optional; generated-type inclusion; correct Biome 2 key; plain/React fixture checks. | Verify adopter compatibility/exclusions. Retain inherited strictest config; don't overwrite consumer integrations. |
| Workers | Maintained plugin line; tests tsconfig; Env generation; request/binding/isolation fixtures; npm command composition. | Official package deprecation verified. Test plugin API/runtime/mutation separation. Compatibility dates and nodejs_compat change only after approval. |
| Go | Generic non-Wails defaults versus opt-in architecture; analyzer tests/go.sum rebuild dependency; fail-closed bloat and baseline; exactly-one-JSON parsing. | Preserve TheWarRoom rules/build; test tool failure, malformed baseline and baseline nonmutation; partial syntactic analyzer guarantees clearly stated. |
| Python | Maintained mutmut config/CLI verification; Pydantic plugin versus unsupported claim. | Run approved installed tool help/example, plugin in project and hook environment, source collection/exit behavior. No guessed pin compatibility. |
| Bash | Reject zero without integer-overflow/octal parsing; Bats + actual ShellCheck config in CI; stage minimum. | Decide leading zeros and separate port-range requirement; positive/negative cases, actual hooks and diagnostic attribution. |
| Bun/ECS | 300-line conflict; supported Node guidance/local dependency invocation; purity-claim limits; strict own-client protocol examples. | Respect accepted project-specific ECS law. Decide reporting policy and behavioral compatibility; JSON snapshot security cannot be promised by shallow AST checks. |
| Shared CI | Fixture coverage for all seven; immutable action/binary identities; synthetic secret detection; correct package-manager composition. | Independent checksum provenance, runtime matrix, dependencies/lockfiles, fork safety, expected diagnostic assertions; no single generic installer across stacks. |

## G. Provisional planning phases (sequence to be challenged)

1. Verify evidence/capabilities; identify unsupported claims and ask material intent/risk questions. Do not select production pilot silently.
2. Define architecture seam boundaries and measurable success criteria: durable rule core, distribution/provenance, executable stack gates, harness containment/authority adapters, evidence/evaluation.
3. Obtain operator direction and required ClaudeBox/expert review for durable/fleet architecture. Record superseding ADRs only after approval.
4. Baseline one approved low-risk pilot and safety/verification gaps. Immediate security updates can be separate bounded work; do not wait for full research to acknowledge a known issue.
5. Implement read-only classification/tracking in temporary fixtures IF selected; no consumer writes. Test threat model and ownership/composition.
6. Add one approved gate/containment/update-planning change at a time; compare baseline, retain rollback; demonstrate real positive and negative behavior.
7. Validate the seven overlay changes in isolated fixture/adopter environments, with migration notes. Security/compatibility knot (Vitest/Workers/CI) must not be treated as independent trivial bumps.
8. Enroll approved consumers and expand rollout only from observed results; maintain separate rule freshness, execution authority and enforcement evidence.

Possible sequencing conflict to resolve: user originally wanted tracking in place before broader modernization, while dossier proposes pilot-baseline/gates first. A read-only baseline can support tracking without changing gates; a full automated updater must not outrun clarified authority and evidence. Third pass should recommend the smallest safe order, not assume either document wins.

## Third research pass commission / acceptance

After this log is complete, commission ONE fresh-context researcher. It must read the dossier, this log, and prior reports; verify R1–R18 and D1–D13 (or explicitly list inaccessible/unfinished entries), focus full-text work on consequential numerical/implementation claims, and seek omitted primary evidence only when a design-critical gap exists. No arbitrary six-month exclusion, no exhaustive product catalog. Validate current capabilities against exact product surfaces rather than aggregators. Challenge this log/prior tracker proposal as well as the dossier.

Deliverables:
1. Claim register: source ID, identity/date/method/sample/denominator verification, exact supporting/correcting passages and links, verdict/confidence/applicability.
2. Corrections/unsupported assertions ranked by design impact; separate conflicting evidence from absence of evidence.
3. Tested-versus-documented runtime/tool capability matrix including deployed Pi relevance, containment versus worktrees, licensing/free-first limits, enforcement semantics.
4. Minimum coherent implementation options, recommended sequence/dependencies, acceptance fixtures, migration/rollback, risk/authority seams, estimated operational/token overhead without fabricated measurements.
5. Decisions Christopher must make, blockers needing ClaudeBox/expert input, remaining unknowns, and concise parent synthesis.

Read-only except its configured report artifact. No installs, code/config changes, credentials, consumer edits, git/PR mutations, fleet contacts or nested agents. Its report is evidence/proposal, never adoption authority. Parent consolidates findings before asking for implementation permission.

## Completion record

Initial consideration logging complete before third-agent launch. All items above are candidates/questions unless explicitly marked locally or independently verified. Original dossier and current operational standards unchanged. No tests run during logging. Research outcomes are integrated below as a separately identified parent update after receipt; earlier questions remain intact rather than silently replaced.

## Research outcome — parent integration, 2026-10-08

Third agent: evidence-auditor, run `8645bde3-ca97-4228-b248-5465a40c37dd`.
Report: `~/scratch/coding-standards-rebuild-research-pass.md`, SHA256 `9a14604d973418c16f1eab6bdbd23451be1ec0f8df8d0bc794d3c2ecd018619c`.
Status: research received; no experiments reproduced, implementation approved, or operational policy changed. Original dossier checksum remains unchanged. The full claim/capability registers live in the report; findings below are parent synthesis, not a rewritten dossier. The report is currently scratch, not a durable repository archive; preserve a reviewed research artifact/citation register with the eventual approved spec before session closure or scratch cleanup.

### Direction retained

The audit supports bounded intent/authority, meaningful behavioral verification, proportionate deterministic gates, evidence-bearing reports, dependency review, and independent human acceptance. It does not support treating a long checklist or the newest model as a guarantee. Short task-relevant guidance and executable enforcement remain sound design candidates, with actual implementation-specific limitations.

### Consequential accuracy corrections

- Auditor reached all 18 research identities/submission histories and 13 official documentation surfaces, with full-text checks for material paper claims. 'Verified' means correspondence with the inspected source, not independent reproduction. Named authors do not establish human-only authorship.
- Author-register corrections attributed to the auditor: R9 first author Gen Dong; R12 Shota Sawada; R13 Sien Reeve O. Peralta; R14 Isham Kalappurackal Mansoor; R16 Chi Zhang; R17 metadata Mikhail Surikov. R14's July 31 submission is valid despite its 2608 identifier, resolving E04.
- R2's 91.49% concerns the 1,504 visibly resolved episodes, not all sessions/failures. R15's 15.4% is 409/2,660 assembled setups, not the full 3,171-repository collection. R13's 35.7% is 126/353 manually inspected rejected PRs, not every rejected PR. R11 interviewed 15; 14 performed coding tasks.
- R7 headline '67%' is inconsistent with detailed constructive-request counts; do not retain or substitute an invented universal compliance rate. R5 Lucky Pass is a process-score classification, not proof every classified patch is defective. R16 bundles advisory/cosmetic taxonomy defects with safety findings and overstates some specification requirements.
- Several papers reuse historic AIDev artifacts; avoid counting them as independent current-fleet measurements. Negative-only instruction superiority, universal five-run minimums, A/B for every maintenance change, all-LLMs-less-secure universals, and free/paid capability equivalence are unsupported generalizations.
- Original ADR comparative/vendor statistics are not fully audited. R4/R10/R13 independent conference confirmation remains incomplete. These open items cannot be silently closed by this report.

### Security/enforcement distinctions for the spec

1. Worktree isolation prevents some Git/workspace collisions; it does not contain host files, subprocesses, credentials or egress. Containment must be verified on actual execution paths.
2. Hooks are event/runtime/version-specific. Parent independently fetched current official Claude hooks docs after report receipt: a timed-out command/http/mcp_tool PreToolUse hook does not block the call; the ordinary permission flow still applies. Without valid blocking JSON, ordinary exit 1 is nonblocking for most hook events; exit 2 can block supported pre-action events. Agent SDK callback timeouts differ. Post-action hooks cannot undo a completed operation. This verifies documented behavior, NOT installed/live behavior.
3. Auditor inspected installed pi-subagents 0.76.1 docs: native child permission arbitration is opt-in, unknown tools default allow and Bash passes through that gate. This is NOT a claim that every Pi guard allows everything, nor evidence of effective session policy. Pi extensions execute with host-user privileges; workflow JavaScript sandboxing does not contain children's tools.
4. D12 documents particular Codex desktop plugin lifecycle surfaces; D13 concerns an Agents API executor. Neither establishes Pi/CLI capability. MCP Skills stable specification availability does not prove the deployed client negotiates/implements it.
5. Credential separation and whole execution-boundary permissions are separate from model read-tool allowlists. Evaluate parent/foreground child/background child/external runner separately, including build/install subprocesses.
6. Engine, action wrapper, rule-pack and hosted-service licenses differ. Private CodeQL/dependency-review/secret-scanning availability can require products/entitlements; scanner rule redistribution and external validity calls also require review. Free-first remains a constraint, not a detection-equivalence promise.

Primary docs parent checked: https://code.claude.com/docs/en/hooks (rolling, accessed October 8). Actual deployed/version-specific semantics still need canary validation.

### Context/instruction policy correction

Parent independently inspected https://arxiv.org/html/2602.11988v3 after receipt. The paper's overall results still warn against redundant context and increased inference cost; trace analyses explicitly find instructions followed with more testing/exploration. Appendix B says context files can act as useful overviews when documentation is absent. This does not justify universal 'overviews do not change agent behavior' wording in AGENTS/ADR. Keep a concise maintained routing/map policy if Christopher chooses it, but identify that as policy and respect nonstandard project facts. Supersede the overstated empirical rationale through an approved ADR rather than quietly altering history.

### Strengthened tracking design candidates

Retain four independent state domains: freshness against an approved snapshot, source/baseline provenance, configured/selected policy, and observed enforcement evidence. None implies the others.

- Per-unit revisions and fingerprints remain suitable for partial/customized consumers; add catalog/checker identity and changes in rule applicability to the comparison context.
- A consumer receipt is editable metadata, not authentic approval. Protect review/acceptance separately if required; receipt-only version bumps cannot claim a migration or passing gates.
- First implementation candidate stays read-only/offline whole-file classification, conservative review for merged snippets. No initial semantic config solver or automatic updater.
- Unknown lineage stays unknown. Exact matches establish byte identity, not owner consent. Enrollment requires owner review.
- Generated registry must show snapshot age, last observation, coverage limits, divergent worktree refs and project-ID collisions. Do not suppress stale/failed observation warnings while optimizing no-op output.
- Check source-side as well as destination-side path attacks, symlinks/hardlinks/case collisions, malformed/oversized data, concurrent edits and Git external-helper/filter/config execution risks. Source/catalog/receipt are data, never arbitrary commands.
- Whole-file hash classification is insufficient to claim policy compliance or approval. Enforcement evidence must bind precise tested bytes (including dirty changes), tools/config/environment/event—not merely a commit string.
- Copier remains an option for new genuinely rendered projects, not fabricated adoption history. Its tasks/migrations create execution authority; --skip-tasks does not skip migrations. Renovate remains dependency-pin support, not standards migration.

### Revised planning order — proposal, not authorization

1. Define success criteria, autonomy/approval boundaries, pilot ownership, source approval and distribution-unit ownership/composition. Bring durable fleet architecture/ADR choices to ClaudeBox/expert review with Christopher's authorization.
2. If approved, test a local read-only tracker against synthetic fixtures. No installs, network by default, enrollment or consumer mutation.
3. Prepare owner-reviewed enrollment/baseline proposals. Keep rule-version and gate-evidence states separate.
4. Add read-only update plans; permit managed-file application only under separately approved expected-hash, path, ownership, concurrency and rollback controls.
5. Modernize actual containment/gates/overlays one variable at a time with clean controls and diagnostic-specific violations. Handle known security migration separately rather than requiring completion of the entire rebuild.
6. Roll out fleet registry/automation only after coordinated ownership and observed pilot results.

### Additional no-go conditions

No false approval via receipt updates; no fabricated historical baselines; no worktree-only sandbox claims; no unknown/error-as-success; no policy/config PR that self-approves its own gate exceptions; no automatic activation/deletion/rename/remote write; no untested major compatibility claims; no rollback that deletes unrecorded user work.

### Open decisions and evidence still needed

Christopher must choose objective tradeoffs, normal-task autonomy boundaries, local versus fleet scope, pilot/source/owner, free-first interpretation, managed/customized units, evaluation proportionality and evidence retention. Confirm intentional Bun 300-line exception and Go project-specific law before migrations. Effective runtime security configuration, hosted branch protections, all overlay tests/hook installs, consumer lineage and numeric token savings remain unverified. No build or gate change is authorized by this integration.

## Relayed authority-advisor outcome — parent review, 2026-10-08

Input: `~/scratch/ordinary-task-authority-advisor-findings-2026-10-08.md`, SHA256 `54ecd4d10f1310f61700491ff32a1c4795fab8b3f475beb62afc05eb91efd07b`. Christopher relayed the report from the separate-model consultation. Model identity was not independently recorded; its internal author label says Bee, so do not infer a specific independent model/runtime from that label. Original advisor file remains untouched.

### Recommendation received (not adopted)

Bounded task grant: branch/worktree -> in-scope edits/tests -> verified local commit -> conditional named-remote/agents/<task-slug> push -> draft PR. Human-only ready-for-review and merge/deploy/irreversible actions. Remote protections must be checked before activating push/PR corridor; otherwise stop at local commit. Four proposed decisions: remote/namespace allowlist, readiness/merge authority, elevated risk definition and done-evidence format.

Parent agrees with graduated authority, bounded grants, explicit remote identity, independent acceptance and short evidence reporting as design candidates. Parent does NOT accept the remote-protection premise as sufficient containment, the claim containment can generally be deferred, or metadata labels as authenticated acceptance. No corridor, remote inspection, commit, push or PR authority has been adopted by receiving this answer.

### Gaps/corrections before a specification

| ID | Advisor seam | Parent assessment / required tightening |
|---|---|---|
| A01 | Default branch protections are 'load-bearing containment'. | Necessary for controlled integration, not containment of credentials, code disclosure, feature-branch writes, push/PR-triggered CI or malicious build scripts. Audit actor/token scopes and bypass privileges, applicable rulesets, workflow triggers/permissions/secret exposure and artifact handling. A namespace is not a security boundary unless actually enforced. |
| A02 | Ordinary execution containment is deferrable because tests already run project code. | Changed/generated code, fixtures, dependency graphs and existing scripts can exercise the same host privilege paths. No claim current trust model is accepted/verified. Establish minimum actual execution/credential/egress boundaries before granting autonomous execution or external writes. More advanced containment improvements can be staged after the baseline. |
| A03 | Agent-writable evidence and a human-only field in one receipt. | Field labels do not enforce write ownership in a Git-tracked document. CODEOWNERS protects merge only when applicable required owner review/rules/bypass settings enforce it; it does not prevent edits on a branch. Acceptance needs protected reviewed integration or an independently authenticated record. Distinguish local candidate evidence from accepted state. |
| A04 | Every expectation change excluded from ordinary grants. | Too broad: approved behavior changes often need new/updated expected outputs. Permit tests expressing the approved acceptance contract; require review for weakening/removing/skipping unrelated or previously guaranteed behavior. Gate/allowlist/policy/receipt ACCEPTANCE changes remain elevated; factual evidence records may be writable within scope. No generator self-certifies the oracle. |
| A05 | Human-only 'ready for review' is a permanent security gate. | Valid operator preference, not independently a containment mechanism. Keep explicit candidate until Christopher chooses. Actual protected acceptance/merge and truthfulness of readiness evidence matter; draft PRs still trigger external effects. |
| A06 | Failures reported/operator OK can permit commit; draft-on-red can be diagnostic. | Standing rule is never commit broken code; this proposal cannot create an ordinary exception or bypass hooks. Separate known behavior failure, pre-existing baseline issue, missing verification and failure discovered only in remote CI. Unknown is never pass. A locally viable candidate awaiting remote-only checks is not the same as knowingly broken code. A separate diagnostic approval does not waive current nonnegotiable rules. |
| A07 | Foreign changes -> unstage own files; dirty tree voids grant. | Preserve initial working tree AND index. Do not destroy another owner's staged state. Isolate own task; pause affected actions on unexplained changes, not every harmless unrelated edit. Before commit verify precise staged scope and expected tested bytes. |
| A08 | Grant voids on actor/state change; routine multi-agent mechanism deferred. | Define authorized principal, writer/reviewer/delegate ceilings and parent integration responsibility before delegation. Routine code changes and remote CI feedback are expected state evolution, not automatic revocation. Security/ownership/source changes trigger reauthorization. One writer per shared seam/worktree; no concurrent conflicting owners. |
| A09 | Grant standing exclusion says all external writes while including push/PR. | Make narrowly named push/PR exceptions explicit. Deploy/irreversible action approval and execution are distinct; human-owned authorization need not mean only a human can run the command, but no change to live authority is implied. Email remains explicit-permission-only. |
| A10 | Default allowlist includes all three repos; branch deletion can be rollback. | Start with a proposed canonical-only pilot, not automatic enrollment of consumers. Obtain actual remote/owner consent and check TFM's local-origin mapping before assuming hosted protections. Branch deletion is a separate authorized external/destructive action, not automatic rollback permission. Preserve no force-push/no destructive cleanup. |

### Recommended next investigation (requires explicit authorization)

Read-only audit of the canonical standards repository FIRST, with no consumer edits, fleet contacts or security-setting changes. Verify both source configuration and hosted state, if accessible:
- Default branch protection plus applicable repository/organization rulesets, required checks/owner reviews, merge actor permissions and bypass paths.
- CI event/branch applicability and token permissions, push and draft-PR side effects, fork/untrusted checkout and privileged workflow boundaries. Rule presence without actual applicable checks is insufficient.
- Proposed agent identity's permitted capabilities and approved remote/namespace enforcement. Do not print credential values or inspect private credentials without approved scope; unavailable evidence is a blocker/unknown, not implied safe.
- Existing local execution/credential/egress boundary through an owner-approved attestation; live canary or code execution needs separate scope. Source/hosted read-only API checks alone cannot establish OS confinement.

Audit results can support the authority-model draft; they cannot activate the corridor. If hosted fields are inaccessible or platform plan limits apply, report that precisely. Do not change protections to make the candidate work without a separately approved change.

### Provisional outcome

Use a bounded corridor as an authority-design candidate, with local commit, push, draft PR and accepted integration as separate rungs. Current rules remain live. Commit authority depends on approved ownership and viable/verified code; external authority additionally depends on actual credentials/workflow/remote controls, not branch protection alone. Proposed simplest rollout: canonical-only read-only audit -> operator chooses/refines grant boundary -> reviewed authority draft -> tracker schema/fixtures. Preserve original tracker-first objective without implementing unsafe automation ahead of its authorization model.

## Authorized canonical GitHub audit outcome — 2026-10-08

Christopher explicitly approved canonical-only read-only protection/workflow audit. Completed via GET-only GitHub API plus source inspection; no hosted settings, credential values, PRs, branches, commits, pushes, consumers or fleet machines changed.

Durable audit: `docs/planning/canonical-github-authority-audit-2026-10-08.md`. Minimized evidence: `~/scratch/coding-standards-github-audit-2026-10-08.json`, SHA256 `26e7c54a0e9d2896336e1847bdc637f75cda807d4116db3126788ff2aea9fbf3`. Main remained `93ee82a346289f7fdf77a696a20a999ffcc61dc6` throughout inspection.

New observed facts supersede earlier 'hosted protection unknown' FOR THIS REPO ONLY:
- Main has classic branch protection: five required GitHub Actions contexts, strict up-to-date base, admins enforced, linear history, no force-push/deletion.
- Approving review count is **zero**; code-owner reviews and last-push approval false; no CODEOWNERS in recognized locations. No mechanical independent-human acceptance proved.
- No repository/inherited rulesets returned. Main classic protection remains real despite empty ruleset endpoint. Ten branches listed; only main protected. No current agents/* namespace or namespace-specific enforcement demonstrated.
- CLI credential available in this session reports repository admin authority and broad repo/workflow OAuth scope. This is separate from Actions GITHUB_TOKEN. No values read/printed. Same broad identity cannot serve as a technically isolated ordinary-task principal without additional control design.
- Hosted Actions allows all actions, no SHA-pinning requirement; default token read and workflow PR-review approval disabled. Source security workflow adds security-events:write for all its jobs. External fork policy only first_time_contributors.
- Existing exact-HEAD security runs report all jobs success, but job-step APIs confirm required ts-lint and ts-test substantive steps skipped because root configs absent. Astro similarly skipped but is not required.
- Python/Go/Bash fixture steps actually ran and succeeded at exact HEAD, but none of their contexts is required by current branch protection.
- Twelve of eighteen action uses are mutable. Binary checksum coverage, dynamic scanner rules and blanket docs/README Gitleaks exclusions remain gaps.
- Current workflows have main-only push triggers and main/develop PR triggers, no privileged pull_request_target/workflow_run pattern in inspected source. Draft PR is not an execution/notification boundary.

Verdict: do not activate autonomous external corridor based on current owner-admin credentials or green context names. Before rollout, design separated authority and protected human acceptance, meaningful required gates and reviewed policy/CI controls. Minimum execution/credential/egress containment still needs owner-approved evidence; no OS or live denial tests were authorized/run. No policy adoption or implementation approval follows from this audit. Consumers remain unaudited.

## Operator direction correction — quality first, 2026-10-08

Christopher clarified before any build: avoid excessive workflow constraints; put constraints on good/bad code. Primary goal: no slop, elegant, human-readable, long-term maintainable code. This supplies the objective priority previously open in P01; exact autonomy and high-risk permissions remain unadopted.

Parent assessment: recent planning overemphasized git/publication authority and risked procedural ceremony. Those investigations exposed real security gaps, but publication infrastructure must support—not become—the coding-standard product. The restricted-publisher proposal remains an OPTION, not a mandatory implementation or evidence that maximum gating is desired. Human-only ready-for-review, broad test-expectation exclusions, repeated approvals and elaborate task grants are not presumed requirements.

### Revised design test

Every proposed restriction must identify a concrete code defect, acceptance-integrity failure or consequential security hazard it prevents, and justify its ongoing friction/cost. Prefer one proven mechanical check over repeated narrative compliance. Remove duplicated checks, arbitrary proxies and process steps without demonstrated benefit. Keep necessary credential/privilege containment separate from code-quality evaluation; good code does not make an owner-admin credential safe, and a secure corridor does not make code maintainable.

### Quality contract comes first (candidate structure)

- Observable requested behavior and preserved relevant compatibility; meaningful regression/behavior tests rather than test counts/coverage theater.
- Established project idioms and reusable existing utilities; clear domain names and cohesive responsibilities.
- Simplest sufficient complete implementation; no speculative framework, premature generic abstraction, unrelated refactor, near-copy proliferation or unnecessary dependency. Necessary complexity/dependencies are justified by real behavior/security/maintenance needs, not line-count rules.
- Explicit typed/validated trust boundaries, sensible errors and relevant observability; no secret leaks or unsafe external execution.
- Human-readable code and comments explaining non-obvious intent; no prompt/review history or ceremonial documentation inside source.
- Maintainable change surface: future owner can reason about contracts/behavior, tests explain intent, architecture law is project-relevant and exceptions are explicit.

Deterministic enforcement: applicable compiler/typecheck, formatter/linter, meaningful test suite and scoped security checks. Judgment review: intent, oracle quality, responsibility boundaries, unnecessary complexity, readability, maintainability and worthwhile abstraction. Passing machine checks cannot mechanically prove elegance or absence of every form of slop.

### Workflow position

Once a task is approved, agents should normally be able to inspect, implement, adjust tests to the approved behavior, run relevant checks and handle in-scope feedback without repeated approval rituals. Any commit/push/PR permissions still need explicit adoption under current standing rules. New material scope, real high-risk operations, credential access, destructive/external actions or weakening acceptance/security remain separately controlled. Routine expected edits/check failures/feedback are not automatically grant revocation.

Minimal evidence: what changed, what behavior/checks were observed, what remains unverified. Do not require large per-task report templates or universal repeated-run/mutation gates. Risk-proportionate deeper checks apply where they can reveal real failure modes.

### Exact next planning step

Draft a concise code-quality acceptance contract with representative good/bad examples, map each item to the smallest useful check or focused review, then evaluate workflow/security controls against that contract and the observed threat model. Do not build a publisher/tracker service before confirming it is needed and earns its friction. Preserve tracking-first implementation sequence after the quality/ownership/authority definitions are clear; no build is authorized by this direction discussion.

## Quality contract draft completed — 2026-10-08

Christopher authorized the next planning step. Created `docs/planning/code-quality-acceptance-contract-draft-2026-10-08.md`, a proposal only. No operational instruction, ADR, overlay, CI setting, consumer or authority changed.

Six acceptance dimensions: Q1 behavior, Q2 simplicity, Q3 readability, Q4 maintainability, Q5 safety, Q6 evidence. Each names concrete defects rather than agent ritual. Six paired examples cover real test oracles, avoiding speculative export frameworks, responsibility-based splitting, semantic reuse rather than blind DRY, validation versus authorization, and observable errors. Examples are illustrative, not executed production/test code.

Mapped to minimal existing checks: formatter/lint, applicable compiler/typecheck, behavior tests, scoped security/dependency/secret checks and focused diff review. Stronger testing is risk-specific. No new service/tool, universal file cap, automatic second-copy abstraction, arbitrary dependency line-count rule, universal mutation/repeated trials or large completion report required.

Draft distinguishes Meets contract / Needs change / Unverified; test changes expressing approved behavior are allowed, concealed weakening is not. Existing inherited relevant problems are disclosed rather than forcing unrelated cleanup. Current authority/credential rules stay live.

Next acceptance exercise proposed, not run: evaluate representative correct fix, weak-test green patch, unnecessary framework, coherent long/tangled short units, boundary failure and evidenced no-change cases. Demonstrate that verdicts track quality and maintenance cost, not proxy metrics or added approval steps. Christopher must review/accept the contract before it is mapped into canonical instructions/overlays; any superseding ADR is a separate reviewed migration.

## Architecture/data-flow/debloat extension — 2026-10-08

Christopher requested architectural-design review coupled with bloat identification and suggestive debloat reducing lines/characters while doing the same job. Initial coding sessions supply the design/data-flow baseline. He explicitly clarified 'wise node structures' means code components and data-flow nodes, NOT agent-workflow stages.

Created `docs/planning/architecture-dataflow-debloat-review-draft-2026-10-08.md` and linked its compact method from the parent quality contract; Q4 now explicitly includes state ownership and data flows. Both remain drafts, not operational policy.

Method: map only relevant initial intended responsibilities/contracts/edges/state effects/failure routes; independently trace actual source; distinguish intent/source-traced/exercised/unknown; compare meaningful routes and owners; propose evidence-backed bounded simplifications. Real nodes need not imply new files/classes or a forced DAG/layer model. Better observed designs can replace mistaken initial maps through explained review rather than diagram obedience.

Debloat must preserve behavior/API/state/security/error guarantees. Identify duplicated semantics, purposeless layers, dead scaffolding, unnecessary conversions/state copying and fragmented responsibilities; verify dynamic callers before declaring dead code. Suggestions show smallest change, evidence/uncertainty, risk and preserving tests. No automatic rewrite.

Measure consistent before/after affected source lines and character totals including replacement helpers, separate from tests/docs/generated artifacts. Estimates are labeled. Smaller but harder to read fails the contract; useful complexity and stronger tests are not bloat. No required quota, custom graph service or per-task architecture ritual.

No review exercises or debloat changes have run. Proposed validation includes coherent flow, unexpected effects, unnecessary framework, superficially similar/different semantics, dynamic callbacks, unreadable compression and an implementation improving on initial design. No new delegation, git or deployment authority granted.

## At-a-glance project application map — 2026-10-08

Christopher requested less prose/more structure showing how this work applies to future projects before building. Created `docs/planning/rebuild-at-a-glance-2026-10-08.md`: canonical quality/selected overlays/review/tracking -> project task/design/code/test/review/verification/acceptance loop; evidence-aware debloat output; proposed updates; completed-investigation versus draft/unbuilt status. It explicitly preserves current guardrails and distinguishes logical checkpoints from extra workflow rituals. No architecture choice, policy adoption or implementation added by this map.

## Operator approval / compaction checkpoint — 2026-10-08

Christopher: **"I approve, after compaction we will rebuild the coding standards."** The compact-safe workflow is authorized, including committing/pushing this checkpoint and updating the Hermes task ledger. This is not session close or authorization to enable the proposed App/broker, migrate consumers, alter hosted controls or bypass current guardrails.

Quality-first direction and architectural/data-flow/bloat-review goals are settled; proceed after compaction rather than re-asking what to do. Implementation has NOT begun. Eight original evidence artifacts were copied unchanged into `docs/planning/evidence/`, with byte/hash/source manifest; originals retained. No live session processes/agents remained, no reclamation needed, filing check PASS.

Checkpoint branch: `docs/standards-rebuild-checkpoint-2026-10-08`, based on main `93ee82a346289f7fdf77a696a20a999ffcc61dc6`; no merge/main modification intended. `.project.yaml` remains unrelated untracked material. Resume state goes to `docs/planning/RESUME.md`, plus the two compact-safe Bee config copies.

Bee config repository is actually dirty on `session/ccyt-preflight`, not main as the skill assumes. Preserve every unrelated edit; commit only this resume on main through a clean temporary Git worktree, without switching/committing the live config branch. Config repo has no remote.

Hermes task T415 added under SUPPORT for the revived coding-standards rebuild, via cc (3e278ea); stale parked-overview project name removed in one-line edit (468757c). Existing completed adoption task T098 and unrelated tasks untouched. Task list: checked0, updated0 existing task rows, added1 (T415); parked overview corrected. No mirror NOW/Task_list edited.

See `docs/planning/RESUME.md` for next actions, run transcript recovery references, artifacts and remaining unknowns. On 'we are back', read the persisted resume first and continue the bounded rebuild.
