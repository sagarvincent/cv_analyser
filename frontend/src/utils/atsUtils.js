// Layer: Leaf — pure aggregation for ATSModule. No JSX, no React.

// -------------------- countPassedChecks ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: ATSModule
export function countPassedChecks(checks) {
  return checks.filter(c => c.pass).length;
}
//-------------------- countPassedChecks ------------- END ----------------
