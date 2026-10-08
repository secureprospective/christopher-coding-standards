# Coding-standards rebuild: independent evidence and implementation-path audit

**Date:** 2026-10-08  
**Target supplied by parent:** `main`, `93ee82a346289f7fdf77a696a20a999ffcc61dc6`  
**Authority:** Read-only research and planning input—not implementation or policy approval.  
**Artifact:** `/home/chris/scratch/coding-standards-rebuild-research-pass.md`

## Scope and evidence convention

Read the four required documents in order, then canonical ADR-0001, multi-agent roles, AGENTS, INDEX, adoption instructions, relevant template instructions/configuration, and bounded installed Pi-subagents technical documentation.

All **18 research identities/submission histories** and **13 official documentation surfaces** were reachable. Material paper claims were checked against HTML full text, not just abstracts. Author metadata was inspected separately because readable HTML sometimes omitted authors.

- **Verified** means the inspected source supports the stated, scoped claim—not that the experiment was independently reproduced.
- **Partly supported** means there is a material wording, denominator, identity, interpretation, or verification limitation.
- Access date is not publication date.
- Named authors and institutional affiliations do **not** establish human-only authorship.
- No tools installed, fetched code executed, tests run, credentials/settings/private transcripts inspected, consumers changed, or fleet machines contacted.
- Consumer hash matches/worktree inventory in the earlier investigation were **not independently rerun**. They remain attributed local investigation evidence.
- `source_check` was used for consequential claims. Its returned assessments were consistently `unclear` because automated semantic assessment was unavailable; the conclusions below come from manual inspection of primary passages.

---

# A. Executive findings and corrections

## 1. Verified claims

**Supported, high confidence:** The dossier’s central recommendation remains defensible: treat generated output as a draft; establish intent and scope; use executable verification; constrain authority; preserve independent human acceptance.

The strongest directly relevant evidence concerns:

- Unnecessary edits to already-fixed issues: R1.
- User-visible misalignment and inaccurate reporting: R2.
- Weak test-oracle signals: R4.
- Run-to-run and harness-dependent variation: R5–R6.
- Skills imposing incorrect implementation or unnecessary procedures: R9.
- Configuration dependencies and broad grants requiring review: R15.
- Verify-before-retry after ambiguous writes: R14, with substantial simulation limitations.

These support **risk-sensitive engineering controls**, not twelve universally mandatory conversational gates or an expensive evaluation ritual for every change.

## 2. Contradicted claims

### Highest design impact

1. **Worktrees are not security sandboxes.**  
   **Status: contradicted; high confidence.** Git documents shared repository administration and separate working trees—not filesystem, process, credential, or network confinement. VS Code describes worktrees as preventing workspace conflicts. Dossier G3 and isolation examples need this distinction.

2. **“Hooks enforce deterministic requirements” is too broad without event/version/failure semantics.**  
   **Status: contradicted as a blanket assurance; high confidence.** Current Claude documentation says ordinary command/HTTP/MCP `PreToolUse` hook timeouts do not block the tool call; most nonzero exits other than `2` are nonblocking absent valid decision JSON. Post-tool hooks cannot undo execution. Installed Pi-subagents watchdog reviews occur after activity; native child permissions are opt-in and always pass Bash through.

3. **The ADR/AGENTS empirical justification for universally excluding architecture overviews is overstated.**  
   **Status: contradicted as a universal empirical conclusion; high confidence.** The latest ETH paper says instructions change behavior and increase testing/exploration. Appendix B reports benefits when other documentation is absent; overview removal did not significantly improve accuracy. A short, maintained routing/map policy remains a reasonable **design choice**, but this paper does not prove every overview is useless or behavior-neutral.

### Research-register corrections

- R9 first author: **Gen Dong**, not Yanjie Gao.
- R12 first author: **Shota Sawada**, not Tatsuya Shirai.
- R13 first author: **Sien Reeve O. Peralta**, not Hidetake Tanaka.
- R14 first author: **Isham Kalappurackal Mansoor**, not Abhishek Phadke.
- R16 first author: **Chi Zhang**, not Yimin Liu.
- R17 author metadata: **Mikhail Surikov**, not “Mikhail Surikov V.”
- R15’s 15.4% is **409/2,660 assembled setups**, not 15.4% of all 3,171 repositories.
- R13’s 35.7% is **126/353 manually inspected rejected PRs**, not a directly measured proportion of every rejected PR in the larger corpus.
- R11 interviewed 15 people; **14 undertook coding tasks**.

## 3. Weak / unclear / unsupported claims

- **Negative instructions universally outperform positive instructions:** unsupported. R8’s decisive polarity analysis covers 18 curated rules on 35 selected Python bug-fix tasks, one model/harness. Only one individual effect was significant, and not under strict multiple-comparison correction.
- **R7’s “67% constructive-request noncompliance”: unclear.** Its detailed table does not support that denominator consistently; see B.
- **Five runs as a universal screening floor:** policy suggestion, not an evidence-derived universal minimum.
- **A/B every component:** useful for behavior-changing configurations, excessive for many mechanical maintenance changes.
- **Assertion-count or regex gates establish oracle quality:** unsupported. R4 explicitly measures syntactic signals, not whether assertions check the intended property.
- **All current LLMs are measurably less secure than human-written code:** unsupported universal statement in ADR-0001. The inspected studies examine particular systems/tasks/populations.
- **Free tooling provides equivalent paid-tool capability:** unsupported. Similar control categories do not imply equivalent detection, integration, support, or licensing.
- **Installed documentation proves deployed protection:** unsupported. Neither active Pi core version nor effective loaded guard/sandbox/permission policy was established here.

## 4. Material source-quality concerns

