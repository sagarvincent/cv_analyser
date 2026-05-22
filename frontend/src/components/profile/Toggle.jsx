// Layer: 2 (profile atom) — pure rendering
import { useState } from 'react';

// -------------------- Toggle ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: ProfilePage
export function Toggle({ label, desc, defaultOn = false }) {
  const [on, setOn] = useState(defaultOn);
  return (
    <div style={{ padding: '14px 0', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 16 }}>
      <div>
        <div style={{ fontWeight: 500, marginBottom: 3 }}>{label}</div>
        <div style={{ color: 'var(--text-2)', fontSize: 12.5 }}>{desc}</div>
      </div>
      <button onClick={() => setOn(o => !o)} style={{
        width: 40, height: 22, borderRadius: 999, position: 'relative',
        background: on ? 'var(--accent)' : 'var(--surface-3)',
        border: `1px solid ${on ? 'var(--accent)' : 'var(--border-2)'}`,
        cursor: 'pointer', transition: '200ms',
        boxShadow: on ? '0 0 8px var(--accent-glow)' : 'none',
        flexShrink: 0,
      }}>
        <span style={{
          position: 'absolute', top: 2, left: on ? 20 : 2,
          width: 16, height: 16, borderRadius: 99,
          background: on ? 'var(--ink)' : 'var(--text-2)',
          transition: '200ms',
        }} />
      </button>
    </div>
  );
}
//-------------------- Toggle ------------- END ----------------
