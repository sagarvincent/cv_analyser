// Layer: 2 (chart sub-component) — pure rendering, no geometry calculation
import { buildRadarGeometry } from '../../utils/radarUtils';

// -------------------- Radar ----------- START ----------
// -- Calls : buildRadarGeometry
// -- Called by: AlignModule
export function Radar({ axes, you, target, size = 320 }) {
  const { cx, cy, youPath, targetPath, gridRings, axisLines, dots, labels } =
    buildRadarGeometry(axes, you, target, size);

  return (
    <svg width={size} height={size} style={{ display: 'block' }}>
      {gridRings.map(({ k, points }) => (
        <polygon key={k} points={points} fill="none" stroke="var(--border)" strokeWidth="0.5" />
      ))}
      {axisLines.map(({ x2, y2 }, i) => (
        <line key={i} x1={cx} y1={cy} x2={x2} y2={y2} stroke="var(--border)" strokeWidth="0.5" />
      ))}
      {targetPath && (
        <path d={targetPath} fill="var(--warn)" fillOpacity="0.06" stroke="var(--warn)" strokeWidth="1" strokeDasharray="3 3" />
      )}
      <path d={youPath} fill="var(--accent)" fillOpacity="0.18" stroke="var(--accent)" strokeWidth="1.5"
        style={{ filter: 'drop-shadow(0 0 6px var(--accent))' }} />
      {dots.map(({ x, y }, i) => (
        <circle key={i} cx={x} cy={y} r="2.5" fill="var(--accent)" />
      ))}
      {labels.map(({ x, y, text }, i) => (
        <text key={i} x={x} y={y + 4} textAnchor="middle"
          fontFamily="var(--font-mono)" fontSize="9.5" fill="var(--text-2)" letterSpacing="0.08em">
          {text}
        </text>
      ))}
    </svg>
  );
}
//-------------------- Radar ------------- END ----------------
