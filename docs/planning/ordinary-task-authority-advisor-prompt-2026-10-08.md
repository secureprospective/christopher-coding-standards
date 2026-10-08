# Advisor prompt: autonomy and authority for the coding-standards rebuild

**Prepared:** 2026-10-08
**For:** a separate model advising Christopher Campbell. Christopher will relay your answer back to Bee.
**Task:** planning advice only. This prompt grants NO permission to run tools, inspect private environments, change files, install anything, commit/push, open a PR, merge, deploy, contact agents, or perform external writes.

## Your assignment

Recommend the future authority model for ordinary AI coding tasks, then identify the few additional decisions we must settle before drafting the coding-standards rebuild specification.

The immediate question is:

> For an ordinary approved task, should agents stop at a verified patch, or may they also commit and open a PR within that approved scope?

Do NOT treat this as a simple binary. A local commit, a remote push and PR creation have different effects and authority requirements. Explain a practical default with explicit boundaries, escalation triggers and enforcement. Your answer is a recommendation for Christopher to accept or reject, NOT an adopted policy or live permission change.

This prompt is self-contained. You do not need access to the repository or the earlier research files to answer. If you cannot verify a technical capability, label it a documented possibility or unknown; do not invent effective permissions or deployed security.

## 1. Operator intent and working style

Christopher is rebuilding a coding-standards repository started months ago. The purpose is to formalize what today's agents can do reliably and make his AI engineering environment as effective as possible. This session is now planning, not implementation.

He prefers direct recommendations and exact first steps, clear scope, facts over reassurance, and clarification before material assumptions. He wants capable agents to move work forward, but not fabricate verification or force him to rebuild misunderstood work. His exact desired balance among autonomy, correctness, security, latency, cost and human attention has NOT yet been finalized.

Low token burn is an explicit objective for routine standards tracking. It is NOT permission to reduce safety, skip necessary verification or hide uncertainty. Avoid requiring repeated long prompts or human approval for every already-authorized mechanical action. Conversely, do not infer that approving a task authorizes all external actions.

Christopher requested a second-model opinion on this authority question and invited other relevant questions/gaps. Present a reasoned default, not a large unranked menu. Distinguish operator decisions from details that can be settled conservatively during design.

## 2. Repository and existing architecture

Canonical repository: `secureprospective/christopher-coding-standards`, currently main at commit `93ee82a346289f7fdf77a696a20a999ffcc61dc6`.

It is a **copy-and-customize standards kit**, not a centrally installed enforcement engine. About 101 tracked files include:
- Advisory `AGENTS.md` and a customizable `SYSTEM_MAP.md`.
- Full/Lite agent doctrine, multi-agent roles, audit guidance, an accepted architectural decision and task-routing index.
- Seven overlays: TypeScript, Astro, Cloudflare Workers, Go, Python, Bash and Bun/ECS.
- Compiler/linter/hook/security/test/coverage/mutation configs and some bespoke checks.
- A manual adoption skill, GitHub PR helper, session notes and feedback logs.

Typical intended flow: canonical source -> manual adoption/customization -> project-local gates/CI -> human acceptance. There is no reliable automated reconciliation, consumer version receipt or registry today.

Two local consumer projects were identified:
- **TheWarRoom:** customized Go enforcement and project-specific architecture/build choices.
- **TFM Playbook:** TypeScript adoption with drifting copies; multiple worktrees are versions of one project, not independent adopters. A local-origin arrangement means remote URL alone is not reliable project identity.

There are real deterministic checks, but CI currently verifies only selected Python/Go/Bash template fixtures. All seven overlays are not yet comprehensively verified. Hosted protections and installed consumer hooks were not established by the investigations.

This is not a blank-slate product and not authorization to rewrite either consumer. Their owners/agents and existing changes must be respected.

## 3. Current guardrails — actual constraints, not implied future freedoms

Standing Bee/operator rules include:
- Never send email without explicit permission.
- Never force-push or use `--no-verify`; never commit broken code.
- Preserve pre-existing user changes; establish the live path/state before moving or deleting anything.
- Do not edit another agent's files without an authorized ownership handoff.
- Verify before reporting completion; distinguish what ran from what merely compiled or was inspected.
- Change one experimental variable at a time and flag uncertainty.
- Fleet-wide coordination/context belongs to ClaudeBox, the head brain; Bee is a working node. Durable fleet decisions need expert review and ClaudeBox context rather than unilateral adoption.

