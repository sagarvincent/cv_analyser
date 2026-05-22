// Layer: 2 (UI sub-component) — pure rendering
import { clampNorm } from '../../utils/animationUtils';
import { toneToColor } from '../../utils/colorUtils';

// -------------------- Bar ----------- START ----------
// -- Calls : clampNorm, toneToColor
// -- Called by: JDFitModule, PeerModule, AlignModule
export function Bar({ value, max = 100, tone = 'accent', height = 6, label, right }) {
  const pct = clampNorm(value, max);
  const color = toneToColor(tone);

  return (
    <div>
      {(label || right) && (
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: 12 }}>
          <span style={{ color: 'var(--text-2)' }}>{label}</span>
          <span className="t-mono" style={{ color: 'var(--muted)' }}>{right}</span>
        </div>
      )}
      <div style={{ height, background: 'var(--surface-3)', borderRadius: 2, overflow: 'hidden' }}>
        <div style={{
          width: `${pct * 100}%`, height: '100%', background: color,
          boxShadow: tone === 'accent' ? `0 0 12px ${color}` : 'none',
          transition: 'width 600ms cubic-bezier(.2,.7,.2,1)',
        }} />
      </div>
    </div>
  );
}
//-------------------- Bar ------------- END ----------------
