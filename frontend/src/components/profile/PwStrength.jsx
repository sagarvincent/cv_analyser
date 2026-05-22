// Layer: 2 (profile atom) — pure rendering, scoring delegated to passwordUtils
import { scorePassword } from '../../utils/passwordUtils';

// -------------------- PwStrength ----------- START ----------
// -- Calls : scorePassword
// -- Called by: ProfilePage
export function PwStrength({ value }) {
  if (!value) return null;
  const score = scorePassword(value);
  const tones  = ['bad', 'bad', 'warn', 'warn', 'good', 'good'];
  const labels = ['VERY WEAK', 'WEAK', 'OK', 'STRONG', 'VERY STRONG', 'EXCEPTIONAL'];
  return (
    <div>
      <div style={{ display: 'flex', gap: 4, marginBottom: 6 }}>
        {[0, 1, 2, 3, 4].map(i => (
          <div key={i} style={{
            flex: 1, height: 3, borderRadius: 1,
            background: i < score ? `var(--${tones[score]})` : 'var(--surface-3)',
            transition: '200ms',
          }} />
        ))}
      </div>
      <div className="t-mono" style={{ fontSize: 10.5, color: `var(--${tones[score]})`, letterSpacing: '0.08em' }}>
        {labels[score]}
      </div>
    </div>
  );
}
//-------------------- PwStrength ------------- END ----------------
