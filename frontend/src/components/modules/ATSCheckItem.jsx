// Layer: 2 (module sub-component) — one ATS check row (pass/fail icon, label, note, pill)

// -------------------- ATSCheckItem ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: ATSModule
export function ATSCheckItem({ check, isLast }) {
  const { pass, label, note } = check;
  const color = pass ? 'var(--good)' : 'var(--bad)';
  return (
    <div style={{
      padding: '14px 20px',
      display: 'grid', gridTemplateColumns: '20px 1fr auto', gap: 14,
      borderBottom: isLast ? 'none' : '1px solid var(--border)',
      alignItems: 'start',
    }}>
      <div style={{
        width: 18, height: 18, borderRadius: 99, marginTop: 2,
        background: color, opacity: 0.18,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: `1px solid ${color}`,
      }}>
        <span style={{ color, fontSize: 11 }}>{pass ? '✓' : '!'}</span>
      </div>
      <div>
        <div style={{ fontWeight: 500, marginBottom: 4 }}>{label}</div>
        <div style={{ color: 'var(--text-2)', fontSize: 12.5 }}>{note}</div>
      </div>
      <span className="t-mono" style={{ fontSize: 10.5, color, letterSpacing: '0.08em' }}>
        {pass ? 'PASS' : 'FIX'}
      </span>
    </div>
  );
}
//-------------------- ATSCheckItem ------------- END ----------------