Existing canonical prose also says:
- Declare scope/blast radius and obtain acknowledgement before modifying an existing module.
- Work on a branch for refactors; functional changes need tests.
- Builder is the sole agent with git/living-doc authority; Recon does not commit/push/merge.
- Human owner approves pushes/merges and controls consequential acceptance.
- The adoption skill asks for human confirmation before committing.
- Guidance is advisory; hooks/CI are intended enforcement. The blanket 'hook wins' formulation itself needs trust/authority qualification.

Some role/vendor assumptions are stale: current authorized bounded subagents do not match the old single-vendor, human-relay-only topology. Those documents will need a reviewed update, not silent bypass.

Important: improving a future policy does not repeal current guardrails. If you recommend delegating commit/push/PR authority, specify the operator approval and superseding policy required. Keep merge/deploy/irreversible operations separate. Do not recommend bypassing failing checks, force pushes or unauthorized email.

## 4. What the investigations established

Three delegated passes have occurred: repository mapping, overlay update investigation and independent evidence/implementation-path audit. The third pass inspected 18 research identities/history records and 13 product-documentation entries, including material paper sections. No experiments were reproduced, tools installed, protections activated, consumers changed or policy adopted.

Research supports these broad engineering directions:
- Already-correct behavior/no-change should be an acceptable result.
- Confirm scope/intent and inspect actual repo state before edits.
- Generated output is a draft until meaningful acceptance evidence exists.
- Green tests, coverage and new test files do not prove intended behavior; assertions/oracles matter.
- Instructions/skills/harness changes can affect scope, correctness and efficiency.
- Least privilege, explicit external-write authority, reviewed dependencies and independently reviewed acceptance remain important.
- A tool timeout can occur after a write succeeds; inspect postconditions before retrying.

The low-grade-model dossier was useful but not ready to become policy:
- Several author attributions and statistical denominators were incorrect.
- Several studies concern older models/historical public artifacts, and some reuse the same corpus.
- 'Negative rules always beat positive rules,' 'five trials for every change,' and 'A/B every component' are unsupported universal prescriptions.
- Assertion counting cannot establish semantic test quality.
- 'All current LLMs are less secure than humans' and 'free tooling equals paid tooling' are overbroad claims.
- Concise nonredundant context is sensible, but a universal ban on architecture context is not established by the cited research.

Do not build your recommendation on universal failure percentages, model-brand stereotypes or unverified benchmarks. Scope controls to risk and actual evidence.

## 5. Technical boundaries that directly affect delegated git/PR authority

### Workspace versus security isolation

A Git worktree can isolate changes and reduce collisions. It does NOT confine host filesystem access, network, credentials or subprocesses. Agents, tests, installers, hooks and build scripts can execute with the launching user's privileges. A container/VM/dedicated identity must itself be configured and tested; its name alone is not evidence of containment.

### Hooks and permissions

Current official Claude docs distinguish hook events/output semantics:
- Ordinary command/http/mcp_tool PreToolUse hook timeouts do not block a tool call; normal permission flow still applies.
- Ordinary exit1 is nonblocking for most hook events unless valid output makes a blocking decision; supported pre-action hooks can block via exit2.
- Agent SDK callback behavior differs.
- Post-action hooks cannot prevent an already-completed action.

Installed Pi-subagents documentation inspected by the researcher describes opt-in native child permission arbitration with unknown tools defaulting to allow and Bash passing through that particular gate. This is not a claim about all possible guards or effective current settings. Workflow JavaScript sandboxing does not contain tools executed by child agents. External runners introduce another authority surface.

The actual active Pi build, effective parent/child/external-runner loadouts, OS confinement, network denials and credential exposure remain unverified. Do not assume a model-level tool allowlist safely constrains unrestricted shell commands.

### Git and PR operations

Committing can run hooks; hooks can execute untrusted project-controlled code. Push invokes network/credential paths and can trigger CI. A PR creates an external artifact, can expose code or metadata, and may trigger privileged workflows/notifications. Draft PRs also have these side effects. Fork/PR event security, token scopes, repo/branch allowlists and ownership protection matter.

