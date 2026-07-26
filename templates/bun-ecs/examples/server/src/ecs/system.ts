import type { SystemOutput, SystemPhase, TickInput } from "../shared/types";
import type { World } from "./world";

// RULE 3 (ECS_RULES.md): all logic lives in systems. A system never calls
// another system directly — game-loop.ts is the only orchestrator.
export interface GameSystem {
  readonly name: string;
  readonly phase: SystemPhase;
  readonly order: number;
  update(world: World, dt: number, inputs: TickInput[]): SystemOutput;
}
