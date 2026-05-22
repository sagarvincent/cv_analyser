// Layer: Leaf — pure scaling and formatting for CompBand. No JSX, no React.

// -------------------- scaleCompValue ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CompBand
export function scaleCompValue(v, min, max, padL, innerW) {
  return padL + ((v - min) / (max - min)) * innerW;
}
//-------------------- scaleCompValue ------------- END ----------------

// -------------------- formatComp ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CompBand
export function formatComp(v, currency) {
  return `${currency}${(v / 1000).toFixed(0)}k`;
}
//-------------------- formatComp ------------- END ----------------
