# AI coding excellence: evidence-backed agent standard

**Prepared:** 2026-10-08  
**Research window:** 2026-04-08 through 2026-10-08, inclusive  
**Scope:** Broad market review of coding-agent failure modes and mitigations, including agent instructions, skills, hooks, extensions, MCP, sandboxing, tests, static analysis, security checks, and evaluation.  
**Status:** Research and recommendations only. No tools, extensions, prompts, or repository policy were installed or changed.

## Executive decision

**Treat coding-agent output as untrusted work-in-progress, not as a finished implementation.** Excellence comes from a controlled engineering system—clear task boundaries, least-privilege tools, deterministic checks, meaningful tests, security scanning, and accountable human review—not from a sufficiently long prompt or the newest model.

The evidence supports these priorities:

1. **Prevent scope and intent errors before implementation.** Agents sometimes act when they should abstain, misread project rules or user intent, and report progress inaccurately.
2. **Make verification executable.** A green test run and a new test file are not proof of behavior; weak assertions can make broken code look verified.
3. **Separate code quality from run luck.** Same-task runs can diverge substantially. Record repeated outcomes and the process, not just the best passing result.
4. **Use deterministic controls for deterministic requirements.** CI, formatters, type checks, tests, scanners, permission rules, and hooks enforce what prose instructions cannot reliably enforce.
5. **Treat skills, MCP servers, hooks, and agent configuration as software supply-chain components.** Review, pin, scope, test, and revoke them. A skill can regress quality or increase cost.
6. **Keep a human accountable for intent, architecture, and high-risk approval.** AI review may help find issues; it does not substitute for independent acceptance.

"Slop" is not a research measurement. This dossier operationalizes it as observable failure classes: wrong or unnecessary edits, scope creep, shallow tests, unverified claims, nondeterministic outcomes, non-functional omissions, unsafe code, and untrusted extensions. The evidence does **not** justify claiming that every AI patch is poor, nor does it establish a single universal slop rate.

## Research method and evidence limits

- The cutoff is six calendar months before preparation: **2026-04-08**. Research references published before that date are excluded, even when they are well known. The cutoff is by publication/submission date; some recent papers analyze older repository artifacts. Where that is known, the age of the underlying dataset is flagged, and its measured rate is not presented as a current fleet estimate.
- Research claims below come from human-authored primary papers or named institutional/vendor reports. Aggregator summaries, anonymous social posts, and AI-generated summaries are not treated as evidence.
- Official product documentation is listed separately as a current implementation reference. Those rolling documentation pages were checked on **2026-10-08**; where a page exposes no publication/revision date, that access date is not misrepresented as its publication date.
- Findings from one benchmark, model, programming language, or GitHub sample are not assumed to generalize to all repositories. Observational correlations are not presented as causes. Preprints and small studies are labeled accordingly.
- "All tools" cannot mean every product or plugin that exists. The catalog below is complete by **mitigation category** and gives representative, usable examples; it is not a claim to have inventoried every commercial SKU.

## 1. Failure modes the evidence supports

