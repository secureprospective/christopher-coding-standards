# AGENTS.md

This file is read by AI coding agents (Claude Code, frontier models, local LLMs) at the start of every session. It is **advisory**. Pre-commit hooks and CI checks are the **enforcement** layer. If guidance here conflicts with what a hook enforces, the hook wins — fix the violation, do not bypass.

## Project profile

- **Project name:** PROJECT_NAME
- **Primary language(s):** PRIMARY_LANGUAGES
- **Public exposure:** PUBLIC_OR_INTERNAL
- **Standards version:** christopher-coding-standards v0.1

> Replace the placeholders above before committing this file.

## Conditional: Spec Kit

If the current task is a **new feature**, a **new module**, or a **new project** (not a small bug fix, not a config tweak, not a documentation change), ask the user whether to initialize GitHub Spec Kit (https://github.com/github/spec-kit) for this work before writing any code.

Default behavior if the user declines or does not respond: proceed without Spec Kit.

## Code footprint

- Target file size: under 250 lines. Hard cap: 400 lines. Refactor over.
- No copy-paste. Check `SYSTEM_MAP.md` for existing utilities before writing helpers.
- Add a third-party dependency only when the alternative is more than ~15 lines of equivalent native code.
- No commented-out code blocks. Delete or use `git` history.

## Security mandates

- All external input (HTTP body, query params, file ingest, IPC, CLI args) validated through an **explicit schema**. No ad-hoc parsing or type-casting.
- No hardcoded secrets, tokens, credentials, IPs, or hostnames. Use environment variables or a secrets manager.
- Parameterized queries only for any database call. No string concatenation into SQL.
- All HTML rendering: framework-escaped or explicitly sanitized.
- All file paths from external input: validated against a directory allowlist. No path traversal.
- All shell calls: argument arrays, never shell strings. Never interpolate external input into a shell command.
- Errors: never leak internal stack traces, paths, or credentials to external responses.

## Refactoring protocol

When modifying any existing module:

1. **Declare scope first.** State what will change, what will not, and what the blast radius is. Wait for human acknowledgement before editing.
2. **Work on a branch.** Never commit experimental refactors directly to `main` or `develop`.
3. **Verify behavior preservation.** Tests pass on both old and new before merge. For pure functions, snapshot input/output.

Do not rewrite working code unprompted. If you see a refactor opportunity, **propose** it; do not execute it.

## Workflow

- Tests required for every functional change.
- Run before committing:
  - `make lint` (or stack-specific command below)
  - `make test`
- If a pre-commit hook fails, read the error and fix the violation. Do **not** bypass with `--no-verify`.

## Stack-specific commands

Fill in for this project. Examples shown:

- **Lint:** `LINT_COMMAND` (e.g. `pnpm biome ci`, `ruff check`, `golangci-lint run`)
- **Format:** `FORMAT_COMMAND` (e.g. `pnpm biome format --write`, `ruff format`)
- **Test:** `TEST_COMMAND` (e.g. `pnpm test`, `pytest`, `go test ./...`)
- **Type check:** `TYPE_COMMAND` (e.g. `pnpm tsc --noEmit`)

## Commit and PR conventions

- Conventional commit prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `build:`, `ci:`.
- Append `[AI-assisted]` to commit messages when an AI agent generated or substantially modified the diff. This is for audit traceability, not credit assignment.
- PR descriptions for AI-assisted work should note which modules were AI-generated and how they were verified.

## What not to do

- Do not edit files in `.git/`, `node_modules/`, `dist/`, `build/`, `.next/`, or vendored directories.
- Do not write to `.env`, `.env.*`, or any file under `secrets/`.
- Do not generate an "architecture overview" section in this file. Empirical research (ETH Zurich, 2026) shows it inflates token cost without changing agent behavior. Keep this file minimal.
- Do not run `/init` and accept the output as final. LLM-generated context files have been shown to degrade agent performance when used unedited.
- Do not propose changes that violate an Architectural Decision Record. ADRs live in `docs/adr/`.
- Do not introduce new top-level directories without updating `SYSTEM_MAP.md`.
- Do not pin third-party CI actions to mutable version tags (`@v1`, `@master`). Pin to commit SHAs. (Reason: `aquasecurity/trivy-action` supply-chain compromise of March 19, 2026 — 75 of 76 version tags were force-pushed with malicious payload.)

## Where to look

- `SYSTEM_MAP.md` — what exists in this project. Check before writing.
- `docs/adr/` — architectural decisions. Read before proposing changes that touch them.
- `README.md` — for human contributors. Project setup and usage.
- `.github/workflows/` — the CI gates that will run on your PR.
