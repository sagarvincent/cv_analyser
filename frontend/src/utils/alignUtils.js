// Layer: Leaf — pure delta, tone, and formatting for AlignModule. No JSX, no React.

// -------------------- calcAlignDelta ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: buildAlignRows
export function calcAlignDelta(you, market) {
  return you - market;
}
//-------------------- calcAlignDelta ------------- END ----------------

// -------------------- alignDeltaTone ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: buildAlignRows
export function alignDeltaTone(delta) {
  return delta > 0.1 ? 'good' : delta < -0.1 ? 'bad' : 'muted';
}
//-------------------- alignDeltaTone ------------- END ----------------

// -------------------- formatAlignDelta ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: buildAlignRows
export function formatAlignDelta(delta) {
  return (delta > 0 ? '+' : '') + (delta * 100).toFixed(0);
}
//-------------------- formatAlignDelta ------------- END ----------------

// -------------------- buildAlignRows ----------- START ----------
// -- Calls : calcAlignDelta, alignDeltaTone, formatAlignDelta
// -- Called by: AlignModule
export function buildAlignRows(axes, you, market) {
  return axes.map((axis, i) => {
    const delta = calcAlignDelta(you[i], market[i]);
    const tone = alignDeltaTone(delta);
    return {
      axis,
      youValue: you[i],
      delta,
      tone,
      barTone: tone === 'muted' ? 'accent' : tone,
      deltaFmt: formatAlignDelta(delta),
      deltaColor: delta > 0 ? 'var(--good)' : 'var(--bad)',
    };
  });
}
//-------------------- buildAlignRows ------------- END ----------------
