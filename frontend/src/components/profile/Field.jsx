// Layer: 2 (profile atom) — pure rendering
// -------------------- Field ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: ProfilePage
export function Field({ label, value, link }) {
  return (
    <div>
      <div className="t-label" style={{ marginBottom: 8 }}>{label}</div>
      <div style={{
        padding: '10px 12px',
        background: 'var(--ink-2)',
        border: '1px solid var(--border)',
        borderRadius: 4,
        fontSize: 14,
        color: link ? 'var(--accent)' : 'var(--text)',
        fontFamily: link ? 'var(--font-mono)' : 'var(--font-sans)',
      }}>{value}</div>
    </div>
  );
}
//-------------------- Field ------------- END ----------------
