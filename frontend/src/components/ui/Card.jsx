// Layer: 2 (UI sub-component) — pure rendering
// -------------------- Card ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: OverviewModule, JDFitModule, SkillGapModule, AltPathsModule, PeerModule, CompModule, TrendsModule, AlignModule, ProfilePage
export function Card({ title, eyebrow, badge, action, children, pad = true, className = '', style }) {
  return (
    <div className={`card ${className}`} style={style}>
      {(title || eyebrow || badge || action) && (
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '14px 18px', borderBottom: '1px solid var(--border)', gap: 12,
        }}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, minWidth: 0 }}>
            {eyebrow && <span className="t-label">{eyebrow}</span>}
            {title && <span style={{ fontSize: 14, fontWeight: 500, letterSpacing: '-0.01em' }}>{title}</span>}
            {badge}
          </div>
          {action}
        </div>
      )}
      <div style={{ padding: pad ? 'var(--pad)' : 0 }}>
        {children}
      </div>
    </div>
  );
}
//-------------------- Card ------------- END ----------------
