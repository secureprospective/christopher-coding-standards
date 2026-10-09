# Workers — npm/workerd integration

Layer on the [TypeScript reference](../typescript/README.md), preserving local project rules. Current acceptance follows [HANDOFF](../../HANDOFF.md), not this configuration alone.

## Compose deliberately

- Keep base Biome and project-local read-only pre-commit/native Gitleaks hooks. Add only the generated output path `!worker-configuration.d.ts` to Biome's `files.includes` (adjust if generating elsewhere); do not exclude authored declarations wholesale. Merge Make targets; use `make PM=npm ...` for this npm reference.
- Replace base tsconfig/Vitest config with these platform files; merge `package.json.snippet`. For the exercised **default npm/workerd composition**, remove these inherited TypeScript-reference fields: `packageManager`, `scripts.preinstall`, the `pnpm` settings block (including its Stryker-only `typed-rest-client>qs` override), all `@stryker-mutator/*` devDependencies, and the `mutation-test`/`mutation-test:full` scripts. Do not remove the guard from pnpm projects or erase unrelated consumer rules. Do not retain conflicting package managers/locks. Zod remains a runtime dependency if the application's boundaries use it.
- Use `@cloudflare/vitest-plugin` and its `cloudflareTest()` plugin, not the old pool package/defineWorkersConfig API. Match Vitest/coverage; current selected4.1.11 includes the previously recorded Vitest fix. Install deliberately with npm to create/review `package-lock.json`; normal installs use `npm ci`. Review the actual graph/advisories/build scripts on dependency changes.
- Copy/merge `wrangler.jsonc`; set the project name/entrypoint and **preserve the application's compatibility date**. The reference date2026-06-01 is not a direction to change deployed runtime semantics. Add only required bindings/flags. Generated types and a local runtime do not establish deployed equivalence.
- Run `npm run cf-typegen` after configuration changes. `typecheck` regenerates then checks production **and tests**; the plugin's type entry supplies cloudflare:test types. Choose a project policy for committing or generating `worker-configuration.d.ts`; do not call stale generated output passing evidence.

```sh
npm run typecheck
npm test
npm run build    # dry-run bundle only; inspect generated output
```

`deploy` is an explicitly authorized publication operation; this kit does not authorize it. Do not execute secret-put, remote database/KV/queue operations or deploy while verifying a disposable fixture.

## Boundaries and tests

Bindings grant access to configured platform resources, but Workers can also issue outbound fetches. Configuration alone does not contain network effects or grant application-level permission. Keep secrets out of plaintext vars/source; scanner coverage is not complete. Observability needs deliberate redaction/sampling, not a guarantee of a complete audit trail.

Use the [official integration guide](https://developers.cloudflare.com/workers/testing/vitest-integration/write-your-first-test/) for cloudflare:workers exports and cloudflare:test lifecycle helpers. Test actual handlers/bindings, valid/rejected inputs, state preservation before rejection and effect failures. A module import test and an integration invocation have different coverage; local workerd is not a deployed Cloudflare service. Verify a missing binding yields the intended compiler diagnostic and a failing assertion actually rejects; arbitrary runtime startup failures do not count.

Optional mutation tooling is a different composition from the default above: select/install it deliberately, resolve its actual npm dependency graph/advisories (pnpm overrides do not apply to npm), and verify it rather than assuming the default Workers lock covers it. Mutation testing belongs to a separate Node-only logic suite/config with no cloudflare imports and explicitly selected source/test paths. Do **not** point inherited Stryker at this workerd config or assume switching test globs moves the runtime. Keep the Node Vitest config under a separate filename and configure Stryker's `vitest.configFile` accordingly; exercise that composition before promising it. Default Workers reference does not promise a mutation or coverage report from workerd.

No Workers package pin, generated type file or green hook proves complete compatibility, containment, authorization, deployed storage semantics or hosted enforcement. C6 runtime evidence is bounded to the tested Linux/Node/npm/plugin graph and synthetic fixture; actual applications still need their own checks.
