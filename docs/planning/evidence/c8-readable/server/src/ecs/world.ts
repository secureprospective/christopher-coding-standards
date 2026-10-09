import type { Component, ComponentType, EntityId } from "../shared/types";

export type Snapshot = Record<EntityId, Record<ComponentType, Component>>;

// Optional example: UUID entities and typed component lookup. Values supplied
// here are trusted; the generic cast does not runtime-check component identity.
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

  // Shallow snapshot of trusted component values; references remain shared.
  // Plain example values round-trip through JSON, but this is not arbitrary
  // JSON validation, immutable point-in-time state or replay/distribution proof.
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
