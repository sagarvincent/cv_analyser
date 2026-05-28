// Layer: 1 (flow screen) — orchestrates analysis animation, no inline calculation
import { useState, useEffect, useRef } from 'react';
import { springStep, calcStepDuration, generateTraceId } from '../../utils/animationUtils';
import { TraceRow } from './TraceRow';
import { useAnalysis } from '../../context/AnalysisContext';

// -------------------- AnalysisScreen ----------- START ----------
// -- Calls : springStep, calcStepDuration, generateTraceId, TraceRow
// -- Called by: App
export function AnalysisScreen({ onComplete }) {
  const { reasoningTrace = [] } = useAnalysis();
  const [step, setStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const traceId = useRef(generateTraceId());

  useEffect(() => {
    if (step >= reasoningTrace.length) {
      const t = setTimeout(onComplete, 700);
      return () => clearTimeout(t);
    }
    const dur = calcStepDuration();
    const t = setTimeout(() => setStep(s => s + 1), dur);
    return () => clearTimeout(t);
  }, [step, onComplete]);

  useEffect(() => {
    let raf;
    const tick = () => {
      const target = step / reasoningTrace.length;
      setProgress(p => springStep(p, target, 0.12));
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [step]);

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '80px 40px', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 28 }}>
        <div>
          <div className="t-eyebrow" style={{ color: 'var(--accent)', marginBottom: 10, animation: 'strataPulse 1.4s ease-in-out infinite' }}>
            ⏵ ANALYSING · LIVE REASONING TRACE
          </div>
          <div className="t-display" style={{ fontSize: 44, letterSpacing: '-0.02em', lineHeight: 1 }}>
            Reading <span className="t-italic" style={{ color: 'var(--accent)' }}>2.4M signals</span>…
          </div>
        </div>
        <div className="t-mono" style={{ fontSize: 12, color: 'var(--muted)' }}>
          STRATA · TRACE 0x{traceId.current.toString(16).padStart(5, '0').toUpperCase()}
        </div>
      </div>

      <div style={{ height: 2, background: 'var(--surface-3)', borderRadius: 1, marginBottom: 36, overflow: 'hidden', position: 'relative' }}>
        <div style={{
          height: '100%', width: `${progress * 100}%`,
          background: 'var(--accent)', boxShadow: '0 0 12px var(--accent)',
          transition: 'width 200ms linear',
        }} />
        <div style={{
          position: 'absolute', inset: 0, width: '30%',
          background: 'linear-gradient(90deg, transparent, var(--accent-glow), transparent)',
          animation: 'strataScan 1.8s linear infinite',
        }} />
      </div>

      <div className="card" style={{ padding: '8px 0', maxHeight: 460, overflow: 'hidden' }}>
        {reasoningTrace.slice(0, step + 1).map((row, i) => (
          <TraceRow key={i} row={row} isActive={i === step} isDone={i < step} />
        ))}
      </div>

      <div style={{ marginTop: 24, display: 'flex', justifyContent: 'space-between', color: 'var(--muted)', fontSize: 11.5, fontFamily: 'var(--font-mono)', letterSpacing: '0.08em' }}>
        <span>STAGE {step + 1} / {reasoningTrace.length}</span>
        <span>{(step / reasoningTrace.length * 100).toFixed(0)}% · ETA {Math.max(0, reasoningTrace.length - step)}S</span>
      </div>
    </div>
  );
}
//-------------------- AnalysisScreen ------------- END ----------------