- Several papers are preprints; R18 is a vendor-affiliated position argument; R17 is a master’s practicum.
- R4, R7, R12 and R13 substantially reuse historical AIDev artifacts. They are not four independent measurements of today’s fleet.
- R2 identifies failures through visible developer pushback, making its correction rate conditional and subject to ascertainment bias.
- R5’s “Lucky Pass” is a process-score classification—not independently demonstrated patch fragility in every classified case.
- R16 combines cosmetic/advisory packaging judgments with safety defects and lacks the manual precision audit it identifies as important.
- Official rolling docs describe capabilities, not deployment assurance or comparative effectiveness.
- Conference acceptance was independently corroborated for R11 and R12; R4/R10/R13 acceptance claims remain incompletely verified.

## 5. Missing evidence

No independent evidence was obtained for:

- Actual active Pi core build, parent/child loadouts, guard configuration, OS containment, network denial, or credentials exposed to execution.
- Hosted branch protections, required-check applicability, bypass privileges, or current passing CI.
- Full seven-overlay compatibility, actual hooks, installs, mutation tests, or consumer lockfiles.
- Historical consumer adoption provenance.
- Fleet inventory completeness or durable registry authority.
- Numeric token savings from the proposed tracker.
- Full ADR vendor-statistic accuracy, especially secondary comparative claims.
- Complete current runtime implementations of the MCP Skills extension.

## 6. Material contradictions

Preserve these rather than silently choosing a convenient interpretation:

- **R7:** headline/summary “67%” conflicts with detailed instruction-channel counts.
- **R16:** its “official-spec conformance” category includes requirements stronger than the inspected Agent Skills specification.
- **D12:** the page specifically restricts plugin lifecycle hooks to manually installed Codex desktop plugins, but later includes broader ChatGPT Work/Codex wording. Do not infer blanket CLI hook support.
- **Canonical guidance versus shipped files:** AGENTS prohibits mutable action pins; `security.yml` still ships multiple mutable tags. “Hook wins” also grants excessive authority if the hook/configuration itself is compromised.
- **Current role document versus actual authorized orchestration:** the document asserts no direct agent channel and a sole vendor-mapped audit role; installed Pi-subagents documentation and this commissioned task demonstrate materially different capability surfaces. This is a governance update question—not permission to rewrite it.
- **Tracking-first request versus dossier gate-first rollout:** resolve with a read-only baseline/tracker first, while handling known security fixes separately.

## 7. Implications for the original conclusion

**Retain the direction; narrow the promises and sequencing.**

The evidence supports a small advisory core, executable stack gates, explicit authority boundaries, honest verification reporting, reviewed dependencies, and proportionate evaluation.

It does **not** justify universal negative-only instructions, worktree-only containment, unconditional hook assurance, always-five-run evaluations, automatically trusted receipts, or an unattended updater.

**Reasoned default proposal:** approve the schema/ownership model and a read-only, offline-first tracker before broader modernization. Keep containment and enforcement evidence separate. Durable fleet choices require Christopher’s authorization plus ClaudeBox context and expert review.

---

# B. R1–R18 research claim register

All links below are primary arXiv records/full text. Dates are first submissions, followed by relevant revisions. Confidence concerns source correspondence, not independent reproducibility.

