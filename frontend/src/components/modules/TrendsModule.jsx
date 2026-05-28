// Layer: 1 (module screen) — market trends module
import { Card, Insight, SectionHeader } from '../ui';
import { TrendItem } from './TrendItem';
import { useAnalysis } from '../../context/AnalysisContext';

// -------------------- TrendsModule ----------- START ----------
// -- Calls : SectionHeader, Card, TrendItem, Insight
// -- Called by: App (via MODULE_COMPONENTS)
export function TrendsModule() {
  const { trendsSummary = {}, trendRising = [], trendFalling = [], trendsInsight = {} } = useAnalysis();
  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={trendsSummary.eyebrow}
        title={
          <>Your field is <span className="t-italic" style={{ color: 'var(--good)' }}>{trendsSummary.titleGrowing}</span>, but the centre of gravity is moving.</>
        }
        sub={trendsSummary.sub}
      />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <Card eyebrow="↑ RISING" title="What's pulling the field forward">
          {trendRising.map((r, i) => (
            <TrendItem key={r.topic} trend={r} tone="good" isLast={i === trendRising.length - 1} />
          ))}
        </Card>

        <Card eyebrow="↓ FALLING" title="What's contracting">
          {trendFalling.map((r, i) => (
            <TrendItem key={r.topic} trend={r} tone="bad" isLast={i === trendFalling.length - 1} />
          ))}
        </Card>
      </div>

      <div style={{ marginTop: 24 }}>
        <Insight text={trendsInsight.text} source={trendsInsight.source} />
      </div>
    </div>
  );
}
//-------------------- TrendsModule ------------- END ----------------
