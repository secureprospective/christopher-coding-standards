/**
 * OPTIONAL example-specific import profile, not a universal DAG/purity policy.
 * Select/adapt/test paths and filename carveouts before enabling a consumer gate.
 * Static import rules do not contain runtime network/DB effects or grant permission.
 * Run: depcruise --config .dependency-cruiser.cjs --output-type err server/src
 */
module.exports = {
  forbidden: [
    {
      name: "no-circular",
      severity: "error",
      comment: "This selected example profile rejects static import cycles.",
      from: {},
      to: { circular: true },
    },
    {
      name: "shared-imports-nothing",
      severity: "error",
      comment: "shared/ cannot import the selected higher-layer paths below.",
      from: { path: "^server/src/shared" },
      to: { path: "^server/src/(ecs|components|systems|network|db)" },
    },
    {
      name: "ecs-imports-shared-only",
      severity: "error",
      comment: "ecs/ (World, GameSystem) may only import shared/.",
      from: { path: "^server/src/ecs" },
      to: { path: "^server/src/(components|systems|network|db)" },
    },
    {
      name: "components-are-leaves",
      severity: "error",
      comment: "components/ are plain data (RULE 2) — they must not import systems/db/network.",
      from: { path: "^server/src/components" },
      to: { path: "^server/src/(systems|network|db)" },
    },
    {
      name: "network-imports-shared-only",
      severity: "error",
      comment: "network/ (the WebSocket layer) may only import shared/ (protocol.ts).",
      from: { path: "^server/src/network" },
      to: { path: "^server/src/(ecs|components|systems|db)" },
    },
    {
      name: "db-imports-shared-only",
      severity: "error",
      comment: "db/ may only import shared/.",
      from: { path: "^server/src/db" },
      to: { path: "^server/src/(ecs|components|systems|network)" },
    },
    {
      name: "simulate-systems-no-db-network",
      severity: "error",
      comment:
        "RULE 5 carveout: only save-/network-send-/flight-recorder-system.ts may import db/ or " +
        "network/ (the broadcast phase, where RULE 9 side effects are allowed). Every other system " +
        "stays inside components/, ecs/, game-data/, shared/.",
      from: {
        path: "^server/src/systems/(?!.*(save|network-send|flight-recorder)-system\\.ts$)",
      },
      to: { path: "^server/src/(db|network)" },
    },
  ],
  options: {
    // Production import profile only; harness imports cross layers intentionally.
    // Test files remain included in tsc/Bun tests; filename scope is not anti-bypass.
    exclude: { path: "\\.(test|spec)\\.tsx?$" },
    tsPreCompilationDeps: true,
    tsConfig: { fileName: "tsconfig.json" },
    doNotFollow: { path: "node_modules" },
  },
};
