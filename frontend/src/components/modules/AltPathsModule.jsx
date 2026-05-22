// Layer: 1 (module screen) — alternative career paths module
import { Card, Insight, SectionHeader } from '../ui';
import { CareerNetwork } from '../charts';
import { altPathsSummary, altPathsCenter, altPathsNodes, altPathsLinks, altPathsInsight } from '../../data/mockData';

// -------------------- AltPathsModule ----------- START ----------
// -- Calls : SectionHeader, Card, CareerNetwork, Insight
// -- Called by: App (via MODULE_COMPONENTS)
export function AltPathsModule({ chartStyle }) {
  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={altPathsSummary.eyebrow}
        title={
          <>The Director path is <span className="t-italic" style={{ color: 'var(--warn)' }}>{altPathsSummary.titleWarn}</span>{altPathsSummary.titleRest}</>
        }
        sub={altPathsSummary.sub}
      />

      <Card pad={false}>
        <div style={{ padding: 20 }}>
          <CareerNetwork center={altPathsCenter} nodes={altPathsNodes} links={altPathsLinks} chartStyle={chartStyle} />
        </div>
        <div style={{ borderTop: '1px solid var(--border)', padding: '14px 24px', display: 'flex', gap: 22, fontSize: 11, color: 'var(--muted)', fontFamily: 'var(--font-mono)' }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}><span style={{ width: 8, height: 8, borderRadius: 99, background: 'var(--accent)' }} />FIT &gt; 85</span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}><span style={{ width: 8, height: 8, borderRadius: 99, background: 'var(--good)' }} />FIT 70–85</span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}><span style={{ width: 8, height: 8, borderRadius: 99, background: 'var(--warn)' }} />FIT 55–70</span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}><span style={{ width: 8, height: 8, borderRadius: 99, background: 'var(--muted)' }} />FIT &lt; 55</span>
        </div>
      </Card>

      <div style={{ marginTop: 24 }}>
        <Insight text={altPathsInsight.text} source={altPathsInsight.source} />
      </div>
    </div>
  );
}
//-------------------- AltPathsModule ------------- END ----------------
