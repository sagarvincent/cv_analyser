// Layer: 1 (module screen) — ATS compatibility check module
import { Ring, SectionHeader } from '../ui';
import { ATSCheckItem } from './ATSCheckItem';
import { countPassedChecks } from '../../utils/atsUtils';
import { atsSummary, atsChecks } from '../../data/mockData';

// -------------------- ATSModule ----------- START ----------
// -- Calls : SectionHeader, Ring, ATSCheckItem, countPassedChecks
// -- Called by: App (via MODULE_COMPONENTS)
export function ATSModule() {
  const passed = countPassedChecks(atsChecks);

  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={atsSummary.eyebrow}
        title={
          <><span className="t-italic" style={{ color: 'var(--good)' }}>{atsSummary.titleScore}</span>{atsSummary.titleRest}</>
        }
        sub={atsSummary.sub}
      />

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: 24 }}>
        <div className="card" style={{ padding: 28, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18 }}>
          <Ring value={atsSummary.score} size={210} label="ATS SCORE" tone="good" />
          <div style={{ textAlign: 'center' }}>
            <div className="t-label" style={{ marginBottom: 6 }}>{passed} of {atsChecks.length} CHECKS PASSED</div>
            <div style={{ fontSize: 12, color: 'var(--muted)' }}>
              Estimated recruiter dwell: <span style={{ color: 'var(--good)' }}>{atsSummary.dwellTime}</span> · norm: {atsSummary.normDwellTime}
            </div>
          </div>
        </div>

        <div className="card" style={{ padding: 0 }}>
          {atsChecks.map((c, i) => (
            <ATSCheckItem key={i} check={c} isLast={i === atsChecks.length - 1} />
          ))}
        </div>
      </div>
    </div>
  );
}
//-------------------- ATSModule ------------- END ----------------
