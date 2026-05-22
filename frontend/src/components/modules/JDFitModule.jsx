// Layer: 1 (module screen) — job description fit analysis module
import { Card, CountUp, Ring, SectionHeader } from '../ui';
import { JDFitMatchItem } from './JDFitMatchItem';
import { JDFitGapItem } from './JDFitGapItem';
import { jdFitSummary, jdFitMatches, jdFitGaps } from '../../data/mockData';

// -------------------- JDFitModule ----------- START ----------
// -- Calls : SectionHeader, Ring, CountUp, Card, JDFitMatchItem, JDFitGapItem
// -- Called by: App (via MODULE_COMPONENTS)
export function JDFitModule() {
  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={jdFitSummary.eyebrow}
        title={
          <>This role is <span className="t-italic" style={{ color: 'var(--warn)' }}>{jdFitSummary.titleReach}</span> {jdFitSummary.titleRest}</>
        }
        sub={jdFitSummary.sub}
      />

      {/* Top metric strip */}
      <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr 1fr 1fr', gap: 0, border: '1px solid var(--border)', borderRadius: 8, padding: 28, marginBottom: 28, background: 'var(--surface)' }}>
        <div style={{ paddingRight: 32, borderRight: '1px solid var(--border)' }}>
          <Ring value={jdFitSummary.score} size={150} label="OVERALL FIT" tone="warn" />
        </div>
        <div style={{ padding: '8px 24px', borderRight: '1px solid var(--border)' }}>
          <div className="t-label">EVIDENCED MATCHES</div>
          <div className="t-num" style={{ fontSize: 48, color: 'var(--good)', lineHeight: 1, marginTop: 8 }}><CountUp to={jdFitSummary.evidencedMatches} /></div>
          <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 6 }}>of {jdFitSummary.totalRequirements} JD requirements</div>
        </div>
        <div style={{ padding: '8px 24px', borderRight: '1px solid var(--border)' }}>
          <div className="t-label">GAPS FLAGGED</div>
          <div className="t-num" style={{ fontSize: 48, color: 'var(--warn)', lineHeight: 1, marginTop: 8 }}><CountUp to={jdFitSummary.gapsFlagged} /></div>
          <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 6 }}>{jdFitSummary.gapBreakdown}</div>
        </div>
        <div style={{ padding: '8px 24px' }}>
          <div className="t-label">KEYWORD DENSITY</div>
          <div className="t-num" style={{ fontSize: 48, color: 'var(--accent)', lineHeight: 1, marginTop: 8 }}>
            <CountUp to={jdFitSummary.keywordDensity} /><span style={{ fontSize: 18, color: 'var(--muted)' }}>%</span>
          </div>
          <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 6 }}>healthy · &gt;60% target</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <Card eyebrow="EVIDENCE STREAM" title="Where the CV lands">
          {jdFitMatches.map((m, i) => (
            <JDFitMatchItem key={i} match={m} isLast={i === jdFitMatches.length - 1} />
          ))}
        </Card>

        <Card eyebrow="GAPS" title="Where the CV stalls">
          {jdFitGaps.map((g, i) => (
            <JDFitGapItem key={i} gap={g} isLast={i === jdFitGaps.length - 1} />
          ))}
        </Card>
      </div>
    </div>
  );
}
//-------------------- JDFitModule ------------- END ----------------
