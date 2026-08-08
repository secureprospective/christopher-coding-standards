# TypeScript Overlay — Adoption Guide

Part of `christopher-coding-standards`. Applies to any TypeScript project (Node, React, Astro, etc.).

**Note for Astro projects:** Use this overlay for `.ts`/`.tsx` files, then add the [Astro overlay](../astro/README.md) (Phase 1D) for `.astro` template files — it requires `prettier-plugin-astro` and a different Biome configuration, and replaces this overlay's `tsconfig.json`.

**Note for Cloudflare Workers projects:** Adopt this overlay first, then add the [Cloudflare Workers overlay](../cloudflare-workers/README.md) — it keeps this overlay's Biome/pre-commit/Gitleaks unchanged but replaces the `tsconfig.json` and `vitest.config.ts` (tests run inside the workerd runtime) and adds the Wrangler toolchain and typed bindings.

---

## What this overlay adds

| Layer | Tool | What it enforces |
|---|---|---|
| Formatter + linter | Biome 2.4 | Style, safety rules, `any` prohibition, null-assertion prohibition |
| Pre-commit hooks | pre-commit + Biome + Gitleaks | Blocks commits with lint failures or secrets |
| Type safety | TypeScript strict+ | `strict: true` + 3 additional flags (see tsconfig.json) |
| Boundary validation | Zod v4 | Schema-validated external input at every entry point |
| Testing | Vitest 3 | Fast, native ESM/TypeScript test runner |
| Mutation testing | Stryker + vitest-runner | Proves tests actually catch bugs, not just run |

---

## Adoption steps

### 1. Install pre-commit framework

```bash
pip install pre-commit
```

One-time setup. Runs on all future commits in this repo.

### 2. Copy files into your repo root

```
biome.json
.pre-commit-config.yaml
tsconfig.json
vitest.config.ts
stryker.config.mjs
Makefile
schemas/example.ts  →  src/schemas/example.ts  (move to your source tree)
```

### 3. Merge the package.json snippet

Open `package.json.snippet`. Add the `scripts` and `devDependencies` blocks into your project's `package.json`. Do not overwrite existing scripts — merge them.

The snippet ships the **pnpm guardrail** (fleet standard) in three pieces:

1. **`packageManager` pin** — `"packageManager": "pnpm@10.34.3"` plus a corepack pin (enable with `corepack enable`, then `corepack use pnpm@10.34.3` to register the version). This stops pnpm's major version from silently drifting between machines and CI.
2. **`preinstall` guard** — `"preinstall": "npx only-allow pnpm"`. If anything runs `npm install` or `yarn` in this repo it fails loud with a one-line error instead of silently producing a second lockfile. npm/yarn exit non-zero; pnpm passes.
3. **`--frozen-lockfile` discipline** — CI and any agent-driven install **must** use `pnpm install --frozen-lockfile` (never bare `pnpm install`), so the committed `pnpm-lock.yaml` is never silently rewritten. Add this to your CI and to the "Install" step of any agent workflow. If a dependency genuinely needs updating, do it deliberately with `pnpm add`/`pnpm update` and commit the lockfile change as its own PR.

```bash
pnpm install --frozen-lockfile
```

### 4. Activate pre-commit hooks

```bash
pre-commit install
```

Hooks will now run on every `git commit`.

### 5. Customize the placeholders

**In `biome.json`:** The defaults work as-is. If your project uses single quotes or tabs, adjust `javascript.formatter.quoteStyle` and `indentStyle`.

**In `tsconfig.json`:** Update `"outDir"`, `"rootDir"`, and `"lib"` for your project structure. The strictness flags should not be changed.

**In `vitest.config.ts`:** Change `environment` to `"jsdom"` if your tests require browser APIs (React component tests).

**In `stryker.config.mjs`:** Update the `mutate` glob if your source is not under `src/`.

### 6. Pin the pre-commit hook SHAs (required before production)

The `.pre-commit-config.yaml` ships with version tags. Version tags can be force-pushed — this is how the 2026 Trivy supply chain attack worked.

**To generate pinned SHAs:**

```bash
# Install StepSecurity's pin-github-actions tool
pip install pin-github-actions

# For the GitHub Actions workflow (from Phase 1B)
pin-github-actions .github/workflows/security.yml

# For pre-commit hooks — get SHA manually:
git ls-remote https://github.com/biomejs/pre-commit v2.4.16
git ls-remote https://github.com/gitleaks/gitleaks v8.27.2
```

Replace the `rev:` values in `.pre-commit-config.yaml` with the full 40-character SHA.

**To keep SHAs updated automatically:** Add `biomejs/pre-commit` and `gitleaks/gitleaks` to your Renovate or Dependabot configuration. They will open PRs when new versions release.

---

## ESM compatibility notes

This overlay is ESM-first (`"type": "module"` in package.json, `"module": "esnext"` in tsconfig).

**If something breaks:**

| Tool | Fix |
|---|---|
| `ts-node` | Switch to `tsx` (`pnpm add -D tsx`) or use `ts-node --esm` |
| Older Jest config | Not applicable — this overlay uses Vitest |
| `require()` in a dependency | Add `"moduleResolution": "node16"` as a fallback, or use a dynamic `import()` |

---

## Verification test

Run this after adoption to confirm all gates are live.

**Step 1:** Create a test file with deliberate violations:

```typescript
// test/bad.ts
var x: any = 1;
eval("console.log(1)");
const secret = "AKIAIOSFODNN7EXAMPLE";
```

**Step 2:** Try to commit it:

```bash
git add test/bad.ts
git commit -m "test: verify gates"
```

**Expected — all four must fire:**
- Biome flags `var` and `any` → pre-commit blocks the commit
- Gitleaks flags the AWS key → pre-commit blocks the commit
- `make lint` exits non-zero
- Semgrep (CI) flags `eval()` on the PR

If any gate does not fire, stop and diagnose before using this repo in production.

**Step 3:** Delete the test file and proceed.

---

## Mutation testing

Run locally:

```bash
make mutation-test          # incremental — changed files only
make mutation-test-full     # full scan — use for weekly audit
```

**Reading the report:** Open `reports/mutation/report.html` in a browser. Red mutants are surviving mutations — your tests did not catch them. Fix the tests, not the threshold.

**Thresholds:** 80 high / 60 low / 60 break. A build fails below 60.

---

## Phase status

- ✅ Phase 1A — repo skeleton
- ✅ Phase 1B — language-agnostic templates
- ✅ Phase 1C — TypeScript overlay (this directory)
- ✅ Phase 1D — Astro overlay (`templates/astro/`, split from 1C due to .astro formatting complexity)
- ✅ Cloudflare Workers overlay (`templates/cloudflare-workers/`) — extends this overlay for workerd-deployed projects
- ✅ Go overlay (`templates/go/`)
- ⏳ Phase 2 (cont.) — Python, Bash overlays
- ⏳ Phase 3 — local-model selection guidance, dual-model architecture doc
