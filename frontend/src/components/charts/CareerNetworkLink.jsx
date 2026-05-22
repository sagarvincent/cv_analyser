// Layer: 2 (chart sub-component) — single connection line in the CareerNetwork graph
import { colorForFit, calcLinkStrokeWidth } from '../../utils/careerNetworkUtils';

// -------------------- CareerNetworkLink ----------- START ----------
// -- Calls : colorForFit, calcLinkStrokeWidth
// -- Called by: CareerNetwork
export function CareerNetworkLink({ a, b, fit }) {
  return (
    <line x1={a.x} y1={a.y} x2={b.x} y2={b.y}
      stroke={colorForFit(fit ?? 0.6)}
      strokeWidth={calcLinkStrokeWidth(fit)}
      strokeOpacity={0.5} />
  );
}
//-------------------- CareerNetworkLink ------------- END ----------------
