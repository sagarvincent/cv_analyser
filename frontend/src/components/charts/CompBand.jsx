// Layer: 2 (chart sub-component) — pure rendering, scaling and formatting delegated to utils
import { scaleCompValue, formatComp } from '../../utils/compBandUtils';

// -------------------- CompBand ----------- START ----------
// -- Calls : scaleCompValue, formatComp
// -- Called by: CompModule
export function CompBand({ min, p25, p50, p75, max, you, currency = '$' }) {
  const W = 560, H = 110;
  const padL = 60, padR = 60, padT = 30;
  const innerW = W - padL - padR;
  const scale = (v) => scaleCompValue(v, min, max, padL, innerW);
  const fmt = (v) => formatComp(v, currency);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{ display: 'block' }}>
      <rect x={padL} y={padT + 18} width={innerW} height="14" rx="2" fill="var(--surface-3)" />
      <rect x={scale(p25)} y={padT + 18} width={scale(p75) - scale(p25)} height="14" rx="2" fill="var(--accent)" opacity="0.35" />
      <line x1={scale(p50)} y1={padT + 12} x2={scale(p50)} y2={padT + 38} stroke="var(--accent)" strokeWidth="1.5" />
      <text x={scale(p50)} y={padT + 6} textAnchor="middle" fontFamily="var(--font-mono)" fontSize="10" fill="var(--accent)" letterSpacing="0.06em">
        P50 · {fmt(p50)}
      </text>
      <g transform={`translate(${scale(you)}, ${padT + 25})`}>
        <circle r="6" fill="var(--accent)" style={{ filter: 'drop-shadow(0 0 8px var(--accent))' }} />
        <circle r="3" fill="var(--ink)" />
      </g>
      <g transform={`translate(${scale(you)}, ${padT + 56})`}>
        <text textAnchor="middle" fontFamily="var(--font-mono)" fontSize="9" fill="var(--text-2)" letterSpacing="0.08em">YOU</text>
        <text y="14" textAnchor="middle" fontFamily="var(--font-mono)" fontSize="11" fill="var(--text)">{fmt(you)}</text>
      </g>
      <text x={padL - 8} y={padT + 28} textAnchor="end" fontFamily="var(--font-mono)" fontSize="10" fill="var(--muted)">{fmt(min)}</text>
      <text x={padL + innerW + 8} y={padT + 28} fontFamily="var(--font-mono)" fontSize="10" fill="var(--muted)">{fmt(max)}</text>
    </svg>
  );
}
//-------------------- CompBand ------------- END ----------------
