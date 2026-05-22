// Layer: Leaf — pure formatting and tone mapping for JDFitModule. No JSX, no React.

// -------------------- formatStrengthPct ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: JDFitModule
export function formatStrengthPct(strength) {
  return Math.round(strength * 100);
}
//-------------------- formatStrengthPct ------------- END ----------------

// -------------------- impactTone ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: JDFitModule
export function impactTone(impact) {
  return impact === 'HIGH' ? 'bad' : impact === 'MED' ? 'warn' : 'muted';
}
//-------------------- impactTone ------------- END ----------------
