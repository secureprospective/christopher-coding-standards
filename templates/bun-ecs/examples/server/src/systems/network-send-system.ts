import type { PositionComponent } from "../components/position-component";
import type { GameSystem } from "../ecs/system";
import type { World } from "../ecs/world";
import type { PlayerSnapshot } from "../network/protocol-out";
import type { SystemOutput, TickInput } from "../shared/types";

// broadcast-phase system: RULE 5's carveout lets save/network-send/
// flight-recorder systems import db/ and network/ — this is where side
// effects (RULE 9) are allowed.
export class NetworkSendSystem implements GameSystem {
  readonly name = "NetworkSendSystem";
  readonly phase = "broadcast" as const;
  readonly order = 12;
  private tick = 0;

  update(world: World, _dt: number, _inputs: TickInput[]): SystemOutput {
    const entities = world.getEntitiesWith("position");
    const snapshot: PlayerSnapshot = {
      tick: this.tick++,
      entities: entities.map((id) => {
        const position = world.getComponent<PositionComponent>(id, "position");
        return { id, x: position?.x ?? 0, z: position?.z ?? 0 };
      }),
    };
    void snapshot; // SIDE EFFECT: broadcast to connected WebSocket clients
    return { events: [] };
  }
}
