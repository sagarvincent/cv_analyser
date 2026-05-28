// Layer: 1 (module screen) — compensation benchmarking module
import { Card, SectionHeader } from '../ui';
import { CompBand } from '../charts';
import { CompRefCard } from './CompRefCard';
import { formatComp } from '../../utils/compBandUtils';
import { useAnalysis } from '../../context/AnalysisContext';

// -------------------- CompModule ----------- START ----------
// -- Calls : SectionHeader, Card, CompBand, CompRefCard, formatComp
// -- Called by: App (via MODULE_COMPONENTS)
export function CompModule() {
  const { compSummary = {}, compBandData = {}, compRefCards = [] } = useAnalysis();
  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={compSummary.eyebrow}
        title={
          <>You're underpaid by <span className="t-italic" style={{ color: 'var(--warn)' }}>{compSummary.titleUnderpaid}</span></>
        }
        sub={compSummary.sub}
      />

      <Card eyebrow="CURRENT VS MARKET" title={compSummary.bandTitle}>
        <CompBand {...compBandData} />
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18, color: 'var(--muted)', fontSize: 12 }}>
          <span>p25 · {formatComp(compBandData.p25, '$')}</span>
          <span style={{ color: 'var(--warn)' }}>YOU · {formatComp(compBandData.you, '$')} <span style={{ color: 'var(--muted)' }}>(8th percentile)</span></span>
          <span>p75 · {formatComp(compBandData.p75, '$')}</span>
        </div>
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, marginTop: 24 }}>
        {compRefCards.map((c) => (
          <CompRefCard key={c.label} card={c} />
        ))}
      </div>
    </div>
  );
}
//-------------------- CompModule ------------- END ----------------
