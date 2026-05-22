// Layer: 2 (UI sub-component) — pure rendering, animation calculation delegated to utils
import { useState, useEffect } from 'react';
import { cubicEaseOut } from '../../utils/animationUtils';

// -------------------- CountUp ----------- START ----------
// -- Calls : cubicEaseOut
// -- Called by: OverviewModule, JDFitModule, PeerModule, CompModule, Ring
export function CountUp({ to, suffix = '', duration = 900, decimals = 0 }) {
  const [v, setV] = useState(0);

  useEffect(() => {
    const start = performance.now();
    let raf;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      setV(to * cubicEaseOut(t));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [to, duration]);

  return <>{decimals ? v.toFixed(decimals) : Math.round(v)}{suffix}</>;
}
//-------------------- CountUp ------------- END ----------------
