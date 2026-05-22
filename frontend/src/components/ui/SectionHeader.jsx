// Layer: 2 (UI sub-component) — pure rendering
// -------------------- SectionHeader ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: OverviewModule, JDFitModule, ATSModule, PeerModule, SkillGapModule, AltPathsModule, CompModule, TrendsModule, AlignModule
export function SectionHeader({ eyebrow, title, sub }) {
  return (
    <div style={{ marginBottom: 24 }}>
      {eyebrow && <div className="t-eyebrow" style={{ marginBottom: 10, color: 'var(--accent)' }}>{eyebrow}</div>}
      <div className="t-display" style={{ fontSize: 42, lineHeight: 1.05, letterSpacing: '-0.02em' }}>{title}</div>
      {sub && <div style={{ marginTop: 12, color: 'var(--text-2)', maxWidth: 640, fontSize: 15 }}>{sub}</div>}
    </div>
  );
}
//-------------------- SectionHeader ------------- END ----------------
