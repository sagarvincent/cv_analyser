// Layer: Leaf — pure layout/formatting for OverviewModule. No JSX, no React.

// -------------------- overviewCellBorders ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: OverviewMetricCard
export function overviewCellBorders(i, total, layout) {
  const isList = layout === 'list';
  return {
    borderRight: !isList && (i % 3 !== 2) ? '1px solid var(--border)' : 'none',
    borderBottom: !isList && i < 3
      ? '1px solid var(--border)'
      : (isList && i < total - 1 ? '1px solid var(--border)' : 'none'),
  };
}
//-------------------- overviewCellBorders ------------- END ----------------
