// Layer: Leaf — pure color and geometry for SkillHeatmap. No JSX, no React.

// -------------------- colorForSkill ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: SkillHeatmap
export function colorForSkill(v) {
  if (v == null) return 'var(--surface-3)';
  if (v < 0.25) return `oklch(0.30 0.04 25 / ${0.4 + v})`;
  if (v < 0.55) return `oklch(0.55 0.12 75 / ${0.55 + v * 0.45})`;
  if (v < 0.75) return `oklch(0.74 0.13 155 / ${0.65 + v * 0.35})`;
  return `oklch(0.85 0.14 195 / ${0.85 + v * 0.15})`;
}
//-------------------- colorForSkill ------------- END ----------------

// -------------------- calcCellPosition ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: SkillHeatmap
export function calcCellPosition(ri, ci, labelW, headerH, cellW, cellH) {
  return { cx: labelW + ci * cellW, cy: headerH + ri * cellH };
}
//-------------------- calcCellPosition ------------- END ----------------

// -------------------- calcDotRadius ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: SkillHeatmap
export function calcDotRadius(v) {
  return v == null ? 0 : 4 + v * 10;
}
//-------------------- calcDotRadius ------------- END ----------------
