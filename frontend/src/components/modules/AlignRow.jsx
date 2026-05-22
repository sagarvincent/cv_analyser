// Layer: 2 (module sub-component) — one alignment row (label + bar + delta) in AlignModule
import { Bar } from '../ui';

// -------------------- AlignRow ----------- START ----------
// -- Calls : Bar
// -- Called by: AlignModule
export function AlignRow({ row }) {
  const { axis, youValue, barTone, deltaFmt, deltaColor } = row;
  return (
    <div className="card" style={{ padding: 18, display: 'grid', gridTemplateColumns: '120px 1fr auto', gap: 18, alignItems: 'center' }}>
      <span className="t-label">{axis}</span>
      <div>
        <Bar value={youValue * 100} tone={barTone} height={3} />
      </div>
      <span className="t-mono" style={{ fontSize: 14, color: deltaColor }}>
        {deltaFmt}
      </span>
    </div>
  );
}
//-------------------- AlignRow ------------- END ----------------
