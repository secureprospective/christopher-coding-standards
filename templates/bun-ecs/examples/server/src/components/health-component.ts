import type { Component } from "../shared/types";

export interface HealthComponent extends Component {
  type: "health";
  current: number;
  max: number;
}
