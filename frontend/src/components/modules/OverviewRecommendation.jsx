// Layer: 2 (module sub-component) — one numbered recommendation in OverviewModule

// -------------------- OverviewRecommendation ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: OverviewModule
export function OverviewRecommendation({ rec }) {
  return (
    <div style={{ padding: '18px 0', borderBottom: '1px solid var(--border)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'baseline' }}>
        <span className="t-mono" style={{ color: 'var(--accent)', fontSize: 12, letterSpacing: '0.1em' }}>{rec.n} ·</span>
        <span className="pill pill-accent">{rec.tag}</span>
      </div>
      <div style={{ fontWeight: 500, fontSize: 16, marginBottom: 6 }}>{rec.title}</div>
      <div style={{ color: 'var(--text-2)', fontSize: 13, lineHeight: 1.55 }}>{rec.body}</div>
    </div>
  );
}
//-------------------- OverviewRecommendation ------------- END ----------------
