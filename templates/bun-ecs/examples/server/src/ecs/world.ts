import type { Component, ComponentType, EntityId } from "../shared/types";

export type Snapshot = Record<EntityId, Record<ComponentType, Component>>;

// RULE 1 (ECS_RULES.md): the entity is a UUID and nothing more. This class
// is the ONLY place entities live — no Entity class, no inheritance.
export class World {
  private entities = new Map<EntityId, Map<ComponentType, Component>>();

  createEntity(): EntityId {
    const id = crypto.randomUUID();
    this.entities.set(id, new Map());
    return id;
  }

  removeEntity(id: EntityId): void {
    this.entities.delete(id);
  }

  addComponent(id: EntityId, component: Component): void {
    this.entities.get(id)?.set(component.type, component);
  }

  removeComponent(id: EntityId, type: ComponentType): void {
    this.entities.get(id)?.delete(type);
  }

  getComponent<T extends Component>(id: EntityId, type: ComponentType): T | undefined {
    return this.entities.get(id)?.get(type) as T | undefined;
  }

  getEntitiesWith(...types: ComponentType[]): EntityId[] {
    const result: EntityId[] = [];
    for (const [id, components] of this.entities) {
      if (types.every((type) => components.has(type))) result.push(id);
    }
    return result;
  }

  // LOCKED (architecture panel gate, 2026-07-26 shadowbane decision): mandatory
  // from Phase 0. Produces/rehydrates a plain JSON tree — no Set/Map/class
  // instances leak through. Cheapest seam a future distributed rewrite hangs
  // actor rehydration on.
  exportSnapshot(): Snapshot {
    const snapshot: Snapshot = {};
    for (const [id, components] of this.entities) {
      snapshot[id] = Object.fromEntries(components) as Record<ComponentType, Component>;
    }
    return snapshot;
  }

  importSnapshot(snapshot: Snapshot): void {
    this.entities.clear();
    for (const [id, components] of Object.entries(snapshot)) {
      this.entities.set(id, new Map(Object.entries(components) as [ComponentType, Component][]));
    }
  }
}
