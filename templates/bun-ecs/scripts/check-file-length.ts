#!/usr/bin/env bun
// RULE 6 (ECS_RULES.md): max file length 300 lines. No stock TS/Biome rule
// enforces this — Biome has no line-count lint. Run against staged files
// via pre-commit, or against a full tree with no args.
import { readFileSync } from "node:fs";

const MAX_LINES = 300;

async function main() {
  const args = process.argv.slice(2);
  const files =
    args.length > 0
      ? args
      : (await Array.fromAsync(new Bun.Glob("server/src/**/*.ts").scan("."))).map((f) => f);

  let failed = false;
  for (const file of files) {
    if (!file.endsWith(".ts") && !file.endsWith(".tsx")) continue;
    const lineCount = readFileSync(file, "utf-8").split("\n").length;
    if (lineCount > MAX_LINES) {
      console.error(`${file}: ${lineCount} lines (max ${MAX_LINES})`);
      failed = true;
    }
  }

  if (failed) {
    console.error(
      "\nRULE 6 violation: split the file(s) above. An LLM's context window benefits too.",
    );
    process.exit(1);
  }
}

main();
