import type { GameSystem } from "./ecs/system";
import { MovementSystem } from "./systems/movement-system";
import { NetworkSendSystem } from "./systems/network-send-system";

// RULE 4 (ECS_RULES.md): the pipeline is explicit and ordered. This is the
// ONLY file that imports all systems and the ONLY place execution order is
// decided. SYSTEM_ORDER.md mirrors this list — if you change one, change
// both.
export const SYSTEMS: GameSystem[] = [
  new MovementSystem(), // simulate, order 2
  new NetworkSendSystem(), // broadcast, order 12
];
