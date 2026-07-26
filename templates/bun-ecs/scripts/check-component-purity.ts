#!/usr/bin/env bun
// RULE 2 (ECS_RULES.md): components are data, zero methods. No stock
// TS/Biome rule catches this — it's a project-specific architectural
// invariant, not a general lint. AST-based (not regex) so it isn't fooled
// by comments or string literals containing the word "class".
import { readFileSync } from "node:fs";
import ts from "typescript";

const COMPONENTS_GLOB = "server/src/components/**/*.ts";

function checkFile(filePath: string, source: string): string[] {
  const violations: string[] = [];
  const sourceFile = ts.createSourceFile(filePath, source, ts.ScriptTarget.Latest, true);

  function visit(node: ts.Node) {
    if (ts.isClassDeclaration(node)) {
      const line = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
      violations.push(
        `${filePath}:${line}: class declaration in a component file — components are plain data (RULE 2), never classes.`,
      );
    }

    if (ts.isMethodSignature(node)) {
      const line = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
      const name = node.name.getText(sourceFile);
      violations.push(
        `${filePath}:${line}: method signature "${name}()" — components have zero methods (RULE 2). Move this logic to a System.`,
      );
    }

    if (ts.isPropertySignature(node) && node.type && ts.isFunctionTypeNode(node.type)) {
      const line = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
      const name = node.name.getText(sourceFile);
      violations.push(
        `${filePath}:${line}: field "${name}" is a function type — component fields must be JSON-serializable (RULE 1's snapshot requirement forbids functions, same as Set/Map).`,
      );
    }

    ts.forEachChild(node, visit);
  }

  visit(sourceFile);
  return violations;
}

async function main() {
  const args = process.argv.slice(2);
  const files =
    args.length > 0
      ? args.filter((f) => f.includes("/components/"))
      : await Array.fromAsync(new Bun.Glob(COMPONENTS_GLOB).scan("."));

  let allViolations: string[] = [];
  for (const file of files) {
    if (!file.endsWith(".ts")) continue;
    const source = readFileSync(file, "utf-8");
    allViolations = allViolations.concat(checkFile(file, source));
  }

  if (allViolations.length > 0) {
    for (const v of allViolations) console.error(v);
    process.exit(1);
  }
}

main();