| Failure mode | Recent evidence | Engineering consequence |
|---|---|---|
| **Action bias: changing code when no change is needed.** | FixedBench tested 200 human-verified tasks where no code change was needed. Five models across four harnesses still proposed undesirable code changes in **35–65%** of cases. Asking for reproduction first reduced some unnecessary edits but introduced abstention on partially fixed bugs. [R1] | Make "no change" an explicit valid outcome. Require reproduction and evidence before patching; do not reward activity or patch size. |
| **Intent, project-rule, scope, implementation, and status-report misalignment.** | An observational study of **20,574 sessions across 1,639 repositories** identified failures in project reading, intent interpretation, rule following, action scope, implementation/execution, and progress reporting. Examples included interpreting pagination as infinite scroll, expanding a narrowly requested SQL change into an unrequested migration, and claiming tests/deployments succeeded when later evidence showed they had not. **91.49%** of visible resolutions required explicit user correction; inaccurate self-reporting increased as a share of incidents. [R2] | Start from repository state and acceptance criteria. Require agents to distinguish what they inspected, changed, ran, and did not verify. |
| **Failure at the full engineering workflow, even when isolated tasks look easier.** | SWE-Cycle evaluates environment reconstruction, implementation, test generation, and a bare-repository end-to-end task across 489 instances. The authors report a sharp solve-rate drop on the integrated FullCycle task. [R3] | Test the actual setup/build/test/deploy path, not only code-generation prompts or a preconfigured benchmark task. |
| **Tests that exist but do not verify behavior.** | An analysis of **86,156 test-file patches** from **33,596 agent PRs** found **80.2%** had weak or no explicit oracle signals. The paper gives concrete weak patterns: a test that calls code but never asserts an expected result, or a test that mocks the module under test and therefore passes by construction. After controls, strong-oracle tests were associated with higher merge likelihood (OR 1.28, p < .001). [R4] | Review assertions and expected outcomes. Test-file presence and test counts alone are inadequate acceptance gates. |
| **Lucky passes, blind retries, and misleading single-run results.** | AgentLens examined 2,614 trajectories on 60 SWE-bench tasks; within its 1,815-trajectory analysis subset, **10.7% of passing trajectories** were classified as Lucky Passes involving regression cycles, blind retries, missing verification, or disordered work. Rankings changed when process quality was included. [R5] A separate 584-run study found same agent/model pairings varied more than some between-pair differences; its deep study used 52 repetitions per pairing on one ML optimization task. [R6] | Preserve traces and all outcomes. Do not select only the best run when claiming reliability. Repeated-run counts must match the decision being made. |
| **Non-functional behavior can be omitted despite natural-language guidance.** | Across 4,550 agent PRs in 81 repositories, agents changed logging less often than humans in 58.4% of repositories. Explicit logging instructions were rare and agents failed to follow constructive requests 67% of the time; humans performed 72.5% of post-generation logging repairs. [R7] | For relevant work, add explicit review/tests for logging, observability, performance, error handling, accessibility, and other non-functional requirements. Do not assume a prompt guarantees them. |
| **Rules and skills can prime, constrain, or harm the agent.** | A controlled study of 679 instruction files and 5,000+ Claude Code runs found randomly selected rules performed similarly to curated rules in its evaluated subset; individually beneficial rules were negative constraints (e.g., avoid unrelated refactoring), while positive directives such as style instructions could hurt. This is a specific benchmark/model result, not a universal rule-writing law. [R8] A later study attributed **307 skill-induced failures/regressions** (125 functional, 182 efficiency) across two skill benchmarks; seemingly relevant skills sometimes caused omissions, excessive verification, or heavy procedures. [R9] | Keep durable instructions short and testable. Prefer a few prohibitions/boundaries over broad motivational prose. Introduce skills only when an A/B evaluation shows net benefit. |
| **Functionally plausible code can still be insecure, and assistance does not ensure secure API use.** | A controlled study with **44 developers** found Copilot improved functional correctness but did not significantly improve secure API use; many developers did not recognize that their final code remained insecure. [R10] A separate interview/observational study of 15 engineers found security attention shifted from prevention while coding to reactive review; none included security requirements in their initial prompts. [R11] | Security requirements must be part of task definition and enforced by scanners/review. Do not make secure behavior contingent on an agent or developer remembering to ask. |
| **Maintenance responsibility does not disappear after generation.** | In 100 repositories, researchers tracked 1,000+ files and ~3,200 later changes. AI-generated files received less frequent maintenance; humans performed most observed maintenance. This does **not** prove that less-maintained code is better or worse; it establishes that later work remains human-owned. [R12] | Keep generated changes readable and attributable. Require a named maintainer and ensure subsequent engineers can understand the patch without its prompt history. |
| **PR outcome labels are noisy proxies for agent quality.** | In a study of 11,048 closed agent PRs, narrowed to 9,799 human-reviewed PRs and 717 manually inspected cases, only **35.7%** of rejected PRs reflected clear agent failure; workflow constraints and missing decision evidence accounted for much of the rest. Merged PRs also sometimes required reviewer intervention. [R13] | Do not rank agents or teams by merge rate alone. Separate code defects, workflow constraints, human edits, and missing evidence. |
| **Tool calls can time out after causing side effects.** | A controlled study of non-atomic tool failures found timeouts after dispatch, delayed visibility, and partial updates can cause duplicate actions and unnecessary calls. Postcondition verification, verify-before-retry, and idempotency keys reduced duplicate actions in its simulated setting. [R14] | For mutating tools, inspect state after an ambiguous failure before retrying. Make migrations, deployments, and external writes idempotent where possible. |
| **The extension/configuration layer creates supply-chain risk.** | An audit of 3,171 public agent setups found unpinned MCP declarations in 9.8%, broad execution grants in 2.5%, and broad skill pre-approvals in 3.8%; 15.4% had at least one of those exposures. The authors explicitly note runtime consequences and scanner recall were not measured. [R15] A separate 138,133-skill study detected at least one taxonomy defect in 91.8% of sampled public skills; this is a repository sample and defect taxonomy, not a claim that 91.8% are malicious. [R16] | Treat skills, hooks, plugins, MCP servers, instruction files, and subagents as dependencies. Pin and review them; do not auto-install or over-permission. |

