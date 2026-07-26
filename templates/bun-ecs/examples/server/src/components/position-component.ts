import type { Component } from "../shared/types";

export interface PositionComponent extends Component {
  type: "position";
  x: number;
  z: number;
}
