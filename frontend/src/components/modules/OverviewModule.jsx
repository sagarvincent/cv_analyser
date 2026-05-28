// Layer: 1 (module screen) — overview dashboard module
import { Card, Insight, SectionHeader } from '../ui';
import { OverviewMetricCard } from './OverviewMetricCard';
import { OverviewRecommendation } from './OverviewRecommendation';
import { OverviewMarketSignal } from './OverviewMarketSignal';
import { useAnalysis } from '../../context/AnalysisContext';

// -------------------- OverviewModule ----------- START ----------
// -- Calls : SectionHeader, Card, Insight, OverviewMetricCard, OverviewRecommendation, OverviewMarketSignal
// -- Called by: App (via MODULE_COMPONENTS)
export function OverviewModule({ layout, onNav }) {
  const {
    overviewCards = [], overviewSummary = {}, overviewRecommendations = [],
    overviewInsight = {}, overviewMarketData = {}, overviewVectorSignature = {},
  } = useAnalysis();
  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={overviewSummary.eyebrow}
        title={
          <>You're <span className="t-italic" style={{ color: 'var(--accent)' }}>{overviewSummary.titleStrong}</span><br />{overviewSummary.titleRest}</>
        }
        sub={overviewSummary.body}
      />

      {/* Big result cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: layout === 'list' ? '1fr' : 'repeat(3, 1fr)',
        gap: 0,
        border: '1px solid var(--border)',
        borderRadius: 8,
        overflow: 'hidden',
        marginBottom: 28,
      }}>
        {overviewCards.map((c, i) => (
          <OverviewMetricCard key={c.id} card={c} index={i} total={overviewCards.length} layout={layout} onNav={onNav} />
        ))}
      </div>

      {/* Two-column: recommendations + signals */}
      <div style={{ display: 'grid', gridTemplateColumns: layout === 'list' ? '1fr' : '1.4fr 1fr', gap: 20 }}>
        <Card eyebrow="THE THREE MOVES" title="Highest-leverage actions">
          {overviewRecommendations.map((r) => (
            <OverviewRecommendation key={r.n} rec={r} />
          ))}
          <div style={{ paddingTop: 18 }}>
            <Insight text={overviewInsight.text} source={overviewInsight.source} />
          </div>
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <Card eyebrow="LIVE MARKET" title="Today's signal">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              <OverviewMarketSignal
                label="OPEN ROLES"
                count={overviewMarketData.openRoles}
                trend={overviewMarketData.openRolesTrend}
                change={overviewMarketData.openRolesChange}
                tone="good"
              />
              <OverviewMarketSignal
                label="APPLICANT/ROLE"
                count={overviewMarketData.applicantsPerRole}
                trend={overviewMarketData.applicantsTrend}
                change={overviewMarketData.applicantsChange}
                tone="warn"
              />
            </div>
            <div className="hairline" style={{ margin: '20px 0' }} />
            <div style={{ fontSize: 13, color: 'var(--text-2)', lineHeight: 1.55 }}>
              {overviewMarketData.commentary}
            </div>
          </Card>

          <Card eyebrow="VECTOR FINGERPRINT" title="Career-space signature" pad={false}>
            <div style={{ padding: 14, background: 'var(--ink-2)' }}>
              <div className="t-mono" style={{ fontSize: 10.5, color: 'var(--muted)', lineHeight: 1.7, letterSpacing: '0.04em', wordBreak: 'break-all' }}>
                {overviewVectorSignature.model} ⏵<br />
                {overviewVectorSignature.preview}
              </div>
            </div>
            <div style={{ padding: '12px 16px', fontSize: 12, color: 'var(--muted)', borderTop: '1px solid var(--border)' }}>
              {overviewVectorSignature.dims} dims · cohort: <span style={{ color: 'var(--accent)' }}>{overviewVectorSignature.cohort}</span>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
//-------------------- OverviewModule ------------- END ----------------