A pinned source/component is identifiable, not automatically safe. Catalogs, receipts, scanner allowlists, workflow files and instructions are policy surfaces; agents must not be able to expand their own authority or self-approve exceptions through those edits.

## 6. Proposed distribution/tracking path — not yet approved

The current reasoned default is a minimal offline-first deterministic tracker rather than a model-driven updater:
1. Canonical distribution catalog: source-to-destination mappings, overlay composition/precedence, ownership class.
2. Tracked consumer receipt: selected overlays, per-unit accepted source revisions and source/destination fingerprints.
3. Fixed trusted read-only checker and generated registry view.
4. Later reviewed update proposals; initially no automatic custom-snippet reconciliation.

Keep FOUR state domains separate:
- **Freshness:** relevant content compared with an approved immutable snapshot.
- **Provenance:** source identities and reviewed baseline recorded.
- **Configuration:** gates/permission policy present and selected.
- **Enforcement evidence:** actual checks observed on exact code/config/tool/environment/event.

A receipt is editable metadata; it is not authenticated approval and does not prove checks ran. Accepted source must not advance just because a bot edits a SHA. Whole-file comparisons can conservatively flag customized snippets for review. Unknown historical adoption stays unknown. Registry scope/age/offline coverage and divergent worktree refs remain explicit.

Alternative: Copier for genuinely rendered/new projects, but existing manual/customized copies lack true generation lineage. Do not fabricate its answers file. Its update tasks/migrations carry execution risks; --skip-tasks does not skip migrations. Shared packages/submodules or Renovate can help particular units/pins, not replace migration authority or evidence.

Proposed order: define authority/schema/ownership -> read-only synthetic-fixture checker -> owner-reviewed enrollment proposals -> safe update plans -> separately approved bounded managed-file application -> coordinated rollout. Christopher had asked to have tracking in place before broader modernization. A read-only baseline fits that; an unsafe automatic updater does not.

Known security remediation can be separate bounded work: parent independently verified Vitest GHSA-82fw-gwwq-j7x9 (stable fix4.1.11, shipped Vitest3 range cannot receive it), and deprecated Workers pool package renamed to @cloudflare/vitest-plugin. Compatibility/actual exposure and consumer migrations are NOT tested. No blanket dependency refresh is proposed.

## 7. Define 'ordinary approved task' before answering

Suggested starting definition, for you to challenge:
- Operator has approved a concrete behavior/acceptance contract, repository, scope and task owner.
- Work is reversible, local-to-project, low/moderate risk and inside the existing architecture.
- Required tooling/environment and protected paths are known.
- No new secret access, production authority, destructive migration, policy weakening or external action is implied.

Exclude or require separate escalation for auth/authorization, cryptography, secrets/privacy/payments, destructive/schema/data migrations, production infrastructure/network exposure, untrusted execution, dependency/build/hook scripts, security policy/gates/receipts/updater changes, and material scope/architecture expansion. Risk cannot be determined by file count/path alone.

Distinguish a **locally checked patch**, a **committed candidate**, a **draft PR awaiting CI**, and a **review-ready PR with applicable evidence**. Some checks can only run after push. Do not create the impossible requirement that remote CI pass before the action that triggers it. Conversely, do not call a draft PR fully verified merely because it exists or compilation succeeded.

A failed/infrastructure-unavailable check must remain visible. Unknown is not success. Explain whether a clearly labeled draft PR may still be permissible under explicit authorization and what must block any claim of readiness.

## 8. Specific questions your answer should resolve

### Primary authority question

For a scoped ordinary task, who may perform each of these steps, under what permission and evidence?
- Create/select branch or isolated worktree.
- Modify code and tests.
- Run builds/tests/hooks (including project-controlled code).
- Stage only authorized changes and create a local commit.
- Push to an approved remote/branch namespace.
- Open/update draft PR; mark ready for review.
- Address reviewer/CI feedback within the same scope.
- Change test expectations, scanner exceptions, standards receipts or checks.
- Merge, deploy, perform irreversible action or external/data migration.

Identify permissions that can be granted once for an approved task versus actions that always need new approval. Define the lifetime/revocation of that grant and what happens if state, scope, actor or risk changes.

### Related design gaps