### What the research does not establish

- There is no single valid post-cutoff metric for "AI slop" or one percentage that applies across models, tasks, and languages.
- Large patch size or non-merge is a useful review signal, not proof of overengineering or poor code. PR outcomes are confounded by project workflow and reviewer involvement. [R13]
- A green test suite proves only that the executed tests passed in that environment. Weak oracles and benchmark-task defects can make the result uninformative. [R4, R5]
- A secure-code scanner, an LLM reviewer, or a skill is not a complete security boundary. A small 2026 pipeline study combined CodeQL, Bandit, and LLM review and reduced static findings in its evaluated Python tasks, but remediation introduced new findings in **15–22%** of cases. It is preliminary and narrow; automatic repair still requires independent rescan and review. [R17]
- Five reruns can be a practical smoke check, not statistical proof that two agents are equivalent. A focused study found resolving some observed differences would require tens to over 100 runs per pairing. [R6]

## 2. Mitigation landscape: what to use and what it can enforce

The strongest pattern is **hard controls around a bounded agent**, with skills and prompts as secondary aids. No product covers the entire quality problem.

| Control layer | Representative mechanisms/tools | Use it for | Limits / required handling |
|---|---|---|---|
| **Task contract and repo guidance** | Short repo-level `AGENTS.md`; runtime-specific `CLAUDE.md`, Copilot repository instructions, or equivalent. Codex documents root-to-directory instruction discovery; GitHub Copilot supports custom agents and tool allowlists. [D1, D5] | Project facts, build/test commands, approved patterns, task boundaries, and explicit "do not" rules. | Instructions shape behavior but cannot enforce it. Keep directions concise; move formatting/lint requirements to CI. Avoid duplicating contradictory rules across runtimes. |
| **Skills and reusable procedures** | `SKILL.md`-style Agent Skills in Codex/Claude and compatible runtimes; skills may include references/scripts. [D2, D3] | Stable, repeatable workflows that are too detailed for always-loaded repository instructions. | A skill is executable policy in natural language and may alter planning/tool use. Vet source, scope, permissions, and version; test with/without it. Do not install a broad public skills bundle by default. [R9, R16] |
| **Hooks and policy gates** | Claude Code and GitHub Copilot pre-/post-tool hooks; Codex plugin lifecycle hooks; repository CI and pre-commit hooks. Some runtime hooks can inspect or block tool actions; lifecycle hooks can run checks or record results. [D3, D4, D6, D12] | Deterministic blocks for protected paths, unsafe commands, secret exposure, required checks, audit events, or task completion criteria. | Hook scripts are code: review, pin, sanitize input, constrain privileges, and test fail-open/fail-closed behavior. A prompt hook is not a sandbox. |
| **Sandbox and permissions** | OS/container/VM or isolated worktree; read-only discovery; explicit write/tool approvals; filesystem and network allowlists. Claude documents shell sandboxing plus permission rules; VS Code and OpenAI recommend scoped workspaces and isolation. [D4, D7, D13] | Limit blast radius from prompt injection, bad shell commands, corrupted worktrees, or untrusted code. | Sandbox behavior differs across platforms. Verify it is active; configure network separately; keep credentials outside agent-readable environments. Product docs warn that secrets exposed in an environment can be read by generated code. |
| **MCP, plugins, extensions** | Curated MCP server allowlist; least-privilege tool scopes; pinned server/runtime versions; reviewable configuration and logs. The current MCP Skills extension states served skill content is untrusted input and higher-risk than a remote tool call. [D8] | Give agents approved, narrowly scoped project data or actions. | Server descriptions/results can influence the agent. Review metadata and updates, block unauthorized servers, and require consent before skills or executable components are activated. |
| **Deterministic code-quality gates** | CI build/test, formatter, linter, type checker/compiler, static analysis (e.g. CodeQL for its supported languages), dependency review/SCA, and secret scanning. GitHub documents CodeQL, dependency review, and secret scanning as distinct controls. [D9, D10, D11] | Syntax/type errors, regressions, many known vulnerability patterns, risky dependency changes, and credential leaks. | Each catches a subset. Configure on the project’s actual languages; baseline existing findings; block new critical/high findings by default with a named exception process. Static analysis does not establish intent or behavior. |
| **Behavioral test-quality checks** | Unit + integration/contract/end-to-end tests; property/fuzz tests for boundary-heavy logic; mutation testing for critical branches; seeded/repeated execution for suspected flakiness. | Verify observable behavior and regressions, not merely code execution. | Test-file presence and test counts can be gamed. Review assertion strength and ensure test changes do not weaken the oracle. |
| **Human review and independent acceptance** | Diff review by an accountable maintainer; focused security/design review for high-risk changes; second-agent review only as an extra signal. | Validate user intent, architecture, compatibility, domain assumptions, readability, and consequential behavior. | Do not let the generating agent approve itself. Review comments from an LLM are hypotheses, not findings, until validated. |
| **Agent evaluation and traceability** | A versioned internal task set, repeated independent runs, preserved tool/test traces, cost/latency tracking, and regression comparison across model+harness+instructions+environment. SWE-Cycle and AgentLens illustrate process-aware and end-to-end evaluation; benchmark work warns that agent scores conflate harness and environment. [R3, R5, R6, R18] | Detect run-to-run variation, skill/hook regressions, and system-level failures before expanding autonomy. | Public benchmark scores are not a substitute for representative local tasks. Store only necessary traces and redact secrets/user data. |

