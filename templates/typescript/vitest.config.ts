import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    // Run tests in Node environment by default.
    // Change to "jsdom" for browser-environment tests (e.g. React components).
    environment: "node",

    // Show verbose output per test file.
    reporters: ["verbose"],

    // Coverage via v8 — fastest option, no instrumentation overhead.
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov", "html"],
      reportsDirectory: "./coverage",
      // Fail CI if coverage drops below these thresholds.
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },

    // Test file patterns.
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
    exclude: ["node_modules", "dist", ".stryker-tmp"],
  },
});
