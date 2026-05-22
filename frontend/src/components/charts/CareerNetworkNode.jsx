// Layer: 2 (chart sub-component) — single node (role) in the CareerNetwork graph
import { colorForFit, calcNodeRadius, formatFitPct } from '../../utils/careerNetworkUtils';

// -------------------- CareerNetworkNode ----------- START ----------
// -- Calls : colorForFit, calcNodeRadius, formatFitPct
// -- Called by: CareerNetwork
export function CareerNetworkNode({ node, chartStyle }) {
  const c = colorForFit(node.fit);
  const r = calcNodeRadius(node.fit, chartStyle);
  const glow = node.fit > 0.8 ? `drop-shadow(0 0 8px ${c})` : 'none';

  if (chartStyle === 'dots') {
    return (
      <g>
        <circle cx={node.x} cy={node.y} r={r} fill={c} opacity="0.18" />
        <circle cx={node.x} cy={node.y} r={r * 0.5} fill={c} style={{ filter: glow }} />
        <text x={node.x} y={node.y + r + 14} textAnchor="middle" fontFamily="var(--font-sans)" fontSize="11" fill="var(--text)">
          {node.title}
        </text>
        <text x={node.x} y={node.y + r + 28} textAnchor="middle" fontFamily="var(--font-mono)" fontSize="9" fill={c} letterSpacing="0.06em">
          {formatFitPct(node.fit)}% FIT
        </text>
      </g>
    );
  }
  return (
    <g>
      <rect x={node.x - 70} y={node.y - 22} width="140" height="44" rx="3"
        fill="var(--surface-2)" stroke={c} strokeWidth="1" style={{ filter: glow }} />
      <text x={node.x} y={node.y - 4} textAnchor="middle" fontFamily="var(--font-sans)" fontSize="11.5" fontWeight="500" fill="var(--text)">
        {node.title}
      </text>
      <text x={node.x} y={node.y + 12} textAnchor="middle" fontFamily="var(--font-mono)" fontSize="9" fill={c} letterSpacing="0.06em">
        {formatFitPct(node.fit)}% · {node.salary}
      </text>
    </g>
  );
}
//-------------------- CareerNetworkNode ------------- END ----------------