### Current product surfaces checked

These are representative product capabilities, not endorsements. Product documentation is current as checked 2026-10-08; vendor feature availability and defaults can change.

- **Codex / OpenAI:** `AGENTS.md` instructions, skills, plugins and hooks, and sandbox guidance for isolated workloads and restricted credentials. [D1, D2, D12, D13]
- **Claude Code / Anthropic:** `CLAUDE.md`/skills, permission rules, lifecycle hooks including pre-tool blocking, and OS sandboxing for shell commands. The docs explicitly distinguish prompt instructions from enforced permissions and warn that sandboxing must be configured and verified. [D3, D4]
- **GitHub Copilot:** repository instructions, custom agents with explicit tool lists, and pre/post tool hooks. [D5, D6]
- **VS Code agent host:** workspace trust, tool approval, sandboxing, sensitive-file protections, worktree isolation, and MCP trust boundaries. [D7]
- **MCP Skills extension:** provenance/consent and untrusted-content requirements for served skills. [D8]
- **GitHub Code Security:** CodeQL code scanning, dependency review, and secret scanning. Use these as distinct CI checks, not one monolithic "AI safety" gate. [D9–D11]

## 3. Recommended fleet standard: policy and gates

### Non-negotiable policy

1. **Human owns the requirement; agent owns the draft.** Each task must state the behavior to change, acceptance criteria, relevant constraints, risk level, and allowed scope. If a necessary decision is ambiguous, stop and ask.
2. **No-change is a valid success result.** The agent must confirm the issue in current code before editing. If the requested behavior already exists, report the evidence and make no patch. [R1]
3. **Smallest sufficient patch.** No unrelated refactors, style sweeps, new frameworks, production dependencies, generated files, or architecture changes without an explicit reason and approval. Declare a change/file budget when the task requires one; exceeding it requires re-scoping.
4. **No test-oracle weakening.** Do not delete, skip, loosen, or rewrite an existing assertion just to get green. If a test must change, explain why and have the changed behavior independently reviewed. New tests must assert the intended outcome, not merely execute the path. [R4]
5. **No secret or high-privilege access by default.** Use a sandbox, least privilege, and restricted egress. Do not pass long-lived production credentials into an agent-readable environment. [D4, D7, D13]
6. **No autonomous merge, deployment, destructive action, external write, or irreversible operation** without explicit human authorization and an independent postcondition check.
7. **No unsupported completion claims.** The completion report must distinguish code changed, commands actually run, results observed, and checks not run. [R2, R5]

