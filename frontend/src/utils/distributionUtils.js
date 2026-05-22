// Layer: Leaf — pure geometry and classification for Distribution chart. No JSX, no React.

// -------------------- distributionBarFill ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: buildDistributionGeometry
export function distributionBarFill(isYou, isP50) {
  return isYou ? 'var(--accent)' : isP50 ? 'var(--warn)' : 'var(--muted-2)';
}
//-------------------- distributionBarFill ------------- END ----------------

// -------------------- buildDistributionGeometry ----------- START ----------
// -- Calls : distributionBarFill
// -- Called by: Distribution
export function buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB) {
  const innerW = W - padL - padR;
  const innerH = H - padT - padB;
  const max = Math.max(...buckets);
  const bw = innerW / buckets.length;

  const bars = buckets.map((v, i) => {
    const h = (v / max) * innerH;
    const x = padL + i * bw;
    const y = padT + innerH - h;
    const cx = x + bw / 2;
    const isYou = i === you;
    const isP50 = i === p50;
    const fill = distributionBarFill(isYou, isP50);
    const dotCount = Math.max(1, Math.round(v / max * 8));
    const dotPositions = Array.from({ length: dotCount }, (_, di) => ({
      cx,
      cy: padT + innerH - (di + 0.5) * (innerH / 8),
    }));
    return { v, i, h, x, y, cx, isYou, isP50, fill, dotCount, dotPositions };
  });

  const youLabelX = padL + (you + 0.5) * bw;

  return { bw, bars, youLabelX };
}
//-------------------- buildDistributionGeometry ------------- END ----------------
