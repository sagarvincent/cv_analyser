// Layer: 2 (chart sub-component) — renders a single bar/dot-stack within a Distribution

// -------------------- DistributionBar ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: Distribution
export function DistributionBar({ bar, bw, chartStyle }) {
  const { h, x, y, isYou, fill, dotPositions } = bar;

  if (chartStyle === 'dots') {
    return (
      <g>
        {dotPositions.map(({ cx: dcx, cy }, di) => (
          <circle key={di} cx={dcx} cy={cy} r={isYou ? 4 : 3} fill={fill}
            style={{ filter: isYou ? `drop-shadow(0 0 4px ${fill})` : 'none' }} />
        ))}
      </g>
    );
  }
  return (
    <rect x={x + 2} y={y} width={bw - 4} height={h}
      fill={fill} opacity={isYou ? 1 : 0.6}
      style={{ filter: isYou ? 'drop-shadow(0 0 8px var(--accent))' : 'none' }} />
  );
}
//-------------------- DistributionBar ------------- END ----------------
