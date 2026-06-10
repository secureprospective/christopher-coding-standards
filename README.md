# christopher-coding-standards

Canonical engineering standards for AI-assisted code generation across multiple models (Claude Code, frontier models, local LLMs).

## Why this exists

Empirical baseline, sourced research, 2025–2026:

- **Veracode 2025 GenAI Code Security Report** (100+ LLMs across Java, JavaScript, Python, C#): AI-generated code contains **2.74x more vulnerabilities** than human-written code. 45% of samples carry OWASP Top 10 issues.
- **AppSec Santa, 2026**: **1 in 4** AI-generated code samples contain a confirmed OWASP vulnerability.
- **Apiiro, Fortune 50 analysis**: CVSS 7.0+ vulnerabilities appear **2.5x more often** in AI-generated code.
- **GitHub-scale CWE study**: top dangerous CWEs in AI-generated code are SQL Injection (CWE-89), OS Command Injection (CWE-78), Code Injection (CWE-94), hard-coded credentials (CWE-259/798).

This standard assumes every AI output is unverified third-party code until it passes the layered gates below. No model — frontier or local — is trusted to self-police.

## Design principles

1. **Model-agnostic.** Same gates apply whether code comes from Claude Code, frontier models, or local LLMs.
2. **Deterministic where possible.** Hooks and CI gates over prose instructions.
3. **Free-tooling-first.** Works without paid SaaS.
4. **Canonical.** This repo is the single source of truth. Other repos copy from here.
5. **Replicable.** TFM Vanguards can adopt the same standard with the same tooling on their own hardware.

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

1. Copy `AGENTS.md` to repo root. Customize the per-project section (project name, languages, public exposure, stack-specific commands).
2. Copy `.claude/settings.json` to repo `.claude/` directory.
3. Copy `SYSTEM_MAP.md` template to repo root and fill in directory invariants and existing utilities.
4. Copy `.gitleaks.toml` to repo root.
5. Copy `.github/workflows/security.yml` to repo `.github/workflows/`.
6. Enable branch protection per `docs/branch-protection.md`.
7. For TypeScript projects: copy the TypeScript overlay from `/templates/typescript/`. See `templates/typescript/README.md` for the adoption walkthrough.

## Multi-agent role allocation

When more than one AI agent works the same codebase — e.g., a deep-reasoning "Builder" agent (Claude Code) alongside a large-context "Recon/Audit" agent (Antigravity CLI) — see `docs/multi-agent-roles.md` for the role split, escalation procedure, and task-routing guidance. The Builder agent retains exclusive git authority and living-document ownership; a human owner remains the final gate on all pushes and merges.

## Phase status

- ✅ Phase 1A — repo skeleton
- ✅ Phase 1B — language-agnostic templates
- ✅ Phase 1C — TypeScript overlay (`/templates/typescript/`)
- ⏳ Phase 1D — Astro overlay (split from 1C — `.astro` files require separate Biome + Prettier config)
- ⏳ Phase 2 — Python, Go, Bash overlays
- ⏳ Phase 3 — local-model selection guidance, dual-model architecture doc

## License

UNLICENSED (placeholder — choose MIT or Apache-2.0 before public release).

## Sources

The empirical claims in this README and in `docs/adr/0001-why-this-standard-exists.md` are sourced. See that ADR for full citations.