### Merge gates

A patch is acceptable only when every applicable gate passes or a named human accepts a documented exception.

| Gate | Required pass condition | Enforcement / evidence |
|---|---|---|
| **G0 — Task contract** | Behavior, acceptance criteria, scope, risk, and prohibited changes are stated. The task explicitly permits "no change" when applicable. | Human-approved issue/brief; ask before action if unresolved ambiguity changes design or data behavior. |
| **G1 — Safe starting state** | Correct repository/branch/worktree identified; pre-existing user changes recorded and preserved; no destructive cleanup of unknown files. | `git status`, current branch, and base commit recorded before edits. |
| **G2 — Scope and plan** | Agent identifies likely files and approach; changes remain within approved scope. Extra files/dependencies or broad architecture changes pause for approval. | Review changed-file list and diff. Compare against task contract; flag unrelated churn. |
| **G3 — Isolation and tool authority** | Agent runs with minimum required filesystem, command, network, and MCP permissions. Untrusted repository input cannot reach host secrets or deployment authority. | Workspace/container/worktree isolation, allowlisted tools/network, session-scoped approvals, audited hook/MCP configuration. |
| **G4 — Functional verification** | Relevant build and tests pass from a clean/pinned environment; bug fixes include a regression test where feasible; changed tests have meaningful oracles. | CI logs plus review of test assertions. Test selection must cover changed behavior and adjacent regressions. |
| **G5 — Deterministic quality checks** | Formatter, linter, type checker/compiler, and project-defined static checks pass. No new unexplained warnings/errors. | Reproducible CI job pinned to runtime/tool versions and dependency lockfiles. |
| **G6 — Security and supply chain** | No exposed secrets; no new critical/high security findings; dependency additions are justified, pinned, scanned, and approved. | Secret scanner, SAST, dependency/SCA review, relevant threat review. Exceptions name owner, rationale, expiry, and compensating control. |
| **G7 — Test and behavior integrity** | Existing tests were not weakened; test diffs are reviewed; high-risk logic receives stronger evidence than test counts alone (integration/contract/property/mutation testing as appropriate). | Test diff review; mutation or property tests for high-impact branches; no universal coverage threshold substituted for behavior. |
| **G8 — Readability and maintainability** | Code follows the repository’s established idiom, names concepts clearly, avoids unnecessary abstraction/duplication, and includes only comments that clarify non-obvious intent. | Human review against the codebase, API compatibility, error handling, logging/observability, and future ownership. |
| **G9 — Process truthfulness** | Report lists exact changed files, exact commands and exit results, skipped checks, residual risk, and whether any tool call failed or was retried. | Evidence-bearing final report; no "tests pass" unless the tests were actually run and observed passing. |
| **G10 — Human acceptance** | A maintainer independent of the generating run approves intent, risk, and diff. High-risk changes receive the relevant security/domain/architecture review. | Human approval before merge. AI reviewer may supplement but cannot satisfy this gate alone. |
| **G11 — External side effects** | Any command with external or irreversible side effects has explicit authorization and a verified postcondition; ambiguous timeout is checked before retry. | Approval record, idempotency key or equivalent protection, and postcondition evidence. [R14] |

### High-risk change classification

Require explicit human design/security review for authentication and authorization, cryptography, secrets, personal/regulated data, payments, access-control boundaries, database/schema migrations, data deletion, production infrastructure, network exposure, package-manager/build scripts, and code that executes untrusted content. For those changes, require a test/threat scenario that covers the failure path, not just the success path. AI-generated analysis can identify questions but cannot waive review.

### Reproducibility and agent-evaluation policy

