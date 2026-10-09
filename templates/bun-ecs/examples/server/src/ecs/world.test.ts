import { expect, test } from "bun:test";
import type { PositionComponent } from "../components/position-component";
import { ClientMessageSchema } from "../shared/protocol";
import { MovementSystem } from "../systems/movement-system";
import { NetworkSendSystem } from "../systems/network-send-system";
import { type Snapshot, World } from "./world";

function setup() {
  const world = new World();
  const id = world.createEntity();
  const position: PositionComponent = { type: "position", x: 0, z: 0 };
  world.addComponent(id, position);
  return { world, id, position };
}

test("actual valid command parsing precedes actual movement effect", () => {
  const { world, id, position } = setup();
  const result = ClientMessageSchema.safeParse({ type: "MOVE", entityId: id, x: 9, z: 0 });
  expect(result.success).toBe(true);
  if (!result.success) throw new Error("expected valid fixture command");
  new MovementSystem().update(world, 1, [result.data]);
  expect(position.x).toBe(4.5);
  expect(position.z).toBe(0);
});

test("synthetic boundary caller rejects before effect and preserves state", () => {
  const { world, id, position } = setup();
  for (const x of ["bad", Number.NaN, Number.POSITIVE_INFINITY]) {
    const result = ClientMessageSchema.safeParse({ type: "MOVE", entityId: id, x, z: 0 });
    if (result.success) new MovementSystem().update(world, 1, [result.data]);
    expect(result.success).toBe(false);
    expect(position).toEqual({ type: "position", x: 0, z: 0 });
  }
});

test("actual movement also ignores malformed coordinates if parsing is bypassed", () => {
  const { world, id, position } = setup();
  new MovementSystem().update(world, 1, [
    { type: "MOVE", entityId: id, x: "bad", z: 0 },
    { type: "MOVE", entityId: id, x: Number.NaN, z: 0 },
  ]);
  expect(position).toEqual({ type: "position", x: 0, z: 0 });
});

test("reference schema strips unknown fields without granting ownership", () => {
  const { id } = setup();
  const parsed = ClientMessageSchema.parse({ type: "MOVE", entityId: id, x: 1, z: 2, extra: true });
  expect(parsed).toEqual({ type: "MOVE", entityId: id, x: 1, z: 2 });
  expect(
    ClientMessageSchema.safeParse({ type: "ATTACK", entityId: id, targetId: "bad" }).success,
  ).toBe(false);
});

test("snapshot export/import intentionally aliases trusted component references", () => {
  const { world, id, position } = setup();
  const snapshot = world.exportSnapshot();
  expect(snapshot[id]?.position).toBe(position);
  position.x = 7;
  const other = new World();
  other.importSnapshot(snapshot);
  expect(other.getComponent<PositionComponent>(id, "position")).toBe(position);
  const encoded = JSON.stringify(snapshot);
  expect(encoded).toContain('"x":7');
  const decoded: Snapshot = JSON.parse(encoded);
  const hydrated = new World();
  hydrated.importSnapshot(decoded);
  expect(hydrated.getComponent<PositionComponent>(id, "position")).toEqual(position);
  expect(hydrated.getComponent<PositionComponent>(id, "position")).not.toBe(position);
  world.removeEntity(id);
  expect(world.getEntitiesWith("position")).toEqual([]);
  expect(other.getEntitiesWith("position")).toEqual([id]);
});

test("unknown entity remains a no-op; network example has no broadcast effect", () => {
  const world = new World();
  world.addComponent("unknown", { type: "position" });
  expect(world.getEntitiesWith("position")).toEqual([]);
  expect(new NetworkSendSystem().update(world, 0, [])).toEqual({ events: [] });
});