1. **Review/acceptance:** what independent evidence and review are necessary at each risk level? Must Christopher personally approve every low-risk commit, or can approval cover a bounded task? Do not confuse an agent reviewer with authentic human acceptance.
2. **Multi-agent ownership:** parent versus delegated writer/reviewer roles; one writer per shared seam/worktree; who stages/commits/integrates; how stale work, collisions and reviewer follow-ups are handled. No child silently expands its capabilities.
3. **Source and receipt approval:** who approves canonical rule changes and downstream adoption/overrides; how an agent-editable receipt cannot self-certify approval/enforcement. Do policy/updater changes belong in a higher-risk class?
4. **Pilot and rollout:** local tracker first versus fleet registry; what baseline is required; what must be resolved with ClaudeBox/expert review before a durable fleet choice. Do not silently choose a live pilot or contact fleet nodes.
5. **Tooling/containment/free-first:** minimum verified runtime boundaries; license/entitlement limitations; acceptable fallback. Free engine/action/rules/hosted services are not interchangeable.
6. **Evaluation and reporting:** risk-sensitive tests/evals, actual tool/hook behavior, exact tested-state evidence, skipped-check handling and truthful reporting without excessive tokens. Avoid universal five-run or full mutation requirements for routine mechanical tasks.
7. **Recovery:** ambiguous timeout after commit/push/PR creation; inspect state before retry, duplicate prevention, rollback without force-push/deleting user work, revocation/incident stopping.
8. **Operator objectives:** identify any genuine ambiguity in autonomy/security/cost/human-attention tradeoffs that must be answered. Offer a conservative provisional default instead of assuming intent.

Do not turn every unresolved implementation detail into a question for Christopher. Prioritize questions that change design or risk. Label harmless choices that can be deferred.

## 9. Expected answer format

Keep the recommendation usable; aim for roughly1,200–1,800words, extending only for necessary nuance. No giant generic AI safety essay or product shopping list.

1. **Direct recommendation** for ordinary tasks: proposed default, why, limits. Explicitly state it requires Christopher's adoption.
2. **Authority matrix**: action | actor/permission | prerequisite evidence | stop/escalate trigger. Distinguish local commit, push, PR, merge and deploy.
3. **Small task-authorization contract**: minimal fields and grant scope/lifetime. Mark illustrative language as future-policy draft, not current permission.
4. **Enforcement sketch**: what is advisory versus mechanically enforced; runtime/OS/CI boundaries; self-approval protections; what remains unverified.
5. **Prioritized additional decisions**: only material ones, with a recommended default, reason and what changes if Christopher chooses otherwise. Separate blockers from deferrable issues.
6. **Exact first planning step** and no-go conditions before implementation. Respect tracking-first and one-variable-at-a-time.
7. **Uncertainty/contradictions**: unsupported assumptions, any change to the provisional proposal, evidence needed to validate it. Cite reliable sources for new technical claims; do not invent product features or deployed configuration.

Christopher will bring your answer back for synthesis. Do not approve changes, promise a security guarantee, or claim any proposed gate has been implemented/tested.

## Optional source references for consequential claims

These are background, not a requirement to redo all research:
- Claude hooks: https://code.claude.com/docs/en/hooks
- Claude sandboxing: https://code.claude.com/docs/en/sandboxing
- Pi security: https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/security.md
- Git worktrees: https://git-scm.com/docs/git-worktree
- GitHub Actions security: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- Copier updates: https://copier.readthedocs.io/en/stable/updating/
- Context study (scoped findings, not universal rule): https://arxiv.org/html/2602.11988v3
- Verify-before-retry paper (controlled simulation, not broad production assurance): https://arxiv.org/html/2608.02645v1

Local provenance for Bee/Christopher (the external advisor need NOT access these):
- `docs/planning/rebuild-considerations-2026-10-08.md`: initial55considerations plus integrated audit findings.
- Independent research report: `~/scratch/coding-standards-rebuild-research-pass.md`.
- Overlay proposals: `~/scratch/coding-standards-overlay-audit.md`.
- Distribution/tracking investigation: `~/scratch/coding-standards-update-mechanism-investigation.md`.

This prompt intentionally supplies the consequential context directly rather than requiring the external advisor to inherit our session or open machine-specific files.
