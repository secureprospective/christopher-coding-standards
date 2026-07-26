export interface PlayerSnapshot {
  entities: { id: string; x: number; z: number }[];
  tick: number;
}
