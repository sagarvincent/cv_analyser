// Layer: 2 (UI sub-component) — pure rendering, no geometry calculation
import { buildSparklineGeometry } from '../../utils/sparklineUtils';
import { toneToColor } from '../../utils/colorUtils';

// -------------------- Spark ----------- START ----------
// -- Calls : buildSparklineGeometry, toneToColor
// -- Called by: OverviewModule, TrendsModule
export function Spark({ data, width = 120, height = 32, tone = 'accent' }) {
  if (!data || data.length < 2) return <svg width={width} height={height} style={{ display: 'block' }} />;
  const { pts, lastX, lastY } = buildSparklineGeometry(data, width, height);
  const color = toneToColor(tone);

  return (
    <svg width={width} height={height} style={{ display: 'block' }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth="1.5" />
      <circle cx={lastX} cy={lastY} r="2.5" fill={color} />
    </svg>
  );
}
//-------------------- Spark ------------- END ----------------
