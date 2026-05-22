// Layer: 2 (chart composer) — maps cells/headers/labels to sub-components; no inline geometry
import { calcCellPosition } from '../../utils/skillHeatmapUtils';
import { SkillHeatmapCell } from './SkillHeatmapCell';

// -------------------- SkillHeatmap ----------- START ----------
// -- Calls : calcCellPosition, SkillHeatmapCell
// -- Called by: SkillGapModule
export function SkillHeatmap({ rows, cols, data, chartStyle = 'blocks' }) {
  const cellW = 56, cellH = 36, labelW = 140, headerH = 64;
  const W = labelW + cols.length * cellW + 24;
  const H = headerH + rows.length * cellH + 16;

  return (
    <div style={{ overflowX: 'auto' }} className="scroll-clean">
      <svg width={W} height={H} style={{ display: 'block' }}>
        {cols.map((c, i) => (
          <g key={c} transform={`translate(${labelW + i * cellW + cellW / 2}, ${headerH - 8}) rotate(-32)`}>
            <text fontFamily="var(--font-mono)" fontSize="10.5" fill="var(--text-2)" textAnchor="start" letterSpacing="0.06em">
              {c.toUpperCase()}
            </text>
          </g>
        ))}
        {rows.map((r, ri) => (
          <g key={r}>
            <text x={labelW - 12} y={headerH + ri * cellH + cellH / 2 + 4}
              textAnchor="end" fontFamily="var(--font-sans)" fontSize="12" fill="var(--text-2)">
              {r}
            </text>
            {cols.map((c, ci) => {
              const v = data[ri]?.[ci];
              const { cx, cy } = calcCellPosition(ri, ci, labelW, headerH, cellW, cellH);
              return (
                <SkillHeatmapCell key={c} v={v} cx={cx} cy={cy} cellW={cellW} cellH={cellH} chartStyle={chartStyle} />
              );
            })}
          </g>
        ))}
      </svg>
    </div>
  );
}
//-------------------- SkillHeatmap ------------- END ----------------
