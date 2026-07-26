export type EntityId = string;

export type ComponentType = "position" | "health" | "stats" | "controllable" | "combat-target";

// RULE 2 (ECS_RULES.md): every Component is plain data with a `type`
// discriminator and JSON-serializable fields only — no Set/Map/class
// instances, no methods. Required so World.exportSnapshot() can produce a
// plain JSON tree with no special-casing per component.
export interface Component {
  type: ComponentType;
}

export type SystemPhase = "collect" | "simulate" | "broadcast";

export interface GameEvent {
  type: string;
  [key: string]: unknown;
}

export interface SystemOutput {
  events: GameEvent[];
}

export interface TickInput {
  type: string;
  entityId: EntityId;
  [key: string]: unknown;
}
