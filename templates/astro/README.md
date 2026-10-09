# Astro — formatting, generated types and optional React

Layer on the [TypeScript reference](../typescript/README.md), preserving local rules. Current acceptance follows [HANDOFF](../../HANDOFF.md); configuration alone is not verified adoption.

## Compose deliberately

1. Merge `package.json.snippet` with the base/project manifest; do not replace unrelated scripts/dependencies. Preserve the base **local** `scripts/check-package-manager.mjs`, `preinstall`, pnpm pin and scoped dependency override. This snippet intentionally does not overwrite them with an npx bootstrap. Reference Node24+ matches the base contract; actual existing Astro applications need compatibility/migration checks before changing framework versions.
2. Copy/merge `.prettierrc.json`; retain existing plugins/overrides. Prettier owns `.astro`, including frontmatter; Biome owns TS/TSX/JS. In Biome2's `files.includes`, retain existing entries and append `!**/*.astro` and `!**/.astro` (generated output). Do not use obsolete `files.ignore` or exclude authored declarations wholesale.
3. Merge this `tsconfig.json` with local options, replacing the Node-only base `extends`/include configuration. Astro's strictest preset and explicit base checks apply to production, configs and tests. Include `.astro/types.d.ts`; `astro check` generates types before checking. Do not mistake bare tsc for checking `.astro` syntax.
4. This default does **not** require React. If using `@astrojs/react`/TSX, install mutually compatible integration, React/ReactDOM and corresponding types, add `react()` to `astro.config.mjs`, and merge `compilerOptions.jsx = "react-jsx"` and `jsxImportSource = "react"`. Check/build that composition separately; enabling JSX options alone does not install or enable the renderer.
5. Deliberately initialize/review the changed graph with `pnpm install --no-frozen-lockfile`; commit/review the lock. This explicit initialization/update is also needed when CI defaults to frozen installation with an existing lock. Normal installs use `pnpm install --frozen-lockfile`. Review advisories and dependency build-script policy; no blanket allow-builds, disabled guard or arbitrary-error acceptance.
6. Merge Make targets and the hook into existing files. The read-only hook uses the project's installed/locked Prettier/plugin via pnpm; it does not write files or resolve a separate hook environment. Package pins/locks are version/integrity controls, not authenticated approval or isolation.

```sh
pnpm install --frozen-lockfile
make lint
make lint-astro
make typecheck
make test
pnpm run build
```

`typecheck` and `typecheck:astro` both use the Astro-aware checker. Keep an existing application's deployment/build policy; the reference build is local output only. Preview/dev start servers and require deliberate local use; neither is deployment authority.

## Verify actual behavior

On a disposable authorized consumer, exercise a valid page and actual component props, generated types, TS tests and build. For React, observe a valid TSX component rendered by the selected integration and a mistyped prop rejected by `astro check`; non-React projects should also pass without React dependencies. Observe `.astro` interpolation/rendered output as appropriate, not just module import.

Introduce one unformatted `.astro` file; `lint-astro` and the installed read-only hook should reject with the formatting diagnostic while preserving bytes. Run `format-astro` deliberately, then verify clean hook/checks again. A path with spaces is an argv test, not filesystem containment. Add a mistyped frontmatter value/prop and require the specific compiler diagnostic, restore, rerun. Missing tools, generated-output startup errors and empty selections are not intended rejections.

Vitest's Node logic tests do not prove page hydration, browser interaction or visual/accessibility behavior. Optional Stryker mutates selected **production** TS sources using its configured runner, not test files or `.astro`; select/exercise source/runtime/config separately before promising component mutation or coverage. This overlay does not establish browser/E2E behavior, deployed rendering or hosted required-check enforcement. Configure/run consumer CI deliberately; do not assume this kit's historical conditional jobs ran on a consumer or change hosted protection without authority.
