// Layer: 2 (module sub-component) — one delta card in SkillGapModule (label, topic, delta, note)

// -------------------- SkillGapDeltaCard ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: SkillGapModule
export function SkillGapDeltaCard({ card }) {
  return (
    <div className="card" style={{ padding: 22 }}>
      <div className="t-label" style={{ marginBottom: 12 }}>{card.label}</div>
      <div style={{ fontSize: 22, fontWeight: 500, marginBottom: 6 }}>{card.topic}</div>
      <div className="t-num" style={{ fontSize: 40, color: card.color, lineHeight: 1, marginBottom: 14 }}>{card.delta}</div>
      <div style={{ color: 'var(--text-2)', fontSize: 13, lineHeight: 1.5 }}>{card.note}</div>
    </div>
  );
}
//-------------------- SkillGapDeltaCard ------------- END ----------------
