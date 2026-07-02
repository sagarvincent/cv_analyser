// Layer: 1 (module screen) — Skill Matrix module (BES04: bucket → JD categories → score)
import { Card, SectionHeader } from '../ui';
import { SkillHeatmap } from '../charts';
import { SkillGapDeltaCard } from './SkillGapDeltaCard';
import { useAnalysis } from '../../context/AnalysisContext';

// -------------------- SkillGapModule ----------- START ----------
// -- Calls : SectionHeader, Card, SkillHeatmap, SkillGapDeltaCard
// -- Called by: App (via MODULE_COMPONENTS)
export function SkillGapModule({ chartStyle }) {
  const {
    skillMatrixSummary = {}, skillMatrixCategories = [], skillMatrixCohorts = [],
    skillMatrixData = [], skillMatrixDeltaCards = [],
  } = useAnalysis();
  const eyebrow = skillMatrixSummary.bucket
    ? `${skillMatrixSummary.eyebrow} · profile = ${skillMatrixSummary.bucket}`
    : skillMatrixSummary.eyebrow;
  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={eyebrow}
        title={
          <>Strongest against the JD on <span className="t-italic" style={{ color: 'var(--accent)' }}>{skillMatrixSummary.overIndexTopic}</span>.<br />Biggest gap on <span className="t-italic" style={{ color: 'var(--bad)' }}>{skillMatrixSummary.underIndexTopic}</span>.</>
        }
        sub={skillMatrixSummary.sub}
      />

      <Card pad={false}>
        <div style={{ padding: 24 }}>
          <SkillHeatmap rows={skillMatrixCategories} cols={skillMatrixCohorts} data={skillMatrixData} chartStyle={chartStyle} />
        </div>
        <div style={{ padding: '14px 24px', borderTop: '1px solid var(--border)', display: 'flex', gap: 18, fontSize: 11, color: 'var(--muted)', fontFamily: 'var(--font-mono)', letterSpacing: '0.06em' }}>
          <span><span style={{ display: 'inline-block', width: 8, height: 8, background: 'oklch(0.30 0.04 25 / 0.6)', marginRight: 6 }} />0–25</span>
          <span><span style={{ display: 'inline-block', width: 8, height: 8, background: 'oklch(0.55 0.12 75 / 0.7)', marginRight: 6 }} />25–55</span>
          <span><span style={{ display: 'inline-block', width: 8, height: 8, background: 'oklch(0.74 0.13 155 / 0.8)', marginRight: 6 }} />55–75</span>
          <span><span style={{ display: 'inline-block', width: 8, height: 8, background: 'oklch(0.85 0.14 195 / 0.95)', marginRight: 6 }} />75–100</span>
        </div>
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, marginTop: 20 }}>
        {skillMatrixDeltaCards.map((c) => (
          <SkillGapDeltaCard key={c.topic} card={c} />
        ))}
      </div>
    </div>
  );
}
//-------------------- SkillGapModule ------------- END ----------------
