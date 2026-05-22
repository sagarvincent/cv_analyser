// Layer: Leaf — pure geometry calculation for Spark sparkline. No JSX, no React.

// -------------------- buildSparklineGeometry ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: Spark
export function buildSparklineGeometry(data, width, height) {
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const pts = data
    .map((v, i) => `${(i / (data.length - 1)) * width},${height - ((v - min) / range) * height}`)
    .join(' ');

  const lastPtStr = pts.split(' ').slice(-1)[0];
  const [lastX, lastY] = lastPtStr.split(',').map(Number);

  return { pts, lastX, lastY };
}
//-------------------- buildSparklineGeometry ------------- END ----------------
