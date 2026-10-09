# Bun — runtime and optional ECS example profile

Layer on the [TypeScript reference](../typescript/README.md), preserving consumer rules. Current acceptance follows [HANDOFF](../../HANDOFF.md). The example is not a game specification or authority to change a live Shadowbane project.

## Compose deliberately

- Merge `package.json.snippet`; select Bun1.4.2 and its matching types deliberately. Node24+ remains needed for the selected Node-shebang development tools; Bun's emulated process.version is not an installed Node version or complete compatibility proof.
- In this default Bun composition, replace the base packageManager pin; remove base `scripts.preinstall`, `pnpm` settings/override, all `@stryker-mutator/*`, `vitest` and `@vitest/coverage-v8` devDependencies, mutation scripts and the inherited coverage script. Use Bun test imports/configuration rather than running Vitest's test API under Bun. Preserve unrelated consumer scripts/settings. Retain Zod as a **runtime** dependency. Do not remove the pnpm guard from pnpm projects.
- Merge this tsconfig/Biome with local options. Tests and checker scripts are included in typechecking. Bun compiles TypeScript but does not replace `tsc` checking. The Biome CLI-only console override is not permission to log sensitive application data.
- Deliberately initialize/update with `bun install`, review/commit `bun.lock`; routine installs use `bun install --frozen-lockfile`. Review resolved graph/advisories/build-script policy. A packageManager field is not an anti-bypass/no-write guarantee; do not maintain competing lockfiles or disable applicable guards to get green.
- Merge Make targets, choosing `PM ?= bun` as the consumer default (a later second `?=` does not override the base pnpm assignment), or invoke `make PM=bun ...`. Merge read-only project-local Biome/immutable native Gitleaks hooks; replace duplicate resolver hooks, preserving custom hooks. Verify/install the selected native scanner as described by the base reference; do not implicitly bootstrap a Go SDK. Hook scanning/pins are not complete secret detection, authenticated approval or containment.

```sh
bun install --frozen-lockfile
bun run check:all    # typecheck, lint, actual Bun tests
```

Test actual boundary exports and callers: valid/rejected payloads, effect ordering and state preservation. Shape validation is not entity ownership, permission, rate/range enforcement or application safety. Introduce one diagnostic-specific lint/type/assertion failure, restore, rerun. Missing tools/empty discovery/arbitrary nonzero are not passes. Exercise actual installed hooks and a clean commit on a disposable authorized consumer.

## Optional example architecture

`examples/server/src` demonstrates UUID entities, components, ordered simulate/broadcast responsibilities and a schema boundary. Copy the pattern only if appropriate; it does not mandate pure components, a DAG, fixed file size or a distributed rewrite. Preserve the adopting project's architecture/guarantees and justify any profile selection there.

The supplied `.dependency-cruiser.cjs` is a **project-specific optional** import profile for `server/src/{shared,ecs,components,systems,network,db}`. `bun run check:deps` checks those selected production static import patterns/cycles, excluding test/spec filenames (tests still typechecked/executed); paths and filename carveouts are not runtime effect authorization or network containment. It is not part of default check:all or hooks. Configure/test the actual graph before enabling a consumer gate. Selected17.4.3 is checked on this tool/runtime graph; do not reuse historical unsupported-version assertions as current compatibility evidence.

`check:components` is an optional narrow TypeScript syntax check, not semantic purity or JSON-serializability proof. Read its actual checked node kinds and exclusions, run typecheck first, and exercise meaningful positive/negative cases before gating. Aliases/runtime values/custom serializers/side effects need their own review/tests. `check:file-length` reports physical lines for review; it does not impose a300-line cap, ratchet or demand artificial splitting. Split by changing responsibility/data ownership, not to satisfy a count.

The example World accepts trusted component values and a caller-selected generic cast; it does not runtime-validate component/type relationships. Snapshot export/import preserves shallow component references, not immutable point-in-time state or arbitrary JSON serialization. Tests should observe the declared aliasing plus round-trip behavior for the actual plain example values. NetworkSendSystem's snapshot is a placeholder: no network broadcast occurs. Input schema selection/unknown-field behavior and caller validation precede effects; application authorization still belongs to the consumer.

Optional Node/Vitest mutation/coverage requires a separately installed/resolved/configured/exercised suite, not inherited C5 promises applied to Bun. This reference does not establish browser, deployed service, race-freedom, replay/distribution, hosted enforcement or universal safety. No live project enrollment, publishing/deployment or hosted protection changes are authorized by adoption.
