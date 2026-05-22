// Layer: 2 (chart composer) — maps placed nodes and links to sub-components; no inline logic
import { useMemo } from 'react';
import { buildCareerNetworkLayout, resolveLinkEndpoints } from '../../utils/careerNetworkUtils';
import { CareerNetworkLink } from './CareerNetworkLink';
import { CareerNetworkNode } from './CareerNetworkNode';

// -------------------- CareerNetwork ----------- START ----------
// -- Calls : buildCareerNetworkLayout, resolveLinkEndpoints, CareerNetworkLink, CareerNetworkNode
// -- Called by: AltPathsModule
export function CareerNetwork({ center, nodes, links, chartStyle = 'blocks' }) {
  const W = 720, H = 460;
  const { placed, cx, cy, ring1R, ring2R } = useMemo(
    () => buildCareerNetworkLayout(nodes, W, H),
    [nodes]
  );

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{ display: 'block', maxWidth: W }}>
      <defs>
        <radialGradient id="centerGlow" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.35" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
        </radialGradient>
      </defs>

      <circle cx={cx} cy={cy} r={ring1R} fill="none" stroke="var(--border)" strokeDasharray="2 6" />
      <circle cx={cx} cy={cy} r={ring2R} fill="none" stroke="var(--border)" strokeDasharray="2 6" />

      {links.map((l, i) => {
        const { a, b } = resolveLinkEndpoints(l, placed, cx, cy);
        return <CareerNetworkLink key={i} a={a} b={b} fit={l.fit} />;
      })}

      <circle cx={cx} cy={cy} r="60" fill="url(#centerGlow)" />
      <circle cx={cx} cy={cy} r="34" fill="var(--surface-2)" stroke="var(--accent)" strokeWidth="1.5"
        style={{ filter: 'drop-shadow(0 0 12px var(--accent))' }} />
      <text x={cx} y={cy - 2} textAnchor="middle" fontFamily="var(--font-mono)" fontSize="9" fill="var(--accent)" letterSpacing="0.12em">
        CURRENT
      </text>
      <text x={cx} y={cy + 12} textAnchor="middle" fontFamily="var(--font-sans)" fontSize="11" fontWeight="500" fill="var(--text)">
        {center.title}
      </text>

      {placed.map((n) => (
        <CareerNetworkNode key={n.id} node={n} chartStyle={chartStyle} />
      ))}
    </svg>
  );
}
//-------------------- CareerNetwork ------------- END ----------------
