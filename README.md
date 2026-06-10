<div align="center">

# christopher-coding-standards

### Stop the slop.

**Canonical, model-agnostic engineering standards that make AI-generated code
something a human — or a different LLM, in a different session — can pick up
cold and trust.**

[![Security](https://github.com/secureprospective/christopher-coding-standards/actions/workflows/security.yml/badge.svg)](https://github.com/secureprospective/christopher-coding-standards/actions/workflows/security.yml)
![Phase](https://img.shields.io/badge/phase-1D%20complete%20%7C%20Phase%202%20next-blue)
![Model Agnostic](https://img.shields.io/badge/models-Claude%20%7C%20Gemini%20%7C%20local-9cf)
![Zero Trust](https://img.shields.io/badge/AI%20output-zero%20trust-critical)
![License](https://img.shields.io/badge/license-MPL--2.0-blue)

**Starting a session here? → Read [`docs/INDEX.md`](docs/INDEX.md) first.**
It routes you to only the files your task needs, instead of this whole repo.

</div>

---

## Contents

- [The problem](#the-problem)
- [How it fits together](#how-it-fits-together)
- [What's actually in here](#whats-actually-in-here)
- [Design principles](#design-principles)
- [The eleven-layer guardrail stack](#the-eleven-layer-guardrail-stack)
- [How to adopt in a new or existing repo](#how-to-adopt-in-a-new-or-existing-repo)
- [Multi-agent role allocation](#multi-agent-role-allocation)
- [Phase status](#phase-status)

---

## The problem

LLMs write fine code *inside* a single context window. They fall apart
*across* sessions and *across* agents — a new session, or a different model
picking up another's work, with nothing forcing it to stay coherent. The
result is **AI slop**: inconsistent patterns, duplicated logic, code that only
made sense to the model that wrote it, in the hour it wrote it.

Every AI output here is treated as **unverified third-party code** until it
passes the layered gates below. No model — frontier or local, Claude or
Gemini — is trusted to self-police.

> Models bring **unlimited leverage** — scale, speed, throughput no human can
> match. Humans bring **revelation** — judgment, values, and the "should we"
> that no benchmark answers. This repo exists to marry the two: machine
> leverage applied inside a structure that always leaves room for human
> revelation to act.

### The numbers

- **Veracode 2025 GenAI Code Security Report** (100+ LLMs across Java,
  JavaScript, Python, C#): AI-generated code contains **2.74x more
  vulnerabilities** than human-written code. 45% of samples carry an OWASP Top
  10 issue.
- **AppSec Santa, 2026**: **1 in 4** AI-generated code samples contain a
  confirmed OWASP vulnerability.
- **Apiiro, Fortune 50 analysis**: CVSS 7.0+ vulnerabilities appear **2.5x more
  often** in AI-generated code.
- **GitHub-scale CWE study**: the top dangerous CWEs in AI-generated code are
  SQL Injection (CWE-89), OS Command Injection (CWE-78), Code Injection
  (CWE-94), and hard-coded credentials (CWE-259/798).

Full citations: `docs/adr/0001-why-this-standard-exists.md`.

## How it fits together

```
                       ┌─────────────────────────┐
                       │   docs/INDEX.md          │   ← every session starts here
                       │   "what do I need?"      │
                       └────────────┬─────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                             ▼                             ▼
┌───────────────┐           ┌─────────────────┐          ┌──────────────────┐
│  BUILDER agent │           │ RECON/AUDIT agent│          │   HUMAN OWNER     │
│  (Claude Code) │◄─────────►│ (Antigravity CLI)│          │  (the soul)       │
│                │  cross-    │                  │          │                  │
│ • writes code  │ pollinate  │ • repo recon     │          │ • approves merges│
│ • sole git     │  (relayed) │ • audits, drafts │          │ • resolves        │
│   authority    │           │ • never commits  │          │   disagreements   │
│ • living docs  │           │ • never edits    │          │ • sets direction  │
└───────┬────────┘           │   living docs    │          └──────────────────┘
        │                     └──────────────────┘
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Eleven-layer guardrail stack (advisory → deterministic CI)   │
│  AGENTS.md → permissions → SYSTEM_MAP.md → schemas → lint →   │
│  pre-commit → SAST/SCA/secrets → tests → sandboxing → ADRs →  │
│  local-model gates                                            │
└─────────────────────────────────────────────────────────────┘
```

Full role split, escalation, and task routing: `docs/multi-agent-roles.md`.

## What's actually in here

| | |
|---|---|
| **Eleven-layer guardrail stack** | From advisory `AGENTS.md` instructions down to CI-enforced SAST/SCA/secrets scanning — table below |
| **Multi-agent governance** | A binding role split between a Builder agent (deep reasoning, sole git authority) and Recon/Audit agents (large context, throughput) — `docs/multi-agent-roles.md` |
| **Cross-pollination workflow** | Structured, logged second-opinion audits between agents — `docs/cross-pollination-log.md` |
| **Task-routing index** | `docs/INDEX.md` — load only what your task needs, not the whole repo |
| **Skills** | `adopt-coding-standards` (one command to onboard a new repo), `github-pr` (read-side GitHub API helper for environments without `gh`) |
| **Language overlays** | `templates/typescript/` (Phase 1C: Biome, Zod, Stryker, Vitest), `templates/astro/` (Phase 1D: Prettier + `prettier-plugin-astro`, `astro check`) |

## Design principles

1. **Model-agnostic.** Same gates apply whether code comes from Claude Code, frontier models, or local LLMs.
2. **Deterministic where possible.** Hooks and CI gates over prose instructions.
3. **Free-tooling-first.** Works without paid SaaS.
4. **Canonical.** This repo is the single source of truth. Other repos copy from here.
5. **Replicable.** Same standard, same tooling, on any hardware.

## The eleven-layer guardrail stack

| Layer | Mechanism | Artifact in this repo |
|---|---|---|
| 1 | Agent instruction (advisory) | `AGENTS.md` |
| 2 | Claude Code permissions | `.claude/settings.json` |
| 3 | System map (anti-drift) | `SYSTEM_MAP.md` (template) |
| 4 | Schema-driven boundaries | Phase 1C+ (language overlays) |
| 5 | Formatter + linter | Phase 1C+ (language overlays) |
| 6 | Pre-commit hooks | Phase 1C+ (language overlays) |
| 7 | Security scanning (SAST + SCA + secrets) | `.gitleaks.toml`, `.github/workflows/security.yml` |
| 8 | Test discipline | branch protection + language overlays |
| 9 | Execution sandboxing | OS-level (operator concern, documented separately) |
| 10 | Refactoring discipline | `AGENTS.md` + ADR pattern |
| 11 | Local model selection | Phase 2 (quantization floor, dual-model architecture) |

## How to adopt in a new or existing repo

Run the `adopt-coding-standards` skill (`skills/adopt-coding-standards/SKILL.md`)
from a Claude Code session in the target repo — it walks through all of the
following:

1. Copy `AGENTS.md` to repo root. Customize the per-project section (project name, languages, public exposure, stack-specific commands).
2. Copy `.claude/settings.json` to repo `.claude/` directory.
3. Copy `SYSTEM_MAP.md` template to repo root and fill in directory invariants and existing utilities.
4. Copy `.gitleaks.toml` to repo root.
5. Copy `.github/workflows/security.yml` to repo `.github/workflows/`.
6. Enable branch protection per `docs/branch-protection.md`.
7. For TypeScript projects: copy the TypeScript overlay from `/templates/typescript/`. See `templates/typescript/README.md` for the adoption walkthrough.
8. If more than one AI agent works this codebase, copy `docs/multi-agent-roles.md` and `docs/cross-pollination-log.md` (reset to just its format section).

## Multi-agent role allocation

When more than one AI agent works the same codebase — e.g., a deep-reasoning
"Builder" agent (Claude Code) alongside a large-context "Recon/Audit" agent
(Antigravity CLI) — see `docs/multi-agent-roles.md` for the role split,
authority chain, escalation procedure, and task-routing guidance. The Builder
agent retains exclusive git authority and living-document ownership; a human
owner remains the final gate on all pushes and merges. This document is
**binding, not advisory** — see its "Why compliance is not optional" section
for why.

## Phase status

- ✅ Phase 1A — repo skeleton
- ✅ Phase 1B — language-agnostic templates
- ✅ Phase 1C — TypeScript overlay (`/templates/typescript/`)
- ✅ Multi-agent governance — role allocation, cross-pollination workflow, task-routing index
- ✅ Phase 1D — Astro overlay (`/templates/astro/`, split from 1C — `.astro` files require separate Prettier config + `astro check`)
- ⏳ Cross-pollination pilot — one real scoped Antigravity audit round on the 1D overlay, logged in `docs/cross-pollination-log.md`
- ⏳ Phase 2 — Python, Go, Bash overlays
- ⏳ Phase 3 — local-model selection guidance, dual-model architecture doc

## License

[MPL-2.0](LICENSE) — Mozilla Public License 2.0. Permissive enough to drop
these templates into any project (including proprietary ones), with a
file-level copyleft: if you modify one of these files and redistribute it,
those changes stay open under MPL-2.0 too. The goal is for improvements to
flow back into the standard, not to restrict who can use it.

## Sources

The empirical claims in this README and in `docs/adr/0001-why-this-standard-exists.md` are sourced. See that ADR for full citations.
