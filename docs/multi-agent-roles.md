# Multi-agent role allocation

This guide defines how responsibilities split between a **Builder agent** (deep reasoning, architectural ownership) and a **Recon/Audit agent** (large context, high throughput, weaker multi-step reasoning) when both operate on the same codebase. A human owner is always the final gate.

**Current mapping (revisit if tooling changes — roles are what matter, not vendor names):**
- Builder agent = Claude Code
- Recon/Audit agent = Antigravity CLI (Gemini-based, written in Go, replaced Gemini CLI in 2026)

## Why this split exists

Empirical basis, 2026 benchmarks:

- Builder-class models lead on multi-step reasoning (Terminal-Bench 2.0: 65.4% vs 54.2%), SWE-bench Verified (82.1% vs 63.8–76.2%), and security analysis (Claude Opus wins 38 of 40 blind-ranked cybersecurity investigations).
- Recon-class agents lead on raw context window (1M–2M tokens vs Claude's smaller window) and throughput (~4x), making them effective at whole-monorepo reconnaissance without hallucinating file paths.

Neither strength is absolute, and both degrade outside their lane: a large-context agent skimming hundreds of files will miss subtle multi-step bugs; a deep-reasoning agent re-reading the same files for recon burns context and time it doesn't need to.

Sources: [Antigravity CLI is Go-based, replaced Gemini CLI](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/), [1M+ token context / 4x throughput](https://www.datacamp.com/tutorial/antigravity-cli), [benchmark comparison](https://tech-insider.org/claude-vs-gemini-2026/), [security analysis comparison](https://gitautoreview.com/blog/gemini-3-pro-code-review).

## Role matrix

### Builder agent — exclusive, never delegated

| Responsibility | Detail |
|---|---|
| Code ownership | Builds and maintains all code |
| Git authority | Sole agent that creates branches, commits, and proposes pushes/merges |
| Living-doc ownership | `AGENTS.md`, `SYSTEM_MAP.md`, ADRs, project instruction file (e.g. `CLAUDE.md`), memory |
| Human interface | Single point of contact; synthesizes Recon agent output before presenting |
| Final verification gate | Re-runs lint/test/build regardless of the Recon agent's reported pass/fail |
| Architectural judgment | Design decisions, refactor scope/blast-radius declarations, pivot-vs-salvage calls |
| Security sign-off | Final say on auth, crypto, secrets, and external-input boundary code — independently verified even if the Recon agent reports clean |

### Recon/Audit agent — affirmative roles

| Task type | Why this agent |
|---|---|
| Repo-wide reconnaissance ("find every caller of X across N files") | Large context window holds the whole monorepo without truncation |
| Bulk mechanical work inside a Builder-authored spec (boilerplate, parallel test fan-out for already-defined interfaces) | High throughput on a narrow, well-specified scope plays to its strength |
| Independent second-opinion audit | Cross-pollination — a different model catches what the Builder's context may have normalized |
| Fast lint/format passes at scale | Mechanical, no deep reasoning required |
| Documentation drafts from existing code | Multimodal/doc-understanding strength; Builder reviews before merge |
| First-pass triage on large diffs | Surfaces areas of interest for the Builder to focus reasoning on |

### Recon/Audit agent — explicit exclusions

- Never commits, pushes, or merges
- Never edits `AGENTS.md`, `SYSTEM_MAP.md`, the project instruction file, memory, or ADRs
- Never has final say on code touching auth, crypto, secrets, or external-input boundaries
- Never communicates directly with the human owner
- Never makes architectural decisions or expands task scope

### Human owner — the final gate

- Approves all pushes/merges
- Resolves Builder-vs-Recon disagreements
- Confirms pivot-vs-salvage calls
- Spot-checks security-sensitive areas the Recon agent flagged clean

## Escalation & disagreement resolution

When the Recon agent's audit disagrees with the Builder's code (or vice versa):

1. The Builder evaluates the discrepancy on its merits — do not silently defer to either agent by default.
2. If the Builder can resolve it definitively (e.g., the Recon agent's finding is a false positive due to missing context), document why in the PR description and proceed.
3. If the finding touches security-sensitive code, or the Builder cannot resolve it with confidence, escalate to the human owner with **both positions stated** — no silent override in either direction.

## Task routing examples

| Task | Routed to | Notes |
|---|---|---|
| Find every caller of `formatCurrency` across a 400-file monorepo before a rename | Recon agent (recon), then Builder (executes) | Plays to context-window strength |
| Write auth middleware, token handling, or anything touching secrets | Builder only | No Recon agent involvement at any stage |
| Generate unit tests for already-specified utility functions | Recon agent (drafts), Builder (reviews/integrates) | Well-specified, mechanical, parallelizable |
| Audit a PR for OWASP issues | Builder (authoritative) + Recon agent (supplementary parallel pass) | Recon findings are input, not a gate |
| Draft API docs for existing endpoints/schemas | Recon agent (drafts), Builder (edits before merge) | Doc-understanding strength |
| Decide whether a build-blocking issue is a pivot or a salvage | Builder evaluates, human owner confirms | Holistic context required |

## Pipeline integration

This role split operates inside the existing synchronized pipeline (see `MULTI_AGENT_ARCHITECTURE.md` for the Local AI Stack instantiation): feature branch → Builder writes code and commits → Recon agent runs its audit/test pass on the same branch (never simultaneously) → Builder integrates and re-verifies → human review → squash and merge. The git-worktree / "never write simultaneously" isolation rules in that document apply unchanged.

## Verification

- New project: confirm `AGENTS.md` and this guide are both present; confirm the Recon agent's tool permissions (where configurable) exclude `git push`/`git commit` and write access to `AGENTS.md`, `SYSTEM_MAP.md`, ADRs, and the project instruction file.
- Spot-check: pick one closed PR where both agents touched the same branch. Confirm only the Builder's commits exist in `git log`, and any Recon-agent-authored content (tests, docs, audit notes) was integrated via the Builder's commits, not its own.
- If a disagreement occurred, confirm it's documented per the Escalation section above — either resolved-with-rationale or escalated, never silently dropped.
