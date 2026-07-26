import type { Component } from "../shared/types";

export interface StatsComponent extends Component {
  type: "stats";
  strength: number;
  dexterity: number;
  constitution: number;
}