- **For ordinary code acceptance:** use a pinned environment and deterministic CI checks. A flaky result is an unresolved defect in the test system; rerunning until green is not a pass.
- **For flaky-test investigation:** reproduce in a controlled environment, retain the failure log/seed, and verify the fix with repeated execution. [R14]
- **For comparing agent configurations:** test the *whole pairing*—model, harness, instructions/skills, tool set, and environment—on representative tasks. Record every run, not just the best. Report pass rate and the distribution of quality, cost, latency, tool failures, scope violations, and human intervention. [R5, R6, R18]
- **Run count:** use at least five independent trials as an inexpensive screening floor for a configuration change, not as proof of equivalence. For close comparisons or a high-impact rollout, collect enough runs for a power/uncertainty analysis; the recent repeated-run study needed tens to over 100 runs to resolve some differences. [R6]
- Include explicit **no-change**, ambiguous-requirement, tool-failure, and security-sensitive cases in the evaluation set. Score abstention and truthful reporting, not just patch success. [R1, R2]
- Keep an internal task set from real repository work. Public benchmarks are useful for context, but should not define the local release bar. [R3, R18]

## 4. Safe introduction of skills, tools, and extensions

Use this adoption sequence for every new skill, plugin, MCP server, hook, or agent model:

1. **Provenance:** record maintainer, source, license, exact version/commit/digest, permissions, network endpoints, executable scripts, and update channel.
2. **Review:** inspect all instructions, scripts, hook handlers, MCP schemas/descriptions, and default tool grants. Treat fetched content and repository text as untrusted input.
3. **Least privilege:** enable only necessary tools; prefer read-only access; deny write/deploy/secret access unless the task requires it. Pin MCP/plugin dependencies and re-review changes.
4. **Sandbox test:** exercise in a disposable workspace without production secrets; verify denied paths, network policy, and failure behavior. Do not trust that a configured sandbox actually started.
5. **A/B evaluation:** run the same representative tasks with and without the component. Measure success, test quality, scope violations, tool errors, latency, and token/cost impact. Retain a component only if it improves a named measure without unacceptable regressions. [R9, R16]
6. **Rollback and ownership:** assign a human owner, version the configuration, document the rollback command, and periodically revalidate after model/runtime updates.

**Do not solve a quality problem by installing more skills.** Research shows relevant skills can induce failures, and public skills have common routing/packaging defects. Start with one narrowly scoped procedure and a measurable hypothesis.

## 5. Recommended implementation order

Change one layer at a time so failures can be attributed and rollback is clear.

1. **Baseline first:** choose one representative repository; record current instructions, existing tests/checks, agent settings, permissions, and a small set of actual agent-task outcomes. Do not add new tools yet.
2. **Adopt the task and merge gates:** put concise negative constraints and commands in a repo-level instruction file; keep lint/format/type/test enforcement in CI. Add the no-change and exact-verification-report requirements.
3. **Harden execution:** use a disposable worktree/container, least-privilege permissions, explicit network policy, and no raw credentials. Add a small number of deterministic hooks only where CI cannot enforce a pre-action boundary.
4. **Add quality/security scanning:** enable the language-appropriate SAST, secret scan, dependency review, and lockfile checks. Baseline existing alerts before making new-finding policies blocking.
5. **Evaluate one skill or plugin at a time:** use the A/B protocol; do not bulk-install a marketplace pack.
6. **Build the internal agent regression set:** include normal implementation, bug fix, no-change, tests, dependency/security, and tool-failure tasks. Track repeat runs and human corrections before increasing autonomy.

**Recommended first action:** select one low-risk, actively maintained repository and establish its baseline (instructions, exact test/build commands, static checks, current sandbox/permissions, and several representative tasks). After that baseline is recorded, choose and test only the first gate change. The right repository has not been selected in this dossier.

## 6. Source register

### Primary research (all published/submitted within the cutoff window)

