#!/usr/bin/env bun
// Optional narrow syntax profile, NOT semantic purity/JSON-serializability proof.
// Typecheck first. Aliased function types, runtime values and effects are outside it.
import { readFileSync } from "node:fs";
import ts from "typescript";

export function checkSource(filePath: string, source: string): string[] {
  const violations: string[] = [];
  const sourceFile = ts.createSourceFile(filePath, source, ts.ScriptTarget.Latest, true);
  function visit(node: ts.Node): void {
    let reason: string | undefined;
    if (ts.isClassDeclaration(node) || ts.isClassExpression(node)) {
      reason = "class syntax in selected component profile";
    } else if (ts.isMethodSignature(node)) {
      reason = `method signature ${node.name.getText(sourceFile)}`;
    } else if (ts.isPropertySignature(node) && node.type && ts.isFunctionTypeNode(node.type)) {
      reason = `direct function-typed field ${node.name.getText(sourceFile)}`;
    }
    if (reason) {
      const line = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
      violations.push(`${filePath}:${line}: ${reason}`);
    }
    ts.forEachChild(node, visit);
  }
  visit(sourceFile);
  return violations;
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const files =
    args.length > 0
      ? args
      : await Array.fromAsync(new Bun.Glob("server/src/components/**/*.ts").scan("."));
  if (files.length === 0) throw new Error("No component files selected");
  const violations: string[] = [];
  for (const file of files) {
    if (!/\/components\/.*\.ts$/.test(file))
      throw new Error(`Not a component source path: ${file}`);
    violations.push(...checkSource(file, readFileSync(file, "utf8")));
  }
  for (const violation of violations) console.error(violation);
  if (violations.length > 0) process.exitCode = 1;
}

if (import.meta.main) await main();
