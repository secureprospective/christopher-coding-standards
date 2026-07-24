# Standards Repo Index

Read only what your task needs. This file exists so a session — Claude,
Antigravity, or a future agent — loads a few hundred lines instead of the
whole repo. If your task doesn't match a row, ask the human owner before
guessing what's relevant.

## Routing table

| If your task is... | Read | Skip |
|---|---|---|
| **Writing or reviewing actual code** (any Builder *or* Recon build/review session) | `docs/agent-codex.md` — the build doctrine: 18 indexable motifs, slop catalog, security baseline, the canon mapped to each motif | Everything else until a task is named |
| **Writing code on a small local model** (Ornith/Gemma/qwen; Hermes' local fallback) whose context can't hold the full Codex | `docs/agent-codex-lite.md` — the 18 motif laws + slop headlines, compressed not cut | The full `agent-codex.md` unless the task sets a template others clone |
| **Selecting/assigning a role to a local model, or re-checking one after a hardware/model change** (Layer 11) | `docs/local-model-guidance.md` — selection checklist, dual-model pattern, dated fleet snapshot | Don't carry forward old floor/context numbers without re-running the checklist |
| Starting a Builder (Claude) session on this repo | `CLAUDE.md` (local), `SYSTEM_MAP.md` | Everything else until a task is named |
| Adopting this standard in a new/existing repo | `skills/adopt-coding-standards/SKILL.md` (run it — it covers the rest) | `templates/`, ADRs, `HANDOFF-*` docs |
| Adding a new language overlay (Phase 2+) | `templates/typescript/` as the pattern + its README, `AGENTS.md` layer table | `HANDOFF-phase-1c.md` (historical only) |
| Adopting Astro support in a project already on the TypeScript overlay | `templates/astro/README.md` | `templates/typescript/README.md` (already done) |
| Adopting Cloudflare Workers support in a project already on the TypeScript overlay | `templates/cloudflare-workers/README.md` | `templates/typescript/README.md` (already done) |
| Any multi-agent / cross-pollination request | `docs/multi-agent-roles.md` (binding) | Everything else unless the scoped request names it |
| Large-context whole-repo audit / de-slop / front-end QA (GLM auditor) | `docs/glm-auditor-discipline.md` (Layer 10.5) + `docs/multi-agent-roles.md` (binding) | Everything else unless the scoped request names it |
| Recon/Audit agent (Antigravity) — any task | `docs/multi-agent-roles.md` only, plus the specific subtree named in the scoped request | `CLAUDE.md`, memory, ADRs, living docs |
| CI / security gate questions | `.github/workflows/security.yml`, `.gitleaks.toml`, `docs/branch-protection.md` | - |
| Opening a PR / checking CI status / reading branch protection (`gh` unavailable) | `skills/github-pr/SKILL.md` | - |
| "Why does this standard exist" (justification for a stakeholder) | `docs/adr/0001-why-this-standard-exists.md` | - |
| Closing a session in this repo | (write step, not read) append an entry to `docs/session-notes.md` | - |
| Periodic standards review ("what should change based on past sessions?") | `docs/session-notes.md` | Everything else unless reviewing |

## Maintenance rule

Adding a new doc, overlay, or ADR is not done until it has a row here. A doc
with no route is dead weight every future session has to discover the hard way.