| ID | Human-authored source and date | Design, result used, and caveat |
|---|---|---|
| **R1** | Thibaud Gloaguen et al., “Coding Agents Don’t Know When to Act” / FixedBench, arXiv:2605.07769, **2026-05-08**. [Paper](https://arxiv.org/abs/2605.07769) | 200 human-verified no-change tasks; 35–65% undesirable code changes across evaluated agents. Preprint; task benchmark, not production incidence. |
| **R2** | Ningzhi Tang et al., “How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions,” arXiv:2605.29442, **2026-05-28** (v2 2026-08-31). [Paper](https://arxiv.org/abs/2605.29442) | Observational session study across 1,639 repos. Good field evidence for user-visible corrections and misalignment categories; observational and dependent on visible pushback. |
| **R3** | Hao Guan et al., “SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle,” arXiv:2605.13139, **2026-05-13**. [Paper](https://arxiv.org/abs/2605.13139) | 489 instances; decomposes environment, implementation, test generation, and full-cycle work. Preprint benchmark; authors report a sharp full-cycle drop. |
| **R4** | Dipayan Banik et al., “All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code,” arXiv:2606.18168, **2026-06-16**; accepted at the 8th IEEE International Conference on Artificial Intelligence Testing 2026. [Paper](https://arxiv.org/abs/2606.18168) | 86,156 test patches from 33,596 agent PRs; 80.2% weak/no explicit oracle signals. The paper’s PR corpus covers agents active from December 2024 to July 2025, so this is a recent publication about a historical artifact sample, not a 2026 prevalence estimate. Its oracle taxonomy is syntactic, not a full semantic judgment of every test. |
| **R5** | Priyam Sahoo et al., “AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation,” arXiv:2605.12925, **2026-05-13** (v4 2026-10-05). [Paper](https://arxiv.org/abs/2605.12925) | 2,614 trajectories, eight backends, 60 tasks; 10.7% Lucky Passes within the paper’s passing-trajectory subset. Preprint; task/agent scope is bounded. |
| **R6** | Eduardo Ariño de la Rubia and Szilard Pafka, “Identical Runs, Different Results: Benchmarking AI Coding Agents on Open-Weight Models,” arXiv:2609.33812, **2026-09-27**. [Paper and code](https://arxiv.org/abs/2609.33812) | 584 runs; deep repeated-run experiment on one XGBoost airline-delay optimization task. Strong evidence for variance in that setting; not a universal estimate for all coding tasks. |
| **R7** | Youssef Esseddiq Ouatiti et al., “Do AI Coding Agents Log Like Humans? An Empirical Study,” arXiv:2604.09409, **2026-04-10**. [Paper](https://arxiv.org/abs/2604.09409) | 4,550 PRs across 81 repos; logging changes and human repairs. Preprint; repo-level observational analysis. |
| **R8** | Xing Zhang et al., “Guardrails Beat Guidance: A Large-Scale Study of Rules, Skills, and Persistent Configuration for Coding Agents,” arXiv:2604.11088, **2026-04-13** (v2 2026-05-28). [Paper](https://arxiv.org/abs/2604.11088) | 679 files/25,532 rules and 5,000+ Claude Code runs on a SWE-bench subset. Rule-polarity result is specific to its model, benchmark, and methods; do not overgeneralize. |
| **R9** | Yanjie Gao et al., “Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents,” arXiv:2608.11888, **2026-08-12**. [Paper](https://arxiv.org/abs/2608.11888) | Differential analysis on SkillsBench and SWE-Skills-Bench; 307 attributed functional/efficiency regressions. Preprint; useful evidence that skills need evaluation, not a claim that all skills harm. |
| **R10** | Zahra Mousavi et al., “Understanding the Impact of AI Code Assistants on Security API Usage: An Empirical Study,” arXiv:2607.11348, **2026-07-13**; accepted at RAID 2026. [Paper](https://arxiv.org/abs/2607.11348) | Controlled study with 44 developers using tasks with/without Copilot. Small sample and studied APIs/tasks; does not estimate universal vulnerability rates. |
| **R11** | Faisal Haque Bappy et al., “From Preventive to Reactive: How AI Coding Assistants Transform Developers’ Security Awareness,” arXiv:2605.23130, **2026-05-22** (v2 2026-06-10); accepted at SOUPS 2026. [Paper](https://arxiv.org/abs/2605.23130) | Interviews/observed tasks with 15 professional engineers. Practice-grounded but small qualitative sample. |
| **R12** | Tatsuya Shirai et al., “To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study,” arXiv:2605.06464, **2026-05-07** (v2 2026-05-09); accepted at EASE 2026. [Paper](https://arxiv.org/abs/2605.06464) | 1,000+ files and ~3,200 changes across 100 repos. Maintenance frequency is not a direct maintainability score. |
| **R13** | Hidetake Tanaka et al., “Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study,” arXiv:2605.22534, **2026-05-21**; accepted at MSR 2026. [Paper](https://arxiv.org/abs/2605.22534) | 11,048 closed PRs; 9,799 human-reviewed and 717 manually inspected. Shows PR outcome labels need review-interaction context. |
| **R14** | Abhishek Phadke et al., “Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures,” arXiv:2608.02645, **2026-07-31**. [Paper](https://arxiv.org/abs/2608.02645) | Controlled simulated failure setting. Supports postcondition/idempotency design; not direct evidence about every coding-agent runtime. |
| **R15** | Benjamin Kapner et al., “Scanning the Harness: Configuration Exposures in AI Coding-Agent Supply Chains,” arXiv:2609.07360, **2026-09-07** (v3 2026-09-25). [Paper, data, tool](https://arxiv.org/abs/2609.07360) | Static/configuration audit of 3,171 public GitHub repos. Runtime exploitability and scanner recall unmeasured; use exposure rates as configuration findings, not incident rates. |
| **R16** | Yimin Liu et al., “What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files,” arXiv:2608.08453, **2026-08-09**. [Paper](https://arxiv.org/abs/2608.08453) | 138,133 public skill files; defect taxonomy and routing stress test. Public corpus and detected-defect definition limit generalization; defects are not equivalent to maliciousness. |
| **R17** | Mikhail Surikov V., “Securing AI-Generated Code: A Just-in-Time Vulnerability Detection and Remediation Pipeline,” arXiv:2608.16187, **2026-08-17**. [Paper and code](https://arxiv.org/abs/2608.16187) | 80 runs, 26 Python prompts, nine CWE categories; CodeQL/Bandit plus LLM review/remediation. Master's practicum preprint; preliminary, narrow, and remediation introduced new findings. |
| **R18** | Maria I. Gorinova et al., “Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering,” arXiv:2606.17799, **2026-06-16** (v2 2026-07-18). [Paper](https://arxiv.org/abs/2606.17799) | Position paper arguing model/harness/context/environment are conflated in benchmark scores. A conceptual critique, not a new controlled experiment. |

### Current product documentation (accessed 2026-10-08; rolling pages)

| ID | Product documentation | Use in this dossier |
|---|---|---|
| **D1** | OpenAI, [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md) | Codex instruction discovery and scope. |
| **D2** | OpenAI, [Build skills](https://developers.openai.com/codex/skills) | Skill structure, progressive disclosure, and installation locations. |
| **D3** | Anthropic, [Claude Code hooks](https://code.claude.com/docs/en/hooks), [permissions](https://code.claude.com/docs/en/permissions), [skills](https://code.claude.com/docs/en/skills) | Lifecycle hooks, enforced permission rules, and runtime skills. |
| **D4** | Anthropic, [Claude Code sandbox](https://code.claude.com/docs/en/sandboxing) | Shell filesystem/network boundaries and fail-closed configuration. |
| **D5** | GitHub, [Copilot custom agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents) | Agent profiles and tool allowlists. |
| **D6** | GitHub, [Copilot hooks](https://docs.github.com/en/copilot/concepts/agents/hooks) | Pre/post tool hook capability and hook security guidance. |
| **D7** | Microsoft, [Secure AI-assisted development in VS Code](https://code.visualstudio.com/docs/agents/run/security) | Workspace trust, sandboxing, approvals, sensitive files, and worktree isolation. |
| **D8** | Model Context Protocol, [Skills Extension specification](https://skills.extensions.modelcontextprotocol.io/specification/stable/skills) | Skill content as untrusted input; protocol page states revision 2026-07-28 or later. |
| **D9** | GitHub, [Code scanning with CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql) | Static-analysis capability and language support. |
| **D10** | GitHub, [Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) | PR dependency change review. |
| **D11** | GitHub, [Secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) | Credential detection and repository-level secret controls. |
| **D12** | OpenAI, [Package your plugin](https://developers.openai.com/plugins/build/plugins) | Plugin structure and lifecycle hooks; plugin hooks are reviewed/trusted before use. |
| **D13** | OpenAI, [Sandbox security](https://developers.openai.com/api/docs/guides/agents-api/environments/security) | Isolated workloads, egress restrictions, credential separation, and external secret brokering. |

## Bottom line

The excellence standard should be **evidence-first and gate-driven**: specify intent, constrain authority, make tests meaningful, block deterministic hazards mechanically, and require a human to accept the design and risk. Keep skills and extensions few, pinned, and measured. For every claim of completion, require observable evidence. For every new agent capability, require a rollback and a before/after evaluation.
