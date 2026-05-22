// Layer: Leaf — pure password scoring. No JSX, no React.

// -------------------- scorePassword ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: PwStrength
export function scorePassword(value) {
  if (!value) return 0;
  let score = 0;
  if (value.length >= 10) score++;
  if (value.length >= 14) score++;
  if (/[A-Z]/.test(value) && /[a-z]/.test(value)) score++;
  if (/\d/.test(value)) score++;
  if (/[^\w]/.test(value)) score++;
  return score;
}
//-------------------- scorePassword ------------- END ----------------
