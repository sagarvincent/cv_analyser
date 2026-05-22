// Layer: 2 (profile atom) — pure rendering
import { useState } from 'react';

// -------------------- PwField ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: ProfilePage
export function PwField({ label, value, onChange, hint }) {
  const [show, setShow] = useState(false);
  return (
    <div>
      <div className="t-label" style={{ marginBottom: 8 }}>{label}</div>
      <div style={{ position: 'relative' }}>
        <input
          type={show ? 'text' : 'password'}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          style={{
            width: '100%', padding: '10px 38px 10px 12px',
            background: 'var(--ink-2)', border: '1px solid var(--border)',
            borderRadius: 4, color: 'var(--text)', fontSize: 14, outline: 'none',
            fontFamily: 'var(--font-mono)', letterSpacing: value ? '0.18em' : 'normal',
          }}
        />
        <button onClick={() => setShow(s => !s)}
          style={{ position: 'absolute', right: 8, top: 8, background: 'transparent', border: 0, color: 'var(--muted)', cursor: 'pointer', fontSize: 11, fontFamily: 'var(--font-mono)' }}>
          {show ? 'HIDE' : 'SHOW'}
        </button>
      </div>
      {hint && <div style={{ marginTop: 6, fontSize: 11, color: 'var(--muted)' }}>{hint}</div>}
    </div>
  );
}
//-------------------- PwField ------------- END ----------------
