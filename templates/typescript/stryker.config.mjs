/** @type {import('@stryker-mutator/api/core').PartialStrykerOptions} */
export default {
  // Use Vitest as the test runner.
  testRunner: "vitest",

  // Point at your vitest config if not at project root.
  // vitest: { configFile: "vitest.config.ts" },

  // Files to mutate. Excludes test files, schemas, and generated code.
  mutate: [
    "src/**/*.ts",
    "!src/**/*.{test,spec}.ts",
    "!src/**/*.d.ts",
    "!src/schemas/**",
  ],

  // TypeScript support.
  checkers: ["typescript"],
  tsconfigFile: "tsconfig.json",

  // Incremental mode: only re-test mutants in files changed since last run.
  // Dramatically faster for PR cycles. Full scan runs on the weekly cron.
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

  // Concurrency: 1 because StrykerJS manages its own parallel workers.
  // The vitest runner requires threads: true (default). Do not set to false.
  concurrency: 4,

  // Timeout per mutant in milliseconds.
  timeoutMS: 30000,

  // Ignore temporary Stryker files from git.
  tempDirName: ".stryker-tmp",
};
