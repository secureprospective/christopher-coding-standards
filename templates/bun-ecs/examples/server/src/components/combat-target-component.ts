import type { Component } from "../shared/types";

export interface CombatTargetComponent extends Component {
  type: "combat-target";
  attackerId: string;
}
