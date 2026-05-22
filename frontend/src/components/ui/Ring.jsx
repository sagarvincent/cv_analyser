// Layer: 2 (UI sub-component) — pure rendering, animation and geometry delegated to utils
import { useState, useEffect } from 'react';
import { CountUp } from './CountUp';
import { cubicEaseOut, calcRingGeometry } from '../../utils/animationUtils';
import { toneToColor } from '../../utils/colorUtils';

// -------------------- Ring ----------- START ----------
// -- Calls : calcRingGeometry, cubicEaseOut, toneToColor, CountUp
// -- Called by: JDFitModule, ATSModule
export function Ring({ value, max = 100, size = 120, label, tone = 'accent' }) {
  const { pct, r, c } = calcRingGeometry(value, max, size);
  const color = toneToColor(tone);

  const [animPct, setAnimPct] = useState(0);
  useEffect(() => {
    const start = performance.now();
    let raf;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / 900);
      setAnimPct(pct * cubicEaseOut(t));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [pct]);

  return (
    <div style={{ position: 'relative', width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--surface-3)" strokeWidth="3" />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth="3"
          strokeDasharray={`${c * animPct} ${c}`} strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 8px ${color})` }} />
      </svg>
      <div style={{
        position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 2,
      }}>
        <div className="t-num" style={{ fontSize: size * 0.36, lineHeight: 1, letterSpacing: '-0.02em' }}>
          <CountUp to={Math.round(value)} />
        </div>
        {label && <div className="t-label" style={{ fontSize: 9 }}>{label}</div>}
      </div>
    </div>
  );
}
//-------------------- Ring ------------- END ----------------
