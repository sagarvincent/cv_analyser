// Layer: 1 (layout) — pure rendering of the top navigation bar
// -------------------- TopBar ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: Dashboard
export function TopBar({ profile, active, showProfile }) {
  return (
    <div style={{
      borderBottom: '1px solid var(--border)',
      padding: '14px 48px',
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      background: 'var(--ink-2)',
      position: 'sticky', top: 0, zIndex: 10,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14, fontSize: 12, fontFamily: 'var(--font-mono)', color: 'var(--muted)', letterSpacing: '0.08em' }}>
        <span>STRATA</span>
        <span>›</span>
        <span>{profile?.cv?.name?.toUpperCase() || 'ARIA CHEN'}</span>
        <span>›</span>
        <span style={{ color: 'var(--accent)' }}>
          {showProfile ? 'PROFILE' : (active?.label?.toUpperCase() || 'OVERVIEW')}
        </span>
      </div>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <span className="pill pill-accent pill-dot">JD LOADED · DIRECTOR PD</span>
        <button className="btn">SHARE BRIEF</button>
        <button className="btn">⇣ EXPORT PDF</button>
      </div>
    </div>
  );
}
//-------------------- TopBar ------------- END ----------------
