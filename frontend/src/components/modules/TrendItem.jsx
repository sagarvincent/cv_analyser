// Layer: 2 (module sub-component) — one rising/falling trend row in TrendsModule
import { Spark } from '../ui';

// -------------------- TrendItem ----------- START ----------
// -- Calls : Spark
// -- Called by: TrendsModule
export function TrendItem({ trend, tone, isLast }) {
  const deltaColor = tone === 'good' ? 'var(--good)' : 'var(--bad)';
  return (
    <div style={{
      padding: '16px 0',
      borderBottom: isLast ? 'none' : '1px solid var(--border)',
      display: 'grid', gridTemplateColumns: '1fr auto 100px', gap: 18, alignItems: 'center',
    }}>
      <div>
        <div style={{ fontWeight: 500, marginBottom: 4 }}>{trend.topic}</div>
        <div style={{ color: 'var(--muted)', fontSize: 12 }}>{trend.note}</div>
      </div>
      <span className="t-num" style={{ fontSize: 22, color: deltaColor }}>{trend.delta}</span>
      <Spark data={trend.spark} width={100} height={36} tone={tone} />
    </div>
  );
}
//-------------------- TrendItem ------------- END ----------------
