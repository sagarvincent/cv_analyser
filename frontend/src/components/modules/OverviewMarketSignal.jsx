// Layer: 2 (module sub-component) — one live-market metric (count + spark + change) in OverviewModule
import { CountUp, Spark } from '../ui';

// -------------------- OverviewMarketSignal ----------- START ----------
// -- Calls : CountUp, Spark
// -- Called by: OverviewModule
export function OverviewMarketSignal({ label, count, trend, change, tone }) {
  const changeColor = tone === 'good' ? 'var(--good)' : tone === 'warn' ? 'var(--warn)' : 'var(--text-2)';
  return (
    <div>
      <div className="t-label" style={{ marginBottom: 8 }}>{label}</div>
      <div className="t-num" style={{ fontSize: 32, lineHeight: 1 }}><CountUp to={count} /></div>
      <div style={{ display: 'flex', gap: 8, marginTop: 6, alignItems: 'center', color: changeColor, fontSize: 12 }}>
        <Spark data={trend} width={70} height={20} tone={tone} />
        {change}
      </div>
    </div>
  );
}
//-------------------- OverviewMarketSignal ------------- END ----------------
