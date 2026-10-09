import { expect, test } from "bun:test";
import { checkSource } from "./check-component-purity";
import { physicalLines } from "./check-file-length";

const path = "server/src/components/example.ts";

test("physical line inventory handles empty, terminated and partial lines", () => {
  expect(physicalLines("")).toBe(0);
  expect(physicalLines("one\n")).toBe(1);
  expect(physicalLines("one\ntwo")).toBe(2);
  expect(physicalLines("\n")).toBe(1);
  expect(physicalLines("a\r\n")).toBe(1);
  expect(physicalLines("x\n".repeat(311))).toBe(311);
});

test("narrow profile ignores harmless strings/comments and permits plain fields", () => {
  expect(
    checkSource(path, 'interface Position { x: number }; const note = "class"; // class'),
  ).toEqual([]);
});

test("narrow profile flags declaration, expression, method and direct callback", () => {
  for (const source of [
    "class Example {}",
    "const Example = class {};",
    "interface Example { move(): void }",
    "interface Example { callback: () => void }",
  ])
    expect(checkSource(path, source)).toHaveLength(1);
});

test("aliases and Set are outside this syntax profile, not falsely serializable", () => {
  expect(
    checkSource(
      path,
      "type Callback = () => void; interface Example { callback: Callback; ids: Set<string> }",
    ),
  ).toEqual([]);
});
