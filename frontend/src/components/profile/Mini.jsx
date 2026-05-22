// Layer: 2 (profile atom) — pure rendering
// -------------------- Mini ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: ProfilePage
export function Mini({ label, value }) {
  return (
    <div style={{ padding: 16, background: 'var(--ink-2)', border: '1px solid var(--border)', borderRadius: 4 }}>
      <div className="t-label" style={{ marginBottom: 8 }}>{label}</div>
      <div className="t-num" style={{ fontSize: 28, lineHeight: 1 }}>{value}</div>
    </div>
  );
}
//-------------------- Mini ------------- END ----------------
