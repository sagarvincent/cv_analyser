// Layer: 2 (chart sub-component) — single cell (block or dot) inside SkillHeatmap
import { colorForSkill, calcDotRadius } from '../../utils/skillHeatmapUtils';

// -------------------- SkillHeatmapCell ----------- START ----------
// -- Calls : colorForSkill, calcDotRadius
// -- Called by: SkillHeatmap
export function SkillHeatmapCell({ v, cx, cy, cellW, cellH, chartStyle }) {
  const color = colorForSkill(v);

  if (chartStyle === 'dots') {
    const radius = calcDotRadius(v);
    return (
      <g>
        <circle cx={cx + cellW / 2} cy={cy + cellH / 2} r="14" fill="none" stroke="var(--border)" />
        {v != null && (
          <circle cx={cx + cellW / 2} cy={cy + cellH / 2} r={radius} fill={color}
            style={{ filter: v > 0.7 ? `drop-shadow(0 0 6px ${color})` : 'none' }} />
        )}
      </g>
    );
  }
  return (
    <g>
      <rect x={cx + 3} y={cy + 3} width={cellW - 6} height={cellH - 6}
        rx="2" fill={color} stroke="var(--border)"
        style={{ filter: v && v > 0.8 ? `drop-shadow(0 0 6px ${color})` : 'none' }} />
      {v != null && (
        <text x={cx + cellW / 2} y={cy + cellH / 2 + 4} textAnchor="middle"
          fontFamily="var(--font-mono)" fontSize="10"
          fill={v > 0.6 ? 'var(--ink)' : 'var(--text-2)'}
          style={{ fontFeatureSettings: "'tnum'" }}>
          {Math.round(v * 100)}
        </text>
      )}
    </g>
  );
}
//-------------------- SkillHeatmapCell ------------- END ----------------
