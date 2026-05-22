// Layer: 2 (flow sub-component) — one reasoning-trace row in AnalysisScreen

// -------------------- TraceRow ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: AnalysisScreen
export function TraceRow({ row, isActive, isDone }) {
  return (
    <div className="fade-in"
      style={{
        padding: '13px 22px',
        display: 'grid', gridTemplateColumns: '100px 14px 1fr auto', gap: 16,
        alignItems: 'center',
        borderBottom: isDone ? '1px solid var(--border)' : '1px solid transparent',
        opacity: isActive ? 1 : 0.55,
        fontSize: 13,
      }}>
      <span className="t-mono" style={{ fontSize: 10.5, color: 'var(--accent)', letterSpacing: '0.12em' }}>
        {row.stage}
      </span>
      <span style={{
        width: 8, height: 8, borderRadius: 999,
        background: isActive ? 'var(--accent)' : 'var(--muted-2)',
        boxShadow: isActive ? '0 0 8px var(--accent)' : 'none',
        animation: isActive ? 'strataPulse 0.9s ease-in-out infinite' : 'none',
      }} />
      <span style={{ color: 'var(--text-2)', fontFamily: 'var(--font-mono)', fontSize: 12 }}>
        {row.text}
      </span>
      <span className="t-mono" style={{ fontSize: 10.5, color: isDone ? 'var(--good)' : 'var(--muted)' }}>
        {isDone ? '✓ OK' : '•••'}
      </span>
    </div>
  );
}
//-------------------- TraceRow ------------- END ----------------
