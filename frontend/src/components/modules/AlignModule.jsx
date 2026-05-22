// Layer: 1 (module screen) — you vs market alignment module
import { Card, SectionHeader } from '../ui';
import { Radar } from '../charts';
import { AlignRow } from './AlignRow';
import { buildAlignRows } from '../../utils/alignUtils';
import { alignSummary, alignAxes, alignYou, alignMarket } from '../../data/mockData';

// -------------------- AlignModule ----------- START ----------
// -- Calls : SectionHeader, Card, Radar, AlignRow, buildAlignRows
// -- Called by: App (via MODULE_COMPONENTS)
export function AlignModule() {
  const rows = buildAlignRows(alignAxes, alignYou, alignMarket);

  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={alignSummary.eyebrow}
        title={
          <>You're built for <span className="t-italic" style={{ color: 'var(--accent)' }}>{alignSummary.titleAccent}</span>, not <span className="t-italic" style={{ color: 'var(--warn)' }}>{alignSummary.titleWarn}</span>.</>
        }
        sub={alignSummary.sub}
      />

      <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: 24, alignItems: 'start' }}>
        <Card eyebrow="ALIGNMENT" title="Profile vs market vector">
          <div style={{ display: 'flex', justifyContent: 'center', padding: 12 }}>
            <Radar axes={alignAxes} you={alignYou} target={alignMarket} size={360} />
          </div>
          <div style={{ display: 'flex', gap: 18, justifyContent: 'center', marginTop: 6, fontSize: 11.5, fontFamily: 'var(--font-mono)', color: 'var(--muted)', letterSpacing: '0.06em' }}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
              <span style={{ width: 14, height: 2, background: 'var(--accent)' }} />YOU
            </span>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
              <span style={{ width: 14, height: 2, background: 'var(--warn)' }} />MARKET DIRECTION
            </span>
          </div>
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {rows.map((row) => (
            <AlignRow key={row.axis} row={row} />
          ))}
        </div>
      </div>
    </div>
  );
}
//-------------------- AlignModule ------------- END ----------------
