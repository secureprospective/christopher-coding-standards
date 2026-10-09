import { cloudflareTest } from "@cloudflare/vitest-plugin";
import { defineConfig } from "vitest/config";

// Cloudflare Workers test config — runs tests INSIDE the workerd runtime via
// @cloudflare/vitest-plugin, so `env` bindings (D1/KV/Queues) exercise a local workerd runtime,
// not every deployed platform behavior. Requires Vitest 4.1+.
//
// NOTE on the API: this uses the current `cloudflareTest()` Vite plugin. The older
// `defineWorkersConfig` / `defineWorkersProject` + `test.poolOptions.workers` form is
// deprecated — do not reintroduce it.
//
// NOTE on mutation testing: Stryker's vitest-runner cannot drive the workerd pool.
// Keep mutation testing (from the base TS overlay) pointed at pure business-logic
// modules using the base vitest.config.ts; use THIS config for integration tests
// that need real bindings. Don't try to mutation-test inside the Workers pool.
export default defineConfig({
  plugins: [
    cloudflareTest({
      // Single source of truth for bindings — reuse wrangler.jsonc instead of
      // redefining test bindings, so tests can't drift from real config.
      wrangler: {
        configPath: "./wrangler.jsonc",
      },
    }),
  ],
  test: {
    include: ["src/**/*.{test,spec}.ts"],
    exclude: ["node_modules", "dist", ".stryker-tmp"],
  },
});