| ID | Correct identity/date | Primary passage and finding | Verdict, scope and confidence |
|---|---|---|---|
| **R1** | **Thibaud Gloaguen et al.**, *Coding Agents Don’t Know When to Act*. **2026-05-08**, v1. [Text](https://arxiv.org/html/2605.07769v1) | §3.1–3.2, Fig. 2/Table 1: 200 SWE-bench-derived already-fixed tasks; unnecessary production-code edits **35–65%**, excluding tests/documentation. Models: Sonnet 4.6, GPT-5.3 Codex, GPT-5.4 mini, Gemini 3 Pro, Qwen3.5-122B; corresponding four harness families, plus SORCAR experiment. §5: Python/popular repositories only. | **Verified / supported; high.** Verify-and-abstain framing helps, but reproduction alone can worsen abstention and partial fixes create over-abstention. Does not establish a universal production incident rate or require bug reproduction for new features. |
| **R2** | **Ningzhi Tang et al.**, title as dossier. **2026-05-28**; v2 **2026-08-31**. [Text](https://arxiv.org/html/2605.29442v2) | §3.1: SpecStory **September 2024–April 2026**, recrawled April 30; Entire.io **January–April 2026**. §3.3: **16,118** retained episodes from 29,896 candidates. §4.2: visible resolution for **1,504 episodes/9.33%**; **91.49% of those** required pushback. | **Verified / supported with essential denominator; high.** Not 91.49% of sessions or all failures. Selection favors public logging and visible dissatisfaction. GPT-5.4 extraction/annotation; estimated precision .93, average annotation accuracy .82. Model-specific failure comparisons unavailable. |
| **R3** | **Hao Guan et al.**, *SWE-Cycle…*. **2026-05-13**, v1. [Text](https://arxiv.org/html/2605.13139v1) | §4.1–4.3: **489 instances**, OpenCode **1.4.6**, Docker; six models: GPT-5.4, Sonnet 4.6, Qwen3.5, GLM-5.1, Kimi-K2.5, MiniMax-M2.7. 90-minute isolated/3-hour FullCycle budgets. “**No model achieves a strict overall solve rate above 14%**.” | **Verified / supported; high.** Strict full-cycle success is a conjunction of phases, not directly equivalent to one-phase solve rate. SWE-Judge uses Opus 4.5, reference patches, dynamic checks and sometimes refined tests; not a purely deterministic independent oracle. No production deploy evaluation. |
| **R4** | **Dipayan Banik, Kowshik Chowdhury, Shazibul Islam Shamim**, *All Smoke, No Alarm…*. **2026-06-16**, v1. [Text](https://arxiv.org/html/2606.18168v1) | §II, §III-A/Fig. 1, §III-B and §V: **86,156 cumulative test-file patches**, **33,596 PRs**, 2,807 repositories; **80.2% W1–W5**. Adjusted OR **1.28**, p<.001. Corpus **December 2024–July 2025**; Codex contributes 65%. | **Partly supported; high for numbers, lower for semantic interpretation.** Modified patches may omit existing assertions; implicit failure oracles are missed. “Equality check exists” does not establish correct property. Merge association remains observational. IEEE AI Testing acceptance appears in author comments but was not independently confirmed from proceedings/program. |
| **R5** | **Priyam Sahoo et al.**, *AgentLens…*. **2026-05-13**; v4 **2026-10-05**. [Text](https://arxiv.org/html/2605.12925v4) | §4–5.1: **2,614 OpenHands trajectories/60 tasks**; eligible **1,815/47 tasks**, including **1,136 passing**. Lucky: **122/1,136 = 10.7%**. §3.4: passing score <47 defines Lucky. §5.2/Table 2 discusses conditional ranking changes. | **Verified / supported as framework classification; high.** Eight backends include GPT-4.1/4o, Codex 5.2/5.3, Sonnet 4.5, Opus 4.5/4.6, Gemini 2.5 Pro. Process reference/threshold choices affect classification; valid atypical strategies are a concern. Not 10.7% proven defective patches. |
| **R6** | **Eduardo Ariño de la Rubia and Szilard Pafka**, *Identical Runs, Different Results…*. **2026-09-27**, v1. [Text](https://arxiv.org/html/2609.33812v1) | §3/Table 1: **584 runs =116+312+156**, collected **September 13–17, 2026**. Deep study: six pairings ×52 runs on one airline-delay XGBoost task. Includes **Pi 0.85.1**, OpenCode, Hermes; exploratory study also Claude Code, Codex, OpenClaw. §3.6: illustrated counts use observed variance/gap, **not general requirements**. | **Verified / supported; high.** Hosted model builds/routing unrecorded; endpoints and adjacent-day model arms remain confounders. Data from 2005–2007; task description mislabeled actual departure time as scheduled. Explicitly distinguishes comparison from repeat-and-select. No justification for five runs everywhere or rejecting every lawful best-of-k workflow. |
| **R7** | **Youssef Esseddiq Ouatiti et al.**, *Do AI Coding Agents Log Like Humans?*. **2026-04-10**, v1. [Text](https://arxiv.org/html/2604.09409v1) | §3: initial **81 repositories**, final **77** after excluding four with no logs. RQ1: **58.4%** fewer logging-changing PRs. RQ3: humans perform **72.5% of logging-statement modifications**. RQ2/Table 6: issue Add 2/5, Modify 3/8, Remove 0/2; repository Add 3/36, Remove 10/10. | **Partly supported / unclear for 67%; high confidence in discrepancy.** 67% corresponds approximately to issue-channel failure across all 15 requests, not all constructive requests across both channels. Constructive Add/Modify total is 8/49 compliant from table, while issue-only is 5/13. Source also inconsistently summarizes repository removals. Do not substitute an invented headline. Observational AIDev study; loading of repository instructions is explicitly uncertain. |
| **R8** | **Xing Zhang et al.**, *Guardrails Beat Guidance…*. **2026-04-13**; v2 **2026-05-28**. [Text](https://arxiv.org/html/2604.11088v2) | §5–6.4/Table 1: 679 files/25,532 rules; Claude Code+**Opus 4.6**; >5,000 runs. Screening selected **58 discriminative tasks**; polarity ablation **35 tasks/18 curated rules**: 3 shaping negative, 4 distorting positive, 11 inert. Only “avoid unrelated refactoring” individually significant; would not survive strict correction. | **Verified as scoped finding; universal inference unsupported.** Python SWE-bench bug fixes, single vendor/model/harness; task-selection bias and ensemble interactions. §7 explicitly limits generalization. Supports testing instructions, not deleting positive acceptance requirements or project facts. |
| **R9** | **Gen Dong et al.**, *Agent Skills Can Be Harmful…*. **2026-08-12**, v1. [Text](https://arxiv.org/html/2608.11888v1) | §III/Table II: OpenCode **1.15.1**+Opus 4.6; SkillsBench **84 tasks**, SWE-Skills-Bench **490**. **665 candidates →307 retained cases:125 functional/182 efficiency**. Only **38 functional cases** are with/no-skill; **87** are cross-skill. Efficiency requires both time/tokens worse and at least one >2×. | **Partly supported; high.** Dossier first-author attribution incorrect. Counts are curated attributed cases, not prevalence. Successful alternative is a pseudo-oracle; paired single-run differences and attribution cannot eliminate stochastic confounding. Supports targeted evaluation, not a universal mandatory A/B ceremony. |
| **R10** | **Zahra Mousavi et al.**, *Understanding the Impact…Security API Usage*. **2026-07-13**, v1. [Text](https://arxiv.org/html/2607.11348v1) | §3–4: **44 developers**, counterbalanced within-subject two-task design; Java JSSE/OAuth; Copilot **1.250.0/GPT-4o**. OAuth functional completion **20/22 versus10/22**; JSSE functional for all. Security evaluation only functional/semi-functional submissions; none fully secure under taxonomy. | **Partly supported; high for study claim.** No significant secure-use improvement is not equivalence or proof of harm in all settings. Historic Copilot, restricted APIs, participant selection/time limits. RAID acceptance author-reported; publisher DOI fetch returned406, so external acceptance verification incomplete. |
| **R11** | **Faisal Haque Bappy et al.**, *From Preventive to Reactive…*. **2026-05-22**; v2 **2026-06-10**. [Text](https://arxiv.org/html/2605.23130v2); [USENIX](https://www.usenix.org/conference/soups2026/presentation/bappy) | §3/Table 1: interviews **November2025–January2026**,15 professionals; **P13 declined coding**, leaving14. Gemini CLI+Gemini2.5 Pro, self-selected tasks without explicit security requirements. Initial prompting observation applies to coding participants. | **Partly supported; high.** Qualitative evidence of practices, not causal identification of a population-wide transition. SOUPS presence corroborated by official USENIX page. |
| **R12** | **Shota Sawada et al.**, *To What Extent Does Agent-generated Code Require Maintenance?*. **2026-05-07**; v2 **2026-05-09**. [Text](https://arxiv.org/html/2605.06464v2); [EASE program](https://conf.researchr.org/details/ease-2026/ease-2026-short-papers-and-emerging-results/24/To-What-Extent-Does-Agent-generated-Code-Require-Maintenance-An-Empirical-Study) | §3–4/Tables1–2: **508 agent+508 human files**,100 repositories; **1,543+1,695=3,238 subsequent commits** through **January31,2026**. Initial PRs December2024–July2025. Humans authored **1,284/1,543=83.21%** maintenance commits to agent files. | **Partly supported; high.** First-author attribution wrong. “1,000+ files” means combined sample, not1,000+ agent files. Codex excluded; bot-account attribution cannot identify undisclosed AI assistance. Lower maintenance frequency is not proof of lower maintenance need. EASE short-paper program independently confirms presence. |
| **R13** | **Sien Reeve O. Peralta et al.**, *Why Are Agentic Pull Requests Merged or Rejected?*. **2026-05-21**, v1. [Text](https://arxiv.org/html/2605.22534v1) | §3–6/Tables2–3:11,048 closed PRs→9,799 human-reviewed; manual717=**353 rejected+364 merged**. Clear failure **126/353=35.7%**; workflow110, unknown117. Explicit involvement **56/364=15.4%** merged. Repositories≥500stars. | **Partly supported; high.** First author wrong; percentages belong to manual subsamples. Unknown rationale does not establish no failure. Proceedings header gives MSR April13–14 and DOI10.1145/3793302.3793575; publisher fetch406/program retrieval incomplete, so external proceedings confirmation unfinished. |
| **R14** | **Isham Kalappurackal Mansoor, Abhishek Phadke, Pratip Rana**, *Verified Tool Calls…*. **2026-07-31**, v1; manuscript itself displays August24. [Text](https://arxiv.org/html/2608.02645v1) | §4.4–4.6, §5, §7: Gemini Flash-Lite/LangGraph; **300 main runs**, two simulated workflows, three fault levels,25episodes per arm. Handwritten True/False/Unknown verifiers; retry budget1. Baseline explicitly instructed direct retry without verification/idempotency. | **Partly supported; high.** July31 submission is correct despite2608identifier. First author wrong. Controlled wrapper/prompt comparison against deliberately weak baseline—not broad production evidence. Timestamp-bucket key example should not be copied blindly: one logical operation needs one durable retry identity. |
| **R15** | **Benjamin Kapner et al.**, *Scanning the Harness…*. **2026-09-07**; v3 **2026-09-25**. [Text](https://arxiv.org/html/2609.07360v3) | §3–4/Table1: scans dated **September6,2026**;3,171repos=**2,660 setups+511collections**. Unpinned260/2,660=9.8%; broad execution67=2.5%; skill grants101=3.8%; overlapping union409=15.4%. | **Partly supported; high.** Dossier conflates total repos with setup denominator. Runtime consequences/recall unmeasured. Mechanical agreement cannot exclude shared mistakes; documented `find` permission semantics required corrections. Transitive resolution and client versions matter. |
| **R16** | **Chi Zhang et al.**, *What Keeps Agent Skills from Being Reusable?*. **2026-08-09**, v1. [Text](https://arxiv.org/html/2608.08453v1) | §3–4,§6:138,133 SHA256-deduplicated files/20,556repos; **91.8% at least one detected taxonomy defect**.31checks; BM25 routing probe20,000skills—not production agent routing. §6 admits missing manual precision audit for safety/persona detectors. | **Partly supported; high.** First author wrong. Taxonomy calls advisory constraints “spec conformance”: e.g.30–300description bounds versus actual1–1024; heading duplication/body format also not hard specification prohibitions. Cosmetic and safety findings bundled. Manuscript workshop dateMay26 versusAugustsubmission warrants date caution, not invented acceptance. |
| **R17** | **Mikhail Surikov**, *Securing AI-Generated Code…*. **2026-08-17**, v1. [Text](https://arxiv.org/html/2608.16187v1) | §3.4,§5.4/Tables6–7,§7:80pipeline runs; **each covers26Python prompts**, four Claude models, two configurations,10repeats. **15–22% of remediations** introduce ≥1new static finding. | **Partly supported; high.** Author formatting wrong. “New vulnerability” should be “new static finding”; no exploitability or functional correctness evaluation, severity unweighted, potential benchmark exposure. Practicum evidence supports rescan/review—not autonomous remediation assurance. |
| **R18** | **Maria I. Gorinova et al.**, *Position: Coding Benchmarks Are Misaligned…*. **2026-06-16**; v2 **2026-07-18**. [Text](https://arxiv.org/html/2606.17799v2) | Introduction/argument: agent is composite model+harness+context+environment+feedback; aggregate scores can obscure component effects and reference-solution limitations. Authors affiliated with Tessl. | **Verified / supported as position argument; high.** Not a new controlled experiment or proof all benchmark grading uses one reference solution. Useful framing; empirical support should come from the cited experiments/local evidence. |

### Register coverage limits

All identities, submission histories and material headline claims were inspected. No independent reproduction or raw-dataset recalculation was performed. Exact collection dates and deployed harness versions are unavailable or incomplete in several observational papers; do not fill them in by inference. Conference comments alone were not treated as confirmation.

---

# C. D1–D13 capability register and Pi applicability

All are rolling documentation accessed during this audit. **None proves local deployment or current licensed entitlement.**

| ID | Inspected official source | Verdict and runtime/enforcement limits | Pi relevance |
|---|---|---|---|
| **D1** | [Codex AGENTS](https://developers.openai.com/codex/guides/agents-md) | **Verified.** Global→root→cwd discovery, override precedence, once-per-run chain, default32KiB limit. Prompt guidance, not mechanical policy. | Do not transplant discovery assumptions without adapter verification. |
| **D2** | [Codex skills](https://developers.openai.com/codex/skills) | **Verified.** Metadata-first disclosure; full content on selection; explicit/implicit activation. Current initial-list budget2%context/8,000characters fallback. Symlink discovery increases provenance/path considerations. | Pi also progressively loads skills; installed inventory still costs context and requires review. |
| **D3** | [Hooks](https://code.claude.com/docs/en/hooks), [permissions](https://code.claude.com/docs/en/permissions), [skills](https://code.claude.com/docs/en/skills) | **Partly supported.** Real pre-tool deny/ask capability, but event-specific outputs/exits matter. Ordinary pre-tool hook timeout can fail open; post-action hooks cannot prevent completed action. `allowed-tools` can preapprove, not define an exclusive security ceiling. | Pi extension `tool_call` can block; separate from Claude hooks and Pi-subagents watchdog. |
| **D4** | [Claude sandbox](https://code.claude.com/docs/en/sandboxing) | **Partly supported.** OS enforcement for sandboxed Bash; not entire Claude process. Strict configuration needs `enabled`, `failIfUnavailable`, `allowUnsandboxedCommands:false`, exclusions and egress review. Default unavailable sandbox can fall back unsandboxed. Platform constraints include native Windows limitation. | No transfer to Pi. Whole-process containment protects more than a shell-tool-only wrapper. |
| **D5** | [Copilot custom agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents) | **Verified.** Profiles include prompts, tools/MCP. Omitted tools default to all available tools. Profile prose restricting edits is not equivalent to removing edit capability. Product/account access required. | Role names are not security properties; inventory actual tool ceiling. |
| **D6** | [Copilot hooks](https://docs.github.com/en/copilot/concepts/agents/hooks) | **Verified capability; behavior untested.** CLI/cloud-agent preToolUse approval/denial; postToolUse logging; repository/personal hook scopes. Do not extrapolate to every IDE implementation. Scripts inherit environment and require input sanitation/permissions. | Build only an explicitly selected runtime adapter; no universal hook file. |
| **D7** | [VS Code security](https://code.visualstudio.com/docs/agents/run/security) | **Partly supported.** Workspace trust, approvals and OS shell/process sandboxing are separate layers. Network enabled by default in documented setting. Worktree prevents workspace conflict—not host isolation. Sensitive-file edit approval is not subprocess read denial. Provider harnesses differ. | No evidence VS Code protection surrounds present Pi session. |
| **D8** | [MCP Skills](https://skills.extensions.modelcontextprotocol.io/specification/stable/skills), [overview](https://skills.extensions.modelcontextprotocol.io/) | **Verified specification; availability unclear.** Published stable extension page, accepted SEP2640, base revision2026-07-28+. Capability negotiation required. Ordinary resources/read does not activate skill. Skills untrusted/higher-risk; digests explicitly not security boundary; execution/tool grants need consent. | Ordinary Agent Skills support does not prove this MCP extension implemented. No local negotiation/activation evidence. |
| **D9** | [CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql), [CLI](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-cli) | **Verified with licensing limits.** Supported languages/framework models only; no-alert result can be incomplete. CLI free for public repositories; private organization use documented with Team/Enterprise Cloud and Code Security license. Queries/rule packs separate from pinned action. | Optional gate—not unconditional free-first requirement. |
| **D10** | [Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) | **Verified with limits.** PR dependency diff/known vulnerabilities; action public availability, private requires Code Security/Advanced Security. Uses API; snapshot sequencing can miss dependencies. Blocking merge requires required-check configuration. | Not offline and not deployment assurance. |
| **D11** | [Secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) | **Verified with limits.** Public scanning free; private/internal plan/product conditions. Known patterns, provider notification and validity checks differ from local scanner. Validity checks contact issuing services. | Needs explicit data/network authority; cannot replace credential separation. |
| **D12** | [Plugin packaging](https://developers.openai.com/plugins/build/plugins) | **Partly supported.** Explicitly documents lifecycle hooks for manually installed Codex desktop plugins, not public directory eligibility. Hooks skipped until reviewed/trusted. Broader later wording does not establish universal CLI/API availability or pre-action coverage. | No Pi capability inference. Pin/review plugin scripts and dependencies independently. |
| **D13** | [Agents API sandbox security](https://developers.openai.com/api/docs/guides/agents-api/environments/security) | **Verified guidance; wrong surface if treated as CLI guarantee.** API executor environment, restricted environment key, external credential broker and network architecture. Self-hosted isolation/proxy are infrastructure operator supplies. Generated code can read exposed keys. | General threat model relevant; exact API mechanisms not evidence of Pi/Codex CLI configuration. |

## Actual Pi-related evidence

**Installed package inspected:** `pi-subagents` **0.76.1**, MIT. This is an installed package identity, **not proof of the running core version or effective settings**.

Primary public Pi documents:

- [Run Pi safely](https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/security.md): Pi acts with launching account’s permissions; working folder is not confinement; project trust controls startup resources, not tool authority; context files may load irrespective of project trust.
- [Extensions](https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/extensions.md): extensions execute inside Pi with OS-user permissions. `tool_call` handlers can block; current docs say handler failure blocks. This is documented behavior, not tested deployed behavior.
- [Skills](https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/skills.md): metadata-first loading, explicit invocation, portability warnings; validation is not uniformly fail-closed.

Installed `pi-subagents/docs/watchdog.md`:

> “With no rules, every tool call passes through.”

> “omitted and unknown tools default to allow”

> “Bash is always passed through”

Native child permission arbitration can deny on missing watchdog/model/timeout, but is **opt-in**, tool-specific and not OS isolation. External CLI tools cannot be intercepted by that native gate.

Installed workflow docs distinguish a JavaScript workflow sandbox from child execution. A workflow without filesystem globals does **not** sandbox tools available to its children.

**Proposal:** baseline the actual parent, foreground child, background child and external-runner surfaces separately. Do not inspect private settings automatically; obtain an owner-approved, redacted capability attestation and disposable canary tests.

## Free-first complications beyond D9–D11

- [Semgrep licensing](https://semgrep.dev/docs/licensing): CE engine LGPL2.1; maintained rules have separate internal-business-use license; third-party rules retain their own licenses. Engine openness does not grant unrestricted rule redistribution.
- [Gitleaks Action README](https://raw.githubusercontent.com/gitleaks/gitleaks-action/master/README.md): organization use requires a license key, described as free; action license differs from CLI. Current README also flags v2 runtime retirement—treat as a maintenance lead needing exact shipped-action/runner verification, **not permission for a blanket v3 upgrade**.
- CI credits, runners, advisory databases, rule refreshes and human maintenance remain costs even when no SaaS fee or model call is required.

---

# D. Additions and gaps in the dossier and 55-point log

The log is substantially more careful than the dossier. All55 considerations were reviewed as hypotheses, not adopted policy.

| Log items | Audit disposition / addition |
|---|---|
| **E01–E04** | Identity/date checks completed; author/denominator corrections above. R14 July31 is valid. Keep submission, manuscript date and conference/publication date separate. |
| **E05–E07** | Supported challenge. Add ETH **2602.11988**, first submission February12; inspected v3September29. Latest full text contradicts universal “does not change behavior” rhetoric and includes documentation-absence ablation. |
| **E08–E10** | Strengthen with R9 cross-skill denominator, R16 advisory-versus-normative mismatch, D12 desktop restriction, D13 API surface and exact Pi adapter evidence. Full original ADR vendor statistics remain unaudited. |
| **P01–P04** | Sensible proposals, not research results. Define complete acceptance behavior before optimizing patch size or approvals. Never require host execution of untrusted reproduction code. |
| **P05–P08** | Keep authority/collision/human-review seams. Add **policy/catalog/receipt/checker changes** to high-risk class. Reviewer independence includes independent oracle/state inspection, not just model difference. |
| **P09–P10** | Supported risk-sensitive direction. Logging/security requirements cannot be generated solely from file counts. “15lines native” is not a safe dependency criterion for cryptography, parsing or protocol logic. |
| **S01–S04** | Highest-priority accuracy corrections. Require canaries through real subprocess/build/extension paths, not merely model read tools. Include parent, children and alternate runners. |
| **S05–S07** | Add scanner rule/data feeds, transitive dependency resolution, config/schema downloads, caches and artifacts to trust inventory. Hosted PR event/checkout/token authority must be tested separately. |
| **S08–S10** | Retain applicability/severity review, licensing and evidence retention. Secrets valid/invalid checks may themselves create external calls. Public report paths can expose project identity/private layout. |
| **V01–V04** | Keep behavior-based testing; syntactic oracle lint only triage. Mutation testing is bounded fault sampling, not proof tests catch every bug. Coverage/length doctrine changes require operator choice. |
| **V05–V08** | Add explicit gate applicability and expected diagnostic assertions. Missing config must not produce misleading success. Evidence must bind policy/config/tools **and exact tested code**, including dirty files. Retry Unknown is not False. |
| **V09–V13** | Proportionate evaluation is preferable to fixed5runs or A/B-everything. Preserve failures and define intentional stochastic tests. Rollback must include data/side effects where applicable. |
| **U01–U04** | Tracking-first candidate sound. Add catalog/checker identity to receipt context; distinguish reviewed present baseline from historical adoption. Do not auto-enroll exact bytes as evidence of owner consent. |
| **U05–U08** | Add source-side symlink/path attacks, Git/config/filter execution risks, duplicate project-ID collisions and offline coverage expiry. Receipt ownership is not authenticated acceptance. |
| **U09–U12** | Retain immutable binding, scoped notices, zero-model detection and ClaudeBox/expert escalation. Notification suppression must not hide stale snapshot/failed observation. Separate locally current from upstream freshness unknown. |

### Foundational additions worth retaining

1. **ETH context-file study:** [2602.11988](https://arxiv.org/html/2602.11988v3), February12 first submission; September29 revision. Evidence favors nonredundant task-relevant guidance, not universal prohibition.
2. **Perry et al.:** [Do Users Write More Insecure Code with AI Assistants?](https://arxiv.org/html/2211.03622), first submitted November2022, later2023 publication.47participants, codex-davinci-002, mostly university population; task-dependent effects and false confidence. Foundational—not a current universal vulnerability estimate.
3. **GitHub security guidance:** [Secure use reference](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions). Immutable action identity, least privilege, protected workflow ownership, hostile PR checkout/artifacts and script injection.
4. **Copier’s actual lifecycle/security model:** rendered historical baselines, conflict review, optional unsafe tasks/migrations; see E.
5. **Pi’s explicit security boundary:** operator-user permissions and extension execution—not inferred containment from role names.

### Newly exposed local documentation gaps

Direct source inspection confirms:

- Adoption skill uses a ClaudeBox-specific absolute path and still says only TypeScript overlay is available.
- TS adoption merges scripts/snippets and customizes configs.
- Astro replaces TS compiler config; its README also still instructs obsolete `files.ignore`, not merely the hook comment noted earlier.
- Go adoption intentionally customizes TheWarRoom module-prefix architecture rules.
- `security.yml` uses mutable actions and `npm ci`; TS package snippet declares pnpm.
- Conditional template checks can succeed without executing substantive stack gates.

These support explicit distribution units and composition—not blind directory mirroring.

---

# E. Architecture options and implementation dependencies

These are **options for parent/operator review**, not selected architecture.

## Option 1 — Minimal deterministic tracker, manual updates

**Reasoned default for present consumers.**

Components:

1. Versioned canonical distribution catalog.
2. Consumer receipt with per-unit reviewed baseline and fingerprints.
3. Fixed, trusted read-only checker.
4. Generated observation/registry view.
5. Human-reviewed change notes and manual update proposals.

**Advantages:** addresses manual/customized consumers, partial adoption and unknown history without converting every repository into a generated template. Routine classification needs no model.

**Costs:** custom schema/security/tests/support; ownership decisions; maintaining mappings and migration notes. “Python standard library suffices” is plausible for a narrow implementation, not demonstrated code-size or portability proof.

**Important simplification:** begin with whole-file/exact-byte checks and conservative “review required” for merged snippets. Do not initially build semantic config comparison or arbitrary patch execution.

## Option 2 — Copier-rendered templates for eligible/new consumers

[Official updating documentation](https://copier.readthedocs.io/en/stable/updating/) verifies:

- Git-versioned templates and genuine answers support customized smart updates.
- Conflicts require manual review.
- Historical template regeneration is part of the algorithm.
- Answers must not be fabricated or edited to pretend a different generation produced the current project.
- `recopy` can overwrite local evolution.
- Updates can execute pre/post migrations and tasks.

[Configuration](https://copier.readthedocs.io/en/stable/configuring/) distinguishes unsafe Jinja extensions, tasks and migrations. `--skip-tasks` does **not** skip migrations.

**Advantages:** established render/update/conflict machinery; questions can encode stack choices; MIT tool license.

**Costs:** converting existing merge instructions to deterministic rendering, recovering genuine rendered baselines, dependency/runtime maintenance and template execution authority. Update cadence is commonly template-wide; independent per-unit accepted revisions still need a design.

**Appropriate when:** Christopher wants a true project-generation product, or new projects can adopt genuine Copier lineage.

**Not appropriate as shortcut:** write `.copier-answers.yml` with current upstream SHA in an old customized consumer and call its provenance known.

## Option 3 — Shared packages/submodules plus dependency automation

Useful for genuinely runtime-loadable common configs and tools.

- Shared package/submodule binds source, but does not integrate merged package scripts, local compiler paths or project architecture.
- [Renovate regex manager](https://docs.renovatebot.com/modules/manager/regex/) can discover/version pins; it does not apply customized template migrations or prove checks run.
- A bot bumping only receipt metadata creates false freshness.

**Default use:** later dependency/action maintenance alongside Option1, not replacement for adoption tracking.

## Keep four separate state domains

| Domain | Meaning | Not proof of |
|---|---|---|
| **Freshness** | Relevant distributed content matches selected approved snapshot | Latest remote content, secure code |
| **Provenance** | Source/destination identities and reviewed baseline recorded | Authentic approval, safe source |
| **Configuration** | Gate/runtime policy present and selected | Installed/loaded/required/executed |
| **Enforcement evidence** | Specific gate observed on exact code/environment/event | All vulnerabilities absent, future behavior |

A receipt editable by an agent cannot authenticate approval. Git review, protected ownership or an external trusted acceptance record must supply that authority if required. Signatures authenticate signer/bytes—not policy quality.

## Minimal classification contract

Compare accepted source fingerprint **A**, selected approved source fingerprint **B**, accepted destination fingerprint **D**, observed destination **C**:

- A=B, C=D: unchanged against selected snapshot.
- A=B, C≠D: local deviation; not automatically violation.
- A≠B, C=D, genuinely managed/source-identical baseline: replacement proposal candidate.
- A≠B with customization/local change: review required.
- Missing source/base/target, unsupported schema, rejected path or unavailable snapshot: explicit unknown/error.
- Deleted/renamed unit: report review; never silently delete.
- Revisions may differ per unit; never summarize partially migrated project as universally current.

Catalog changes themselves can change applicability. Compare catalog identity and mapping changes as well as file hashes.

## Proposed sequence

### Phase 0 — Authority and schema

Before coding:

- Christopher chooses local tracking versus fleet rollup, approved source policy and pilot.
- Define managed/customized/reference-only classes, effective destination ownership and stack composition.
- Define schema versions, unknown states, approval identity and protected policy seams.
- Obtain ClaudeBox context/expert review for durable fleet architecture.

### Phase 1 — Read-only fixtures and baseline

If approved, implement/test status only against synthetic temporary fixtures.

No consumer enrollment, installs, hooks, remote fetching or mutation by default. Use supplied roots and approved local source snapshots.

### Phase 2 — Owner-reviewed enrollment proposals

For real consumers:

- Record present exact matches/customizations without inventing historical versions.
- Enroll only with project owner consent.
- Customized present baseline acceptance is separate from claiming upstream policy implemented.
- No check evidence inherited from an old ref.

### Phase 3 — Safe planning, then bounded updates

Read-only plan first. Later apply, if separately authorized:

- Exact managed files only.
- Approved isolated disposable branch/workspace.
- Recheck expected source/destination hashes immediately before write.
- Refuse symlinks, traversal, conflicting owners, dirty/unrecorded state and unexpected changes.
- No arbitrary commands, hooks, installs, deletes, renames, activation or external writes.
- Advance acceptance only after review; failed checks remain visible.

### Phase 4 — Gate/containment and overlay modernization

One approved change at a time. Known Vitest security migration can proceed as separate bounded work rather than waiting for an entire rebuild.

Retain parent-verified **4.1.11** stable fix evidence; do not infer runtime compatibility from declared peers or upgrade all dependencies to latest.

### Phase 5 — Durable fleet rollup

Only after coordination and observed pilot results. Registry reports coverage, source snapshot age, last observation and per-ref divergence—not universal fleet compliance.

## Concrete acceptance fixtures

All below are **proposed; not run**.

### Tracking/composition

- History-only upstream commit: no content-update alert.
- Shared rule change: every applicable selected stack notified.
- Astro+TS: exactly one effective compiler-config owner; shared TS rules still tracked.
- Workers/Bun: no accidental pnpm guard.
- Local edit, upstream edit, both edits: distinct deterministic states.
- Customized `package.json`: unrelated keys preserved; automatic modification refused initially.
- Missing/deleted source and unknown historical baseline: unknown, not invented migration.
- Partial migration: per-unit revisions visible.
- Multiple worktrees/refs: grouped logical project, divergent observations retained.
- Duplicate project IDs across unrelated clones: explicit collision, not silent collapse.
- Offline approved snapshot: succeeds without network; upstream freshness beyond snapshot reported unknown.
- Receipt-only version bump: cannot claim changed rules applied or enforcement verified.

### Hostile input/checker

- `../`, absolute paths, symlink chains, hardlinks where relevant, case collisions and duplicate destinations rejected.
- Malformed/oversized receipts, unknown schemas and excessive entry counts bounded.
- Source catalog treated as data; embedded commands never executed.
- No model/network call in status.
- Source fingerprint changes between plan/apply: refusal.
- Concurrent destination change: refusal without loss.
- Untrusted Git diff/config/filter/transport settings cannot invoke external helpers through checker.
- Unknown/missing policy blocks mutation, not every harmless status observation.

### Enforcement/containment

- Clean control passes before planted violation.
- Failure diagnostic identifies expected rule—not missing executable/installation error.
- Missing gate config reports not applicable/unknown according to approved policy, never “verified.”
- Actual staged hooks and direct CLI both exercised.
- Policy/receipt/scanner allowlist tampering detected or independently reviewed.
- Read/write canaries outside approved roots denied through tools **and subprocesses**.
- Egress denial tested; permitted endpoint works.
- Parent, foreground/background children and external runners tested separately.
- Timeout, malformed hook output and missing handler exercised against exact installed version.
- Privileged PR fixture cannot run attacker-controlled code with elevated secrets/token.
- Mutating timeout after success: postcondition prevents duplicate; delayed visibility remains Unknown.
- Rollback restores approved files/receipt without touching pre-existing user data.

## Migration and rollback

- Tracking-only rollback: remove/revert approved metadata/checker integration; code unchanged.
- Managed update rollback: restore exact prior reviewed file set and corresponding receipt together.
- Customized migration: owner-reviewed explicit patch; preserve old baseline and exceptions.
- Exception: owner, rationale, scope, review trigger/expiry, compensating control.
- External/data changes require independent restoration/compensation—not just Git revert.
- No destructive cleanup of unknown files or worktrees as a rollback mechanism.

## No-go conditions

Do not authorize updater/rollout when:

- Ownership/composition/source authority unresolved.
- Receipt can silently expand tool authority or activate components.
- Historical baseline fabricated.
- No guard against symlink escape/concurrent change.
- Failure/unknown is reported as clean.
- Policy-changing PR can approve its own receipt/gates.
- Required tools/licenses unavailable with no approved fallback.
- Claimed containment is worktree-only or untested.
- Rollback depends on deleting unrecorded user files.
- Fleet registry scope/authority lacks required coordination.

## Low routine token burn without hidden costs

- Deterministic offline status; brief no-op output plus machine-readable details.
- Notify only changed applicable units; retain periodic coverage/snapshot-age warnings.
- Load index and relevant procedure lazily; do not always load this report/dossier.
- Preserve bounded harness/CI evidence rather than full repeated prose.
- Evaluate behavior-affecting skills/instructions/runtime changes; use lighter static/config checks for mechanical changes.
- Measure total inference, latency, human review and maintenance—not prompt length alone.

**No numeric token saving is established.**

---

# F. Decisions for Christopher and escalation

## Decisions Christopher must make

1. **Primary objective/tradeoffs:** correctness/security/recovery versus autonomy, attention, latency and cost.
2. **First deliverable:** local read-only tracker, fleet rollup, or full rendered-template lifecycle. Default proposal: local tracker.
3. **Approved pilot and consumer owners:** none selected by this audit.
4. **Source approval:** specific immutable snapshot/release; who accepts policy changes.
5. **Ownership/composition:** genuinely managed units versus customization/reference material.
6. **Authority:** separate local edit, branch/commit/push, PR, merge, deployment and irreversible/external-write permissions. Preserve existing email prohibition.
7. **Actual execution boundary:** whole-process container/VM/dedicated account and egress expectations; required evidence.
8. **Free-first interpretation:** no paid requirement versus no external service/license-key dependency; acceptable fallbacks.
9. **Evaluation proportionality:** which changes need paired runs, mutation/property tests, specialist review.
10. **Canonical conflicts:** Bun300-line law, Go project-specific architecture, architecture-context rationale, dependency heuristic and role mapping.
11. **Evidence handling:** retention/access/redaction and whether authentic approval needs an external protected record.
12. **Separate security work:** authority for Vitest/Workers compatibility validation without a blanket modernization sweep.

## ClaudeBox/expert escalation topics

- Fleet identity, registry locations/access, project ownership and durable distribution governance.
- Superseding ADRs and capability-based multi-agent roles.
- Exact active harness/sandbox/guard/child/external-runner boundaries.
- Updater threat model, policy tampering, CI privilege separation and source authenticity.
- Scanner/rule licensing and private-repository entitlement.
- Major dependency/security migration compatibility.
- Representative evaluation design and acceptable uncertainty.

## Remaining unknowns

- Active Pi core and effective loaded security policy.
- Parent/child process environment, mounts, credentials and network.
- Consumer baselines and gate applicability.
- Hosted required protections/bypasses.
- Full original ADR comparative statistics.
- R4/R10/R13 independent conference confirmation.
- R7 inconsistent compliance denominator.
- R16 exact historical specification snapshot and normative classification validity.
- All proposed compatibility, updater and containment fixture results.

---

# G. Compact parent synthesis

**The dossier is broadly right about direction, but not ready to become binding policy.**

1. Correct author attributions, conditional denominators and R7’s inconsistent compliance claim.
2. Keep negative-rule, skill-defect and Lucky-Pass findings scoped to their experiments.
3. Replace worktree-as-sandbox and blanket-hook language with runtime-specific, observed boundaries.
4. Preserve free-first, but distinguish engine, action wrapper, rules, plan and external-service conditions.
5. Prefer **approved schema/ownership → read-only tracker fixtures → owner-reviewed enrollment → safe plans**.
6. Treat receipts as provenance/freshness data, not approval or enforcement proof.
7. Modernize gates/overlays separately with real positive/negative fixtures.
8. No durable fleet choice, updater mutation or policy adoption is approved by this research.

**Report artifact:** `/home/chris/scratch/coding-standards-rebuild-research-pass.md`