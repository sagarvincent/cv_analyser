// Layer: 2 (module sub-component) — one big metric tile in OverviewModule
import { CountUp } from '../ui';
import { toneToColor } from '../../utils/colorUtils';
import { overviewCellBorders } from '../../utils/overviewUtils';

// -------------------- OverviewMetricCard ----------- START ----------
// -- Calls : CountUp, toneToColor, overviewCellBorders
// -- Called by: OverviewModule
export function OverviewMetricCard({ card, index, total, layout, onNav }) {
  const borders = overviewCellBorders(index, total, layout);
  return (
    <button onClick={() => onNav(card.id)} style={{
      padding: '22px 22px 24px',
      background: 'var(--surface)',
      border: 0,
      ...borders,
      textAlign: 'left', cursor: 'pointer', transition: '150ms ease', color: 'var(--text)',
    }}
      onMouseEnter={(e) => e.currentTarget.style.background = 'var(--surface-2)'}
      onMouseLeave={(e) => e.currentTarget.style.background = 'var(--surface)'}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <span className="t-label">{card.label}</span>
        <span style={{ color: 'var(--muted)', fontSize: 13 }}>→</span>
      </div>
      <div className="t-num" style={{
        fontSize: 56, lineHeight: 0.9, letterSpacing: '-0.02em',
        color: toneToColor(card.tone),
      }}>
        {typeof card.value === 'number' ? <CountUp to={card.value} /> : card.value}
        <span style={{ fontSize: 18, color: 'var(--muted)', marginLeft: 4 }}>{card.suffix}</span>
      </div>
      <div style={{ marginTop: 12, fontSize: 12.5, color: 'var(--text-2)' }}>{card.sub}</div>
    </button>
  );
}
//-------------------- OverviewMetricCard ------------- END ----------------
