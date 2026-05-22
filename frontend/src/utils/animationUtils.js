// Layer: Leaf — pure animation and geometry math. No JSX, no React.

// -------------------- cubicEaseOut ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CountUp, Ring
export function cubicEaseOut(t) {
  return 1 - Math.pow(1 - t, 3);
}
//-------------------- cubicEaseOut ------------- END ----------------

// -------------------- springStep ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: AnalysisScreen
export function springStep(current, target, factor) {
  return current + (target - current) * factor;
}
//-------------------- springStep ------------- END ----------------

// -------------------- calcRingGeometry ----------- START ----------
// -- Calls : clampNorm
// -- Called by: Ring
export function calcRingGeometry(value, max, size) {
  const pct = clampNorm(value, max);
  const r = size / 2 - 6;
  const c = 2 * Math.PI * r;
  return { pct, r, c };
}
//-------------------- calcRingGeometry ------------- END ----------------

// -------------------- clampNorm ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: calcRingGeometry, Bar
export function clampNorm(value, max) {
  return Math.max(0, Math.min(1, value / max));
}
//-------------------- clampNorm ------------- END ----------------

// -------------------- calcStepDuration ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: AnalysisScreen
export function calcStepDuration() {
  return 350 + Math.random() * 300;
}
//-------------------- calcStepDuration ------------- END ----------------

// -------------------- generateTraceId ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: AnalysisScreen
export function generateTraceId() {
  return Math.random() * 0xfffff | 0;
}
//-------------------- generateTraceId ------------- END ----------------
