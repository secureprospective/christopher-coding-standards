/** @type {import('@stryker-mutator/api/core').PartialStrykerOptions} */
export default {
  // Use Vitest as the test runner.
  testRunner: "vitest",
  // Explicit modules also work with pnpm's isolated dependency layout.
  plugins: ["@stryker-mutator/vitest-runner", "@stryker-mutator/typescript-checker"],

  // Point at your vitest config if not at project root.
  // vitest: { configFile: "vitest.config.ts" },

  // Files to mutate. Excludes test files, schemas, and generated code.
  mutate: ["src/**/*.ts", "!src/**/*.{test,spec}.ts", "!src/**/*.d.ts", "!src/schemas/**"],

  // TypeScript support.
  checkers: ["typescript"],
  tsconfigFile: "tsconfig.json",

  // Reuse compatible prior results; invalidation follows Stryker's cache rules.
  // Use the full command for independent baselines and after relevant changes.
  incremental: true,
  incrementalFile: ".stryker-tmp/incremental.json",

  // Quality thresholds. Build fails if mutation score drops below break.
  // 80% line coverage with a 40% mutation score means tests observe but don't assert.
  thresholds: {
    high: 80,
    low: 60,
    break: 60,
  },

  // Reporters.
  reporters: ["html", "progress"],
  htmlReporter: { fileName: "reports/mutation/report.html" },

  // Conservative reference budget; tune deliberately for the project/host.
  concurrency: 1,

  // Timeout per mutant in milliseconds.
  timeoutMS: 30000,

  // Ignore temporary Stryker files from git.
  tempDirName: ".stryker-tmp",
};
