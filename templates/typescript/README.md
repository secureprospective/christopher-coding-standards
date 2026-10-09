# TypeScript — Node/ESM reference overlay

Copy and merge into a suitable project; this is not a complete application or an automatic migration. Default reference: Node24+, pnpm10.34.3, TypeScript5, Biome2, Zod4, Vitest4.1.11 with matching V8 coverage, optional Stryker9. Actual accepted versions/evidence follow [HANDOFF](../../HANDOFF.md); metadata/pins are not universal compatibility or security proof.

## Adoption

1. Preserve the project's scripts, constraints and ownership. Copy `biome.json`, `tsconfig.json`, `vitest.config.ts`, `.pre-commit-config.yaml` and, if useful, `stryker.config.mjs`. Merge Make targets rather than replacing an existing Makefile.
2. Merge `package.json.snippet` into the real manifest. Copy `scripts/check-package-manager.mjs` at that exact relative path; place **both** `schemas/example.ts` and `schemas/example.test.ts` under `src/schemas/`. Zod is a runtime dependency. Choose actual source/output paths and platform libraries; strict flags remain unless a project-specific compatibility change is justified/reviewed. Typecheck includes tests. Browser tests need an explicitly installed compatible environment such as jsdom; the Node reference does not supply one.
3. Provision the declared pnpm version without global changes by default. Corepack or an already verified project toolchain can provide it; don't blindly enable/update global shims. The local lifecycle guard checks the consumer's declared version without fetching an unpinned package. It rejects routine npm/wrong-version installs; ignored scripts/spoofed environment can bypass it, and a failed wrong-manager install may already have written files. It is not isolation, authorization or a guarantee against a second lockfile.
4. **First adoption/dependency change:** deliberately run `pnpm install` to create/update `pnpm-lock.yaml`; inspect resolution, dependency source/integrity, advisories and lifecycle/build-script decisions, then commit the reviewed manifest/lock together. Do not use a missing lock as a reason to disable enforcement. **Normal local/agent/CI installs:**

   ```sh
   pnpm install --frozen-lockfile
   ```

   A lock captures the consumer's actual graph, not every future composition. Recheck advisories/compatibility when changing dependencies. The scoped `typed-rest-client>qs` override selects6.16.0 because Stryker's resolved caller2.3.1 pins vulnerable6.15.1 (GHSA-q8mj-m7cp-5q26, GHSA-x5fp-wj9c-mxmx, GHSA-4mjr-xmp4-gh2g); retain/review it with the lock until upstream resolution is patched. Do not suppress the audit or apply a blanket transitive override. Vitest and coverage versions must match; GHSA-82fw-gwwq-j7x9 affected the former Vitest3 line and is fixed at stable4.1.11. This reference does not expose a dev-server API; do not expose test/dev servers casually.
5. Install pre-commit in the approved tool environment; provision and verify native Gitleaks8.30.1 and install the project dependencies first. Run `pre-commit install`, then check the actual hooks. Biome uses **the project's locked local binary** read-only, avoiding a second unpinned npm hook environment. Gitleaks uses an immutable upstream hook commit and the native scanner (no automatic Go SDK bootstrap); its binary version/integrity is still the owner's responsibility.

The kit's inherited `security.yml` still uses npm-ci: it is incompatible with this pnpm contract until C12 repairs it. Installing this overlay does not make that workflow live or accepted. Do not remove the guard or claim skipped jobs passed.

## Behavior and evidence

The example returns parsed data or null; callers reject null before effects, map errors safely and separately authorize operations. A valid `admin` role is **not** permission. Unknown-field rejection is this example's protocol decision, not a universal Zod rule. No validation-error logging is performed. Async refinements require the async parser. The test demonstrates actual exported parsers and a small caller, not an HTTP/database integration or access-control system.

```sh
make lint             # read-only style, imports and configured lint rules
make format-check
make typecheck        # production and test sources; no emit
make test             # missing suite fails, not green
make test-coverage    # explicit production include, including unimported files
```

Coverage thresholds are a reference floor (80lines/functions/statements,75branches), not proof of assertions. Adjust the production include/exclude patterns to the real application. TypeScript checks are not runtime validation. `skipLibCheck` trades checking dependency declarations for speed; it does not prove their soundness.

Verify each changed gate independently with clean input and its intended violation: e.g. Biome `noExplicitAny`, compiler TS2322, a genuinely failing assertion, coverage loss in an untested production file. Observe exact diagnostics/exit codes and unchanged declared inputs; missing tools/arbitrary errors are not intended rejections. Use the kit's [fixture checker](../../tools/README.md) where useful. Do not try to commit known-broken code to prove a hook, weaken tests, or plant real credentials. Run hooks directly on disposable staged fixtures; perform ordinary commits only on clean input.

Gitleaks hooks scan **staged diff**, even with `pre-commit --all-files`; an explicit directory scan is a different check. A harmless custom-rule sentinel can demonstrate scanner wiring without claiming default secret-policy completeness. Pre-commit only sees its selected file types; project-specific sources/generated/symlink targets need deliberate coverage.

## Optional mutation testing

```sh
make mutation-test-full   # independent full baseline
make mutation-test        # cached incremental results when compatible
```

Use when risk or an assertion gap warrants it, not as a mandatory ritual. Customize `mutate`: this reference excludes tests, declarations and schemas, so the schema's tests do **not** establish a schema mutation score. Stryker's cache invalidation is not simply "changed files only"; prefer full checks after material config/test changes. Reference thresholds80high/60low/60break reject below60; tune to the project's actual guarantees, not to hide surviving bugs. Inspect survivors against intended behavior; equivalent mutations may need reasoned disposition. Concurrency1 is a conservative host budget, not a tool requirement.

## Composition

- [Workers](../cloudflare-workers/README.md) replaces platform/type/test configs and currently chooses npm; C6 must demonstrate its actual pool/plugin/Vitest contract. Keep its own manager/lock contract rather than copying the pnpm lifecycle guard.
- [Astro](../astro/README.md) adds Astro/template formatting and generated types; C7 must clear the merged contract. Its inherited preinstall snippet must not overwrite this local guard with an unpinned npx download.
- [Bun/ECS](../bun-ecs/README.md) chooses Bun; C8 owns runtime, commands and dependency compatibility.
- Make defaults to pnpm; `make PM=npm test` or `make PM=bun test` is only appropriate after the project's manifest/guard/lock contract has been composed accordingly. The wrapper alone does not change it.

Use framework-specific ESM resolution deliberately. `moduleResolution: bundler` is not proof Node can execute emitted imports; a deployed Node library may require a paired NodeNext module/resolution configuration and an actual build/runtime check. No dependent overlay, Windows/other platform, hosted enforcement or live consumer is accepted by this reference alone.
