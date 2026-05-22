// Layer: 2 (module sub-component) — one evidence-match row in JDFitModule
import { Bar } from '../ui';
import { formatStrengthPct } from '../../utils/jdFitUtils';

// -------------------- JDFitMatchItem ----------- START ----------
// -- Calls : Bar, formatStrengthPct
// -- Called by: JDFitModule
export function JDFitMatchItem({ match, isLast }) {
  return (
    <div style={{ padding: '14px 0', borderBottom: isLast ? 'none' : '1px solid var(--border)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 8 }}>
        <span style={{ fontWeight: 500 }}>{match.topic}</span>
        <span className="t-mono" style={{ color: 'var(--good)', fontSize: 11 }}>{formatStrengthPct(match.strength)}%</span>
      </div>
      <div style={{ color: 'var(--muted)', fontSize: 12, marginBottom: 8, fontFamily: 'var(--font-mono)' }}>↳ "{match.evidence}"</div>
      <Bar value={match.strength * 100} tone="good" height={3} />
    </div>
  );
}
//-------------------- JDFitMatchItem ------------- END ----------------
