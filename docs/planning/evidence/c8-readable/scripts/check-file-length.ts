#!/usr/bin/env bun
// Optional review inventory, not a size/quality gate or a reason to split cohesive code.
import { readFileSync } from "node:fs";

export function physicalLines(source: string): number {
  if (source.length === 0) return 0;
  return source.split("\n").length - (source.endsWith("\n") ? 1 : 0);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const files =
    args.length > 0 ? args : await Array.fromAsync(new Bun.Glob("server/src/**/*.ts").scan("."));
  if (files.length === 0) throw new Error("No source files selected for line inventory");
  for (const file of files) {
    if (!/\.tsx?$/.test(file)) throw new Error(`Not a TypeScript source path: ${file}`);
    console.log(`${file}: ${physicalLines(readFileSync(file, "utf8"))} physical lines`);
  }
}

if (import.meta.main) await main();
