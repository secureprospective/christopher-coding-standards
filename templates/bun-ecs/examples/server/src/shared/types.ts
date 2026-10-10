export type EntityId = string;

export type ComponentType = "position" | "health" | "stats" | "controllable" | "combat-target";

// The example components use plain fields. This structural base type does not
// guarantee arbitrary values are JSON-serializable or free of methods/Set/Map.
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
