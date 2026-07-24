# Astro Overlay — Adoption Guide

Part of `christopher-coding-standards`. Applies to Astro projects (with or
without `@astrojs/react`).

**Prerequisite:** the [TypeScript overlay](../typescript/README.md) (Phase
1C). Install that first — it covers `.ts`/`.tsx`/`.js` files. This overlay
adds the pieces that overlay's README flagged as Astro-specific: formatting
and type-checking for `.astro` files.

---

## What this overlay adds

| Layer | Tool | What it enforces |
|---|---|---|
| Formatter for `.astro` | Prettier 3 + `prettier-plugin-astro` | Biome does not format `.astro` files; Prettier handles them, including the frontmatter script block |
| Type safety for `.astro` | `astro check` (`@astrojs/check`) | `tsc` cannot parse `.astro` syntax — `astro check` is the Astro-aware equivalent |
| Pre-commit hook | pre-commit + Prettier, scoped to `*.astro` | Blocks commits with unformatted `.astro` files |
| CI | `astro — check` job in `.github/workflows/security.yml` | Runs `astro check` + `prettier --check` on PRs; no-ops if no `astro.config.*` exists |

Biome continues to own `.ts`/`.tsx`/`.js` formatting and linting unchanged —
this overlay does not replace it, only excludes `.astro` from its scope.

---

## Adoption steps

### 1. Confirm prerequisites

- TypeScript overlay (`templates/typescript/`) already adopted.
- Astro project (`astro.config.mjs`/`.ts`/`.mts` exists at repo root).

### 2. Copy `.prettierrc.json` to repo root

If the project doesn't already have a Prettier config, copy this file as-is.
If it does, merge the `plugins` array and the `*.astro` override — do not
drop existing overrides.

### 3. Exclude `.astro` from Biome

Add `"**/*.astro"` to the `files.ignore` array in your existing `biome.json`
(from the TypeScript overlay):

```jsonc
{
  "files": {
    "ignore": [
      "node_modules",
      "dist",
      "build",
      // ...existing entries...
      "**/*.astro"
    ]
  }
}
```

### 4. Replace `tsconfig.json`

**Which tsconfig do I use?** This directory's `tsconfig.json` *replaces*
`templates/typescript/tsconfig.json` for Astro projects — it extends
`astro/tsconfigs/strictest`, which is a superset of the strictness flags the
TypeScript overlay's tsconfig adds by hand, adapted for Astro's build model
(`noEmit`, Astro client types, `moduleDetection`). Don't try to merge the
two; copy this one over the TypeScript overlay's.

If the project doesn't yet depend on `astro`, the `extends` path won't
resolve — confirm `astro` is a dependency first (it will be, in any real
Astro project).

### 5. Merge `package.json.snippet`

Add the `scripts` and `devDependencies` blocks into your project's
`package.json` — merge, don't overwrite. Then:

```bash
pnpm install
```

### 6. Merge `Makefile.snippet`

Add the three new targets into your existing `Makefile`.

### 7. Merge `.pre-commit-config.yaml.snippet`

Add the `prettier-astro` hook into your existing `.pre-commit-config.yaml`.
Unlike the TypeScript/Go/Python overlays' hooks, this is a **`repo: local`**
hook, not a pinned remote repo — there's no `rev:` to pin. It runs `npx
--no-install prettier` against your project's own `prettier` +
`prettier-plugin-astro` (installed via step 5's `package.json.snippet`
devDependencies), so pin those *package versions* instead, the same
discipline as any other devDependency. See "Why a local hook, not
mirrors-prettier" below for why the remote-hook form doesn't work here.

### 8. Enable the CI job

`astro — check` is already defined in `.github/workflows/security.yml`
(copied in Phase 1B) and no-ops automatically if no `astro.config.*` exists.
Once this overlay is adopted, add `astro — check` to the branch protection
required-checks list alongside `ts — lint` / `ts — test`.

---

## Why a local hook, not mirrors-prettier

Found by the 2026-07-24 cross-pollination audit (GLM 5.2 recon + Claude
triage — `docs/cross-pollination-log.md`), which this overlay had never had
before: the `pre-commit/mirrors-prettier` remote hook this overlay originally
shipped was broken two ways.

1. **The pinned `rev: "v3.4.2"` doesn't exist.** `mirrors-prettier`'s newest
   tag is `v3.1.0` — the hook fails at environment init with `pathspec
   'v3.4.2' did not match any file(s) known to git`, before it ever runs.
2. **Repinning to a real tag doesn't fix it.** `additional_dependencies`
   installs `prettier` + `prettier-plugin-astro` into the hook's own
   *isolated* node environment, not the project's `node_modules`. Prettier
   3's plugin loader resolves `plugins: ["prettier-plugin-astro"]` via
   standard ESM package resolution from the file being formatted — it
   cannot see across environments, `NODE_PATH` included. Confirmed live:
   `[error] Cannot find package 'prettier-plugin-astro'`.

The fix is the `repo: local` hook now shipped: it runs `npx --no-install
prettier --write` against the project's own installed `prettier` +
`prettier-plugin-astro` (already devDependencies via
`package.json.snippet`), where plugin resolution works normally. Verified
live end-to-end through `pre-commit run` itself, not just the standalone
CLI: `prettier (astro) ... Failed - files were modified by this hook`, with
a real before/after diff on the malformed test file.

## What's out of scope

- **End-to-end / visual testing** of `.astro` pages (Playwright or similar)
  is not covered by this overlay or by Vitest from the TypeScript overlay.
  Flag to the human owner if the project needs it — not yet standardized.
- **Mutation testing** (Stryker) continues to apply to `.ts`/`.tsx` test
  files only, unchanged from the TypeScript overlay. `.astro` files
  themselves are not mutation-tested.

---

## Verification test

Run this after adoption to confirm the new gates are live.

**Step 1:** Create a deliberately unformatted `.astro` file:

```astro
---
const   title="test"
---
<html><body><h1>{title}</h1></body></html>
```

**Step 2:** Try to commit it:

```bash
git add test.astro
git commit -m "test: verify astro gates"
```

**Expected (confirmed live 2026-07-24 — see "Why a local hook" above):**
- `npx prettier --write "**/*.astro"` (and the `prettier-astro` pre-commit
  hook, same mechanism) reformats the file — `const   title="test"` →
  `const title = "test";`, blank line inserted after frontmatter.
- `astro check` (`make typecheck-astro`) resolves `extends:
  astro/tsconfigs/strictest` with no changes needed to `tsconfig.json`,
  passes clean on valid code, and correctly fails
  (`ts2322: Type 'string' is not assignable to type 'number'`) on a
  deliberately mistyped prop (e.g. `<Counter count="five" />` where the
  component expects `number`). `strictest`'s rules are genuinely active,
  not silently no-op'd — confirmed via an unrelated unused-variable catch
  (`ts6133`, a `strictest`-only rule) in the same test pass.
- On a PR, the `astro — check` CI job runs and reports the same.

If any gate does not fire, stop and diagnose before using this overlay in
production.

**Step 3:** Delete the test file and proceed.

---

## Phase status

- ✅ Phase 1A — repo skeleton
- ✅ Phase 1B — language-agnostic templates
- ✅ Phase 1C — TypeScript overlay (`templates/typescript/`)
- ✅ Phase 1D — Astro overlay (this directory) — pre-commit hook fixed
  2026-07-24 following the cross-pollination audit above
- ✅ Phase 2 — Go, Cloudflare Workers, Python, Bash overlays all complete
- ✅ Phase 3 — local-model selection guidance (`docs/local-model-guidance.md`)
