import type { PositionComponent } from "../components/position-component";
import type { GameSystem } from "../ecs/system";
import type { World } from "../ecs/world";
import type { SystemOutput, TickInput } from "../shared/types";

// simulate-phase system: RULE 5 forbids reaching into db/ or network/ here.
export class MovementSystem implements GameSystem {
  readonly name = "MovementSystem";
  readonly phase = "simulate" as const;
  readonly order = 2;

  update(world: World, dt: number, inputs: TickInput[]): SystemOutput {
    for (const input of inputs) {
      if (input.type !== "MOVE") continue;
      const position = world.getComponent<PositionComponent>(input.entityId, "position");
      if (!position) continue;
      const targetX = input.x as number;
      const targetZ = input.z as number;
      const dx = targetX - position.x;
      const dz = targetZ - position.z;
      const distance = Math.hypot(dx, dz);
      if (distance < 0.01) continue;
      const speed = 4.5;
      const step = Math.min(1, (speed * dt) / distance);
      position.x += dx * step;
      position.z += dz * step;
    }
    return { events: [] };
  }
}
