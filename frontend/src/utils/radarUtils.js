// Layer: Leaf — pure geometry calculation for the Radar chart. No JSX, no React.

// -------------------- calcRadarAngle ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: calcRadarPoint
export function calcRadarAngle(i, n) {
  return -Math.PI / 2 + (i / n) * Math.PI * 2;
}
//-------------------- calcRadarAngle ------------- END ----------------

// -------------------- calcRadarPoint ----------- START ----------
// -- Calls : calcRadarAngle
// -- Called by: buildRadarPath, buildRadarGeometry
export function calcRadarPoint(i, v, cx, cy, R, n) {
  const a = calcRadarAngle(i, n);
  return [cx + Math.cos(a) * R * v, cy + Math.sin(a) * R * v];
}
//-------------------- calcRadarPoint ------------- END ----------------

// -------------------- buildRadarPath ----------- START ----------
// -- Calls : calcRadarPoint
// -- Called by: buildRadarGeometry
export function buildRadarPath(values, cx, cy, R, n) {
  return 'M ' + values.map((v, i) => calcRadarPoint(i, v, cx, cy, R, n).join(',')).join(' L ') + ' Z';
}
//-------------------- buildRadarPath ------------- END ----------------

// -------------------- buildRadarGeometry ----------- START ----------
// -- Calls : buildRadarPath, calcRadarPoint
// -- Called by: Radar
export function buildRadarGeometry(axes, you, target, size) {
  const cx = size / 2, cy = size / 2;
  const R = size * 0.38;
  const n = axes.length;

  const youPath = buildRadarPath(you, cx, cy, R, n);
  const targetPath = target ? buildRadarPath(target, cx, cy, R, n) : null;

  const gridRings = [0.25, 0.5, 0.75, 1].map((k) => ({
    k,
    points: axes.map((_, i) => calcRadarPoint(i, k, cx, cy, R, n).join(',')).join(' '),
  }));

  const axisLines = axes.map((_, i) => {
    const [x2, y2] = calcRadarPoint(i, 1, cx, cy, R, n);
    return { x2, y2 };
  });

  const dots = you.map((v, i) => {
    const [x, y] = calcRadarPoint(i, v, cx, cy, R, n);
    return { x, y };
  });

  const labels = axes.map((a, i) => {
    const [x, y] = calcRadarPoint(i, 1.15, cx, cy, R, n);
    return { x, y, text: a.toUpperCase() };
  });

  return { cx, cy, youPath, targetPath, gridRings, axisLines, dots, labels };
}
//-------------------- buildRadarGeometry ------------- END ----------------
