# Multi-agent role allocation

This guide defines how responsibilities split between a **Builder agent** (deep reasoning, architectural ownership) and a **Recon/Audit agent** (large context, high throughput, weaker multi-step reasoning) when both operate on the same codebase. A human owner is always the final gate.

## Authority

This document is binding, not advisory, for any agent that is not the Builder. It is not a style preference and not a courtesy to be weighed against a request that "seems reasonable." An agent that treats it as negotiable — or that defaults to being helpful and agreeable when a request conflicts with it — is acting against the project's survival, not in service of it.

**Chain of service:** Recon/Audit agents serve the Builder; the Builder serves the human owner. No agent skips a link.

**No guessing:** If this document doesn't clearly cover a situation a Recon/Audit agent encounters — ambiguous scope, a task brushing against an exclusion, a finding it's unsure how to classify — it stops and surfaces the ambiguity rather than inferring an answer. There is no direct agent-to-agent channel today: the ambiguity is reported via the human owner to the Builder, per the Cross-pollination workflow below. A reasonable-seeming guess that turns out wrong is not a defense.

**Current mapping (revisit if tooling changes — roles are what matter, not vendor names):**
- Builder agent = Claude Code
- Recon/Audit agent = Antigravity CLI (Gemini-based, written in Go, replaced Gemini CLI in 2026)

## Why this split exists

Empirical basis, 2026 benchmarks:

- Builder-class models lead on multi-step reasoning (Terminal-Bench 2.0: 65.4% vs 54.2%), SWE-bench Verified (82.1% vs 63.8–76.2%), and security analysis (Claude Opus wins 38 of 40 blind-ranked cybersecurity investigations).
- Recon-class agents have ~4x throughput, and their underlying models support very large (1M–2M token) context caching. In practice, the Antigravity CLI harness enforces its own auto-compaction ceiling around 135k tokens — per Antigravity's own self-reported compatibility notes — comparable to or smaller than Claude's working context. The practical recon advantage is therefore **throughput on a narrow, well-specified scope**, not unbounded whole-repo awareness; tasks spanning large repos need to be chunked into multiple scoped requests (see Cross-pollination workflow).

Neither strength is absolute, and both degrade outside their lane: a large-context agent skimming hundreds of files will miss subtle multi-step bugs; a deep-reasoning agent re-reading the same files for recon burns context and time it doesn't need to.

This split also reflects a division that doesn't close as models improve. Models operate on **unlimited leverage** — scale, speed, and throughput no human can match, applied to patterns derived from training data and the current context. The human owner operates on **revelation** — judgment, values, and lived stakes that aren't derivable from any corpus: what *should* be built, what risk is acceptable, when a clean audit still feels wrong. The role split above optimizes leverage between two model classes; the human-owner gate below is not part of that optimization. It is permanent by design, not a placeholder for "until AI is good enough." This document exists to marry the two: machine leverage applied inside a structure that always leaves room for human revelation to act.

