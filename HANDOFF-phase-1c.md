# Handoff prompt — Phase 1C: TypeScript overlay

## Status

- ✅ **Phase 1A** — repo skeleton complete
- ✅ **Phase 1B** — language-agnostic templates complete
- ⏳ **Phase 1C** — TypeScript overlay (next session — this document)

The repo currently contains:

```
christopher-coding-standards/
├── README.md
├── AGENTS.md
├── SYSTEM_MAP.md
├── .gitleaks.toml
├── .claude/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── security.yml
├── docs/
│   ├── adr/
│   │   └── 0001-why-this-standard-exists.md
│   └── branch-protection.md
├── templates/
│   └── ADR-template.md
└── HANDOFF-phase-1c.md   ← this file
```

## What Phase 1C builds

A `/templates/typescript/` directory containing the language-specific overlay for TS / React / Node projects.

Files to produce:

1. **`biome.json`** — Biome configuration. Linter rules, formatter settings, recommended ruleset. Decide strictness level (recommended vs recommended + opinionated additions).
2. **`.pre-commit-config.yaml`** — pre-commit framework config that runs Biome on staged files, plus Gitleaks at the local hook layer.
3. **`tsconfig.json`** — TypeScript compiler config with strict-mode invariants. Decide full `"strict": true` vs selective flags.
4. **`schemas/example.ts`** — Zod schema example demonstrating the boundary validation pattern referenced in `AGENTS.md`. Include `.strict()` and `z.infer<>` pattern.
5. **`stryker.conf.mjs`** — Stryker mutation testing config. Scope: full project on weekly cron, changed-files only for PRs.
6. **`package.json` snippet** — devDependencies (`@biomejs/biome`, `zod`, `@stryker-mutator/core`, etc.) and scripts (`lint`, `format`, `test`, `mutation-test`).
7. **`/templates/typescript/README.md`** — adoption instructions specific to the TS overlay.

## Decisions locked from previous sessions

- TypeScript first (not Python, not Go)
- Biome (not ESLint + Prettier)
- Astro projects use **overlay C**: Biome for everything except `.astro` files; Prettier with `prettier-plugin-astro` for `.astro` template formatting. **The Astro overlay is separate and not part of Phase 1C.** Phase 1C delivers the base TS overlay only.
- Free tools only
- Spec Kit conditional already encoded in `AGENTS.md`
- Schema library: Zod
- Mutation testing: Stryker, weekly schedule not per-PR
- Pre-commit hooks pinned by SHA where security-sensitive

## Open questions to resolve in Phase 1C

- **Biome strictness level:** `recommended` set only, or `recommended` + selected opinionated rules (e.g., `noExplicitAny`, `noNonNullAssertion`)?
- **TypeScript strict mode:** full `"strict": true` (recommended), or selective flags?
- **Stryker scope:** full project run, or critical paths only? Default mutation timeout settings?
- **Whether to ship a `Makefile` template** alongside the TS overlay, or leave that as per-project.
- **Module system default:** ESM-only, or also support CommonJS for older Node libs?

## Foreseeable problems to address

- Biome 2.3+ has experimental `.astro` support; overlay C avoids dependence on it. Confirm Biome version pin in `biome.json` and in `package.json`.
- `prettier-plugin-astro` is officially supported by Astro and is the safe fallback for `.astro` template formatting — for the **future** Astro overlay, not this one.
- Stryker can be slow on large codebases. Default config should scope to changed files for PR runs and run full on the weekly cron.
- Biome and `pre-commit` framework integration: the `biomejs/pre-commit` repo exists. Confirm its current state and pin to SHA.

## Suggested opening prompt for next session

> Continuing Phase 1C of the christopher-coding-standards build. Phase 1A and 1B are complete in the repo (see structure in HANDOFF-phase-1c.md). The locked stack: TypeScript first, Biome, Zod, Stryker, free tools only. Today builds the TypeScript overlay in `/templates/typescript/` — biome.json, .pre-commit-config.yaml, tsconfig.json, a Zod schema example, Stryker config, package.json devDependencies snippet, and a /templates/typescript/README.md. Foreseeable problems: Biome strictness level, full strict TS mode, Stryker scoping, Biome version pin. Astro-specific overlay is separate and NOT part of 1C.

## Verification step at the end of Phase 1C

Drop `/templates/typescript/` files into an empty test repo. Initialize with `pnpm init`. Install Biome. Write a deliberately bad `.ts` file containing both a style violation and a security flag:

```typescript
// test/bad.ts
var x: any = 1;
eval("console.log(1)");
const secret = "AKIAIOSFODNN7EXAMPLE";
```

Confirm:

- ✅ Biome flags `var` and `any`
- ✅ Pre-commit hook blocks the commit
- ✅ Semgrep (run via CI from Phase 1B's `security.yml`) flags `eval()`
- ✅ Gitleaks flags the AWS key pattern

If any step fails, the overlay is incomplete. Fix before Phase 1C is declared done.
