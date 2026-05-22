// Layer: Leaf — pure tone-to-CSS-variable mapping. No JSX, no React.

// -------------------- toneToColor ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: Bar, Ring, Spark
export function toneToColor(tone) {
  if (tone === 'good')  return 'var(--good)';
  if (tone === 'warn')  return 'var(--warn)';
  if (tone === 'bad')   return 'var(--bad)';
  if (tone === 'muted') return 'var(--muted)';
  return 'var(--accent)';
}
//-------------------- toneToColor ------------- END ----------------
