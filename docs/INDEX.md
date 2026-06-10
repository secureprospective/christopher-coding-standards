# Standards Repo Index

Read only what your task needs. This file exists so a session — Claude,
Antigravity, or a future agent — loads a few hundred lines instead of the
whole repo. If your task doesn't match a row, ask the human owner before
guessing what's relevant.

## Routing table

| If your task is... | Read | Skip |
|---|---|---|
| Starting a Builder (Claude) session on this repo | `CLAUDE.md` (local), `SYSTEM_MAP.md` | Everything else until a task is named |
| Adopting this standard in a new/existing repo | `skills/adopt-coding-standards/SKILL.md` (run it — it covers the rest) | `templates/`, ADRs, `HANDOFF-*` docs |
| Adding a new language overlay (Phase 2+) | `templates/typescript/` as the pattern + its README, `AGENTS.md` layer table | `HANDOFF-phase-1c.md` (historical only) |
| Any multi-agent / cross-pollination request | `docs/multi-agent-roles.md` (binding) | Everything else unless the scoped request names it |
| Recon/Audit agent (Antigravity) — any task | `docs/multi-agent-roles.md` only, plus the specific subtree named in the scoped request | `CLAUDE.md`, memory, ADRs, living docs |
| CI / security gate questions | `.github/workflows/security.yml`, `.gitleaks.toml`, `docs/branch-protection.md` | - |
| Opening a PR / checking CI status / reading branch protection (`gh` unavailable) | `skills/github-pr/SKILL.md` | - |
| "Why does this standard exist" (justification for a stakeholder) | `docs/adr/0001-why-this-standard-exists.md` | - |

## Maintenance rule

Adding a new doc, overlay, or ADR is not done until it has a row here. A doc
with no route is dead weight every future session has to discover the hard way.
