// Layer: 2 (module sub-component) — one gap row in JDFitModule
import { Pill } from '../ui';
import { impactTone } from '../../utils/jdFitUtils';

// -------------------- JDFitGapItem ----------- START ----------
// -- Calls : Pill, impactTone
// -- Called by: JDFitModule
export function JDFitGapItem({ gap, isLast }) {
  const tone = impactTone(gap.impact);
  return (
    <div style={{ padding: '14px 0', borderBottom: isLast ? 'none' : '1px solid var(--border)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 8 }}>
        <span style={{ fontWeight: 500 }}>{gap.topic}</span>
        <Pill tone={tone} dot>{gap.impact}</Pill>
      </div>
      <div style={{ color: 'var(--text-2)', fontSize: 13, lineHeight: 1.5 }}>{gap.note}</div>
    </div>
  );
}
//-------------------- JDFitGapItem ------------- END ----------------
