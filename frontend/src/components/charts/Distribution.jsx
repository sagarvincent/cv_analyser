// Layer: 2 (chart composer) — maps tagged bars to DistributionBar; no geometry, no classification
import { buildDistributionGeometry } from '../../utils/distributionUtils';
import { DistributionBar } from './DistributionBar';

// -------------------- Distribution ----------- START ----------
// -- Calls : buildDistributionGeometry, DistributionBar
// -- Called by: PeerModule
export function Distribution({ buckets, you, p50, label, chartStyle = 'blocks' }) {
  const W = 560, H = 180;
  const padL = 16, padR = 16, padT = 18, padB = 30;
  const { bw, bars, youLabelX } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{ display: 'block' }}>
      {bars.map((bar) => (
        <DistributionBar key={bar.i} bar={bar} bw={bw} chartStyle={chartStyle} />
      ))}

      <text x={padL} y={H - 8} fontFamily="var(--font-mono)" fontSize="10" fill="var(--muted)">{label?.[0] || ''}</text>
      <text x={W - padR} y={H - 8} textAnchor="end" fontFamily="var(--font-mono)" fontSize="10" fill="var(--muted)">{label?.[1] || ''}</text>

      <g transform={`translate(${youLabelX}, ${padT - 6})`}>
        <text textAnchor="middle" fontFamily="var(--font-mono)" fontSize="9" fill="var(--accent)" letterSpacing="0.08em">YOU</text>
        <polygon points="0,2 -4,-3 4,-3" fill="var(--accent)" />
      </g>
    </svg>
  );
}
//-------------------- Distribution ------------- END ----------------
