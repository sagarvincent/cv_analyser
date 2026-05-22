// Layer: 2 (UI sub-component) — pure rendering
// -------------------- Insight ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: OverviewModule, AltPathsModule, TrendsModule
export function Insight({ text, source }) {
  return (
    <div style={{
      borderLeft: '1px solid var(--accent)', paddingLeft: 14,
      color: 'var(--text-2)', fontStyle: 'italic',
      fontFamily: 'var(--font-display)', fontSize: 18, lineHeight: 1.35,
    }}>
      "{text}"
      {source && <div className="t-label" style={{ marginTop: 8, fontStyle: 'normal' }}>{source}</div>}
    </div>
  );
}
//-------------------- Insight ------------- END ----------------
