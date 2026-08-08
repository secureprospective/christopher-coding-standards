# Bun + ECS Overlay — Adoption Guide

Part of `christopher-coding-standards`. For a Bun-runtime, entity-component-system
game/simulation server (the pattern proven out on the Shadowbane Rebuild project).
**Extends the [TypeScript overlay](../typescript/README.md) — adopt that first.** This
overlay reuses Biome/gitleaks/Zod/Vitest-or-bun-test from the TS overlay and only
replaces `tsconfig.json` + `biome.json`, and adds ECS-specific enforcement the TS
overlay has no reason to know about.

**Why this exists as its own overlay, not just "the TS overlay used for a game":**
an ECS architecture has invariants no stock linter checks — entities are IDs only,
components are pure data with zero methods, systems import in one direction only,
files stay under a size an LLM's context window can hold whole. None of that is a
TypeScript concern; all of it is a real drift risk once an LLM is generating systems
across many sessions. This overlay makes those invariants **fail a commit**, not
just live in a doc a future session might skim past.

---

## What this overlay adds

| Layer | Tool | What it enforces |
|---|---|---|
| Runtime target | Bun (`tsconfig.json` `types: ["bun"]`, `moduleResolution: "bundler"`) | Replaces the TS overlay's Node-targeted `tsconfig.json` |
| Import layering | `dependency-cruiser` (`.dependency-cruiser.cjs`) | `shared ← ecs ← components ← systems ← game-loop`, no circular imports, broadcast-phase-only carveout into `db/`/`network/` |
| File size | `scripts/check-file-length.ts` (custom, pre-commit local hook) | 300-line cap — no stock TS/Biome rule covers this |
| Component purity | `scripts/check-component-purity.ts` (custom, AST-based, pre-commit local hook) | Rejects `class` declarations, method signatures, and function-typed fields inside `components/` |
| Formatter + linter | Biome 2.4 (this overlay's `biome.json` — adds a `scripts/**` override so the two checker CLIs can use `console.error`) | Same as TS overlay otherwise |
| Boundary validation | Zod v4 (`shared/protocol.ts` example) | Every inbound WebSocket message validated before it becomes a `TickInput` — "the client is a liar" |
| Secrets | Gitleaks | Same as every other overlay |

**This overlay does not re-decide the architecture.** The rules it enforces (RULE 1–10)
come from the actual game's `ECS_RULES.md`/`SYSTEM_ORDER.md` — read those in the adopting
project for the full rationale and the tick-pipeline ordering. This overlay is the
*enforcement*, not the *spec*.

---

## Adoption steps

### 1. Adopt the TypeScript overlay first

See `../typescript/README.md`. This overlay assumes that one is already in place
(pre-commit framework installed, `pnpm`/`bun install` working, Vitest or `bun test`
wired up).

### 2. Copy files into your repo root

```
tsconfig.json              →  repo root (REPLACES the TS overlay's tsconfig.json)
biome.json                 →  repo root (REPLACES the TS overlay's biome.json)
.dependency-cruiser.cjs    →  repo root
.pre-commit-config.yaml    →  MERGE the three local hooks + the two remote repos into
                               your existing .pre-commit-config.yaml (don't overwrite
                               your TS overlay's hooks — add to them)
scripts/                   →  repo root scripts/
```

### 3. Merge the package.json snippet

Open `package.json.snippet`. Merge the `scripts` and `devDependencies` blocks into
your project's `package.json` — don't overwrite existing scripts.

```bash
bun install
```

> **pnpm guardrail exemption:** this overlay is exempt from the fleet-standard
> `only-allow pnpm` guard (base TypeScript overlay) — Bun is the runtime AND package
> manager here, not an npm-vs-pnpm project. Do not add the base `preinstall` line when
> composing this overlay.

### 4. Lay out your source tree to match the layering rule

`.dependency-cruiser.cjs` hardcodes the path prefixes `server/src/{shared,ecs,components,
systems,network,db}` and `server/src/game-loop.ts`. Either use that exact layout, or
edit the regex paths in `.dependency-cruiser.cjs` to match yours — the rule *names*
(`shared-imports-nothing`, `simulate-systems-no-db-network`, etc.) matter more than the
literal paths.

`examples/server/src/` is a working reference tree — a `World`, a `GameSystem`
interface, four components, a simulate-phase system (`MovementSystem`) and a
broadcast-phase system (`NetworkSendSystem`) that demonstrates the RULE 5 carveout.
Copy the pattern, not necessarily the files verbatim.

### 5. Activate pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files   # first run installs the biome/gitleaks environments
```

### 6. Pin the pre-commit hook SHAs (required before production)

Same reasoning as every other overlay in this repo — see
`docs/adr/0001-why-this-standard-exists.md`. `.pre-commit-config.yaml` ships with SHAs
already pinned for `biome-check` (`v2.4.16`) and `gitleaks` (`v8.30.1`); re-verify them
before relying on this in production:

```bash
git ls-remote https://github.com/biomejs/pre-commit v2.4.16
git ls-remote https://github.com/gitleaks/gitleaks v8.30.1
```

---

## Why `dependency-cruiser`, not `madge`

`ECS_RULES.md` RULE 5 originally suggested `madge --circular` as the check. That only
catches circular imports — it does not catch a simulate-phase system quietly importing
`db/` or `network/`, which is the actual drift risk on an LLM-generated codebase (a wrong
import on line 5 of a 150-line system file is invisible in a review focused on game
logic). `dependency-cruiser` enforces the full layering rule as declarative config *and*
can render the dependency graph as Mermaid in the same command — this was locked as an
architecture-panel decision on the Shadowbane Rebuild project (2026-07-26); ported here
as the reusable enforcement pattern.

**Version floor:** pin `dependency-cruiser` to `17.4.3`, not `^17.4.3` and not `18.x`.
`18.x` requires Node `^22||^24||>=26` (or Bun's equivalent compat surface) — verified
live: `18.1.0` hard-fails under Bun 1.3.14 (`Your node version (20.20.2) is not
supported`). `17.4.3` requires `^20.12`, which the Bun/Node 20 LTS line most adopters
are still on satisfies. Re-check `npm view dependency-cruiser@<version> engines` before
bumping.

---

## Why two custom pre-commit hooks instead of a stock linter rule

Biome has no file-line-count rule and no way to express "an interface in this specific
directory may not declare a method." Go's overlay in this repo solves the analogous
problem with a custom `go/analysis` vettool (`ifaceguard`); this overlay's answer is two
small Bun scripts run as `language: system` local hooks (same pattern this repo's Bash
overlay used for its `lib/strict-mode.sh` — reach for a small purpose-built tool before
assuming no gate is possible).

- `check-file-length.ts` — line-counts every `server/src/**/*.ts` file (or the staged
  files pre-commit passes it), fails over 300 lines.
- `check-component-purity.ts` — parses every `components/**/*.ts` file with the real
  TypeScript compiler API (not regex, so it isn't fooled by comments or string literals)
  and fails on any `class` declaration, `MethodSignature`, or property typed as a
  function — the last one closes the same gap RULE 1's snapshot requirement flags:
  `Set`/`Map`/functions on a component silently break `World.exportSnapshot()`.

**Verification discipline applied while building this overlay (same standard as every
prior overlay in this repo):** every gate — `tsc`, Biome, both custom scripts, and
`dependency-cruiser`'s five rules (four layering directions + the broadcast carveout +
circular-import detection) — was proven live through **actual `pre-commit run`**, not
just the standalone CLI, against both a clean example tree and a deliberate violation
per gate (a component with a method + a function-typed field, a 311-line file, a
simulate-phase system importing `db/`, a two-file circular import, and a planted
AWS-shaped secret via gitleaks). All five failed correctly and all five passed clean on
the compliant tree. The example tree was also smoke-run under real Bun (`bun run`) —
`World.exportSnapshot()` was confirmed to produce plain, `JSON.stringify`-able output
end to end, not just type-check clean.

---

## Relationship to the TypeScript overlay

| | TypeScript overlay | This overlay |
|---|---|---|
| Runtime | Node (or any) | Bun |
| `tsconfig.json` | Node-targeted, `moduleResolution: "bundler"` | **Replaces** — Bun-targeted (`types: ["bun"]`, `module: "Preserve"`, `moduleDetection: "force"`) |
| `biome.json` | Base config | **Replaces** — adds a `scripts/**` override for the two checker CLIs |
| Pre-commit | Biome + gitleaks | **Adds** three local hooks (`dependency-cruiser`, file-length, component-purity) |
| Zod | Generic boundary validation | Same pattern, applied specifically to inbound WebSocket messages (`shared/protocol.ts`) |