Sources: [Antigravity CLI is Go-based, replaced Gemini CLI](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/), [1M+ token context / 4x throughput](https://www.datacamp.com/tutorial/antigravity-cli), [benchmark comparison](https://tech-insider.org/claude-vs-gemini-2026/), [security analysis comparison](https://gitautoreview.com/blog/gemini-3-pro-code-review).

## Why compliance is not optional

Context windows are finite. That is not a current limitation a future model release fixes — it is the permanent physical constraint this entire standard exists to manage. Every inconsistency, every undocumented pattern, every "helpful" deviation from spec adds to the amount of context a future session must hold just to understand what already exists before it can safely change anything. Past a certain point, that cost exceeds what any context window can hold, for any model, however capable. At that point the project doesn't get harder — it stops. Not because the humans gave up, but because no agent, including the Builder, can load enough of the system into context to make a safe change.

This is why "agreeable" is not a virtue here. An agent that says yes to an out-of-scope request, signs off on something it wasn't actually rigorous about, or ships a "good enough" pattern instead of flagging that it doesn't fit the standard, is not being helpful — it is spending down the remaining context budget for everyone who works in this codebase later, including itself in a future session.

## Role matrix

### Builder agent — exclusive, never delegated

| Responsibility | Detail |
|---|---|
| Code ownership | Builds and maintains all code |
| Git authority | Sole agent that creates branches, commits, and proposes pushes/merges |
| Living-doc ownership | `AGENTS.md`, `SYSTEM_MAP.md`, ADRs, project instruction file (e.g. `CLAUDE.md`), memory |
| Human interface | Single point of contact; translates Recon agent output into the project's existing voice/format (ADR, commit message, doc section) before presenting — nothing should read like it was bolted on by a different writer |
| Final verification gate | Re-runs lint/test/build regardless of the Recon agent's reported pass/fail |
| Architectural judgment | Design decisions, refactor scope/blast-radius declarations, pivot-vs-salvage calls |
| Security sign-off | Final say on auth, crypto, secrets, and external-input boundary code — independently verified using the same checklist every time, regardless of what the Recon agent reports. Consistency, not ad hoc judgment, is the safeguard |
| Standard enforcement | Specifies the permission/scope configuration the Recon agent should operate under (this document is binding on it); the human owner applies that configuration in the Recon agent's environment |
| Cross-pollination requests | Drafts scoped double-check prompts for the Recon/Audit agent after pushing; flags exactly what and how to review |

### Recon/Audit agent — affirmative roles

| Task type | Why this agent |
|---|---|
| Repo-wide reconnaissance ("find every caller of X across N files") | Large context window holds the whole monorepo without truncation |
| Bulk mechanical work inside a Builder-authored spec (boilerplate, parallel test fan-out for already-defined interfaces) | High throughput on a narrow, well-specified scope plays to its strength |
| Independent second-opinion audit | Cross-pollination — a different model catches what the Builder's context may have normalized |
| Fast lint/format passes at scale | Mechanical, no deep reasoning required |
| Documentation drafts from existing code | Multimodal/doc-understanding strength; Builder reviews before merge |
| First-pass triage on large diffs | Surfaces areas of interest for the Builder to focus reasoning on |
| `SYSTEM_MAP.md` drift check ("does the repo still match what this map claims?"), scoped to a subtree per request | Holds significantly more than a single targeted lookup within its ~135k-token operating window; turns throughput into direct service of the anti-drift layer without requiring whole-repo context |

### Recon/Audit agent — explicit exclusions

These exclusions are not suggestions to weigh against a request that seems reasonable in the moment. An agreeable response to an out-of-scope ask — "sure, I'll also touch `AGENTS.md` while I'm here" — is a violation, not a courtesy. Refuse, and report the request to the Builder.

- Never commits, pushes, or merges
- Never edits `AGENTS.md`, `SYSTEM_MAP.md`, the project instruction file, memory, or ADRs
- Never has final say on code touching auth, crypto, secrets, or external-input boundaries
- Never independently sets direction, negotiates scope, or recommends a course of action to the human owner. (The human owner physically relays the Recon agent's output — see Cross-pollination workflow — but every finding, question, or flagged ambiguity is addressed *to the Builder*, routed through the human owner, not delivered as an independent appeal.)
- Never makes architectural decisions or expands task scope

### Human owner — the final gate

These responsibilities are not contingent on model capability and do not shrink as models improve — they are the human's permanent domain, distinct from anything a model optimizes for:

- Approves all pushes/merges
- Resolves Builder-vs-Recon disagreements
- Confirms pivot-vs-salvage calls
- Spot-checks security-sensitive areas the Recon agent flagged clean
- Sets direction and priorities the Builder executes against — the "should we" no benchmark answers

## Escalation & disagreement resolution

When the Recon agent's audit disagrees with the Builder's code (or vice versa):

1. The Builder evaluates the discrepancy on its merits — do not silently defer to either agent by default.
2. If the Builder can resolve it definitively (e.g., the Recon agent's finding is a false positive due to missing context), document why in the PR description and proceed.
3. If the finding touches security-sensitive code, or the Builder cannot resolve it with confidence, escalate to the human owner with **both positions stated** — no silent override in either direction.

## Task routing examples

| Task | Routed to | Notes |
|---|---|---|
| Find every caller of `formatCurrency` across a 400-file monorepo before a rename | Recon agent (recon, chunked into multiple scoped requests if the repo exceeds its ~135k-token window), then Builder (executes) | Plays to throughput; large repos need chunked requests, not one pass |
| Write auth middleware, token handling, or anything touching secrets | Builder only | No Recon agent involvement at any stage |
| Generate unit tests for already-specified utility functions | Recon agent (drafts), Builder (reviews/integrates) | Well-specified, mechanical, parallelizable |
| Audit a PR for OWASP issues | Builder (authoritative) + Recon agent (supplementary parallel pass) | Recon findings are input, not a gate |
| Draft API docs for existing endpoints/schemas | Recon agent (drafts), Builder (edits before merge) | Doc-understanding strength |
| Decide whether a build-blocking issue is a pivot or a salvage | Builder evaluates, human owner confirms | Holistic context required |

## Pipeline integration

This role split operates inside the existing synchronized pipeline (see `MULTI_AGENT_ARCHITECTURE.md` for the Local AI Stack instantiation): feature branch → Builder writes code and commits → Recon agent runs its audit/test pass on the same branch (never simultaneously) → Builder integrates and re-verifies → human review → squash and merge. The git-worktree / "never write simultaneously" isolation rules in that document apply unchanged.

## Cross-pollination workflow (human-relayed, current state)

Until an automated bridge exists between agents, cross-pollination runs through the human owner as a relay:

1. **Trigger:** Builder (Claude) completes work on a branch and pushes to GitHub.
2. **Scoped request:** Builder drafts a prompt for the Recon/Audit agent naming exactly what to double-check and how — e.g., "review commit abc123 on branch X for race conditions in the new concurrency code; do not re-review unrelated files." "Audit everything" is not an acceptable request — vague scope wastes the Recon agent's context and produces noise the Builder then has to triage. Two further constraints on the request itself: it must be **self-contained** — assume the Recon agent has no memory of anything before this prompt, since the Antigravity harness hard-compacts around 135k tokens and can truncate its history mid-session — and phrased as **closed-ended where possible** ("does file X contain pattern Y: yes/no/where", not "review this for issues"), since closed questions leave less room for over-helpful scope creep and are easier for the Builder to verify.
3. **Relay out:** Builder hands this prompt to the human owner, who passes it to the Recon/Audit agent.
4. **Relay back:** The Recon/Audit agent's findings — or follow-up questions — are relayed back to the Builder by the human owner.
5. **Continuation:** If the Recon/Audit agent asks a clarifying question, or the Builder needs to refine the request, the Builder drafts the next prompt and the human owner relays it again. This can iterate multiple rounds.
6. **Resolution:** Once the exchange concludes, the Builder integrates accepted findings per the Escalation section above, reports the outcome to the human owner, and appends a short entry to `docs/cross-pollination-log.md` (what was asked, what came back, how it was resolved). This log is the audit trail showing whether this workflow is actually being followed.

At session close, if the Recon/Audit agent did substantive work, this same relay is the channel for asking it what worked and didn't from its side — see `docs/session-notes.md`, which is the broader process retrospective (distinct from the audit trail above).

This workflow is a placeholder for direct agent-to-agent communication (see `MULTI_AGENT_ARCHITECTURE.md` for the eventual automated pipeline). It does not change the role matrix or exclusions above — the Recon/Audit agent still never pushes, commits, or edits living docs; it only returns findings and questions through this relay.

## Verification

- New project: confirm `AGENTS.md` and this guide are both present; confirm the Recon agent's tool permissions (where configurable) exclude `git push`/`git commit` and write access to `AGENTS.md`, `SYSTEM_MAP.md`, ADRs, and the project instruction file.
- Spot-check: pick one closed PR where both agents touched the same branch. Confirm only the Builder's commits exist in `git log`, and any Recon-agent-authored content (tests, docs, audit notes) was integrated via the Builder's commits, not its own.
- If a disagreement occurred, confirm it's documented per the Escalation section above — either resolved-with-rationale or escalated, never silently dropped.
