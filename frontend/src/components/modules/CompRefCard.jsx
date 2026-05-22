// Layer: 2 (module sub-component) — one reference card in CompModule (label, big value, sub)
import { toneToColor } from '../../utils/colorUtils';

// -------------------- CompRefCard ----------- START ----------
// -- Calls : toneToColor
// -- Called by: CompModule
export function CompRefCard({ card }) {
  return (
    <div className="card" style={{ padding: 24 }}>
      <div className="t-label" style={{ marginBottom: 14 }}>{card.label}</div>
      <div className="t-num" style={{ fontSize: 48, lineHeight: 1, color: toneToColor(card.tone) }}>
        {card.value}
      </div>
      <div style={{ marginTop: 12, fontSize: 13, color: 'var(--text-2)' }}>{card.sub}</div>
    </div>
  );
}
//-------------------- CompRefCard ------------- END ----------------
