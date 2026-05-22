// Layer: 1 (flow screen) — CV and JD upload interaction
import { useState } from 'react';
import { CapabilityCell } from './CapabilityCell';
import { SAMPLE_CV, SAMPLE_JD, CAPABILITY_STRIP } from '../../data/mockData';

// -------------------- UploadScreen ----------- START ----------
// -- Calls : useSample, submit, CapabilityCell
// -- Called by: App
export function UploadScreen({ onComplete }) {
  const [cv, setCv] = useState(null);
  const [jd, setJd] = useState('');
  const [dragOver, setDragOver] = useState(false);

  // -------------------- useSample ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: UploadScreen
  const useSample = () => { setCv(SAMPLE_CV); setJd(SAMPLE_JD); };
  //-------------------- useSample ------------- END ----------------

  // -------------------- submit ----------- START ----------
  // -- Calls : onComplete
  // -- Called by: UploadScreen
  const submit = () => { onComplete({ cv: cv || SAMPLE_CV, jd: jd || SAMPLE_JD }); };
  //-------------------- submit ------------- END ----------------

  return (
    <div className="fade-in" style={{ maxWidth: 980, margin: '0 auto', padding: '60px 40px' }}>
      <div style={{ marginBottom: 48 }}>
        <div className="t-eyebrow" style={{ color: 'var(--accent)', marginBottom: 14 }}>
          ⏵ Engine ready · v4.2.1
        </div>
        <div className="t-display" style={{ fontSize: 64, lineHeight: 1, letterSpacing: '-0.025em' }}>
          Submit your <span className="t-italic" style={{ color: 'var(--accent)' }}>profile</span>
          <br />for scrutiny.
        </div>
        <div style={{ color: 'var(--text-2)', maxWidth: 560, marginTop: 18, fontSize: 16 }}>
          We benchmark your CV against 2.4M+ live profiles, 180k active job postings, and the salary
          distributions of 320 markets. The analysis takes about 14 seconds.
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* CV Upload */}
        <div className="card" style={{ padding: 24, position: 'relative', overflow: 'hidden' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
            <div>
              <div className="t-label" style={{ marginBottom: 6 }}>01 · Your CV</div>
              <div style={{ fontSize: 18, fontWeight: 500 }}>Resume or LinkedIn export</div>
            </div>
            <span className="pill pill-accent pill-dot">REQUIRED</span>
          </div>

          {!cv ? (
            <div
              onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => { e.preventDefault(); setDragOver(false); setCv(SAMPLE_CV); }}
              style={{
                border: `1px dashed ${dragOver ? 'var(--accent)' : 'var(--border-2)'}`,
                borderRadius: 6, padding: '44px 20px', textAlign: 'center',
                background: dragOver ? 'var(--accent-glow)' : 'transparent',
                transition: '200ms ease', cursor: 'pointer',
              }}
              onClick={() => setCv(SAMPLE_CV)}
            >
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.14em', color: 'var(--muted)', marginBottom: 14 }}>
                PDF · DOCX · LINKEDIN.JSON
              </div>
              <div style={{ color: 'var(--text-2)' }}>
                Drag & drop or <span style={{ color: 'var(--accent)', textDecoration: 'underline', textUnderlineOffset: 3 }}>browse</span>
              </div>
              <div style={{ marginTop: 18, fontSize: 11.5, color: 'var(--muted)' }}>
                Encrypted in transit · purged after analysis
              </div>
            </div>
          ) : (
            <div style={{
              border: '1px solid var(--accent-d)', borderRadius: 6,
              padding: 18, background: 'var(--accent-glow)',
              display: 'flex', alignItems: 'center', gap: 14,
            }}>
              <div style={{
                width: 44, height: 56, background: 'var(--surface-3)', borderRadius: 3,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--accent)', letterSpacing: '0.1em',
                border: '1px solid var(--accent-d)',
              }}>PDF</div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 500, fontSize: 14 }}>{cv.file}</div>
                <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 2, fontFamily: 'var(--font-mono)' }}>
                  → {cv.name} · {cv.role} · {cv.years}y · {cv.company}
                </div>
              </div>
              <button className="btn btn-ghost" onClick={() => setCv(null)}>✕</button>
            </div>
          )}
        </div>

        {/* JD */}
        <div className="card" style={{ padding: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
            <div>
              <div className="t-label" style={{ marginBottom: 6 }}>02 · Target role</div>
              <div style={{ fontSize: 18, fontWeight: 500 }}>
                Job description <span style={{ color: 'var(--muted)', fontWeight: 400 }}>(optional)</span>
              </div>
            </div>
            <span className="pill">UNLOCKS · JD FIT</span>
          </div>
          <textarea
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            placeholder="Paste a JD here, or leave blank to receive a general market analysis."
            style={{
              width: '100%', height: 168, padding: 14,
              background: 'var(--ink-2)', border: '1px solid var(--border)',
              borderRadius: 4, color: 'var(--text)', fontSize: 13,
              resize: 'none', outline: 'none', lineHeight: 1.55,
            }}
          />
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 32, gap: 16 }}>
        <button className="btn btn-ghost" onClick={useSample}>↻ Load sample profile (Aria Chen)</button>
        <button className="btn btn-primary" onClick={submit} style={{ padding: '12px 22px', fontSize: 12 }}>
          Run analysis ⏵
        </button>
      </div>

      <div style={{
        marginTop: 64, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
        gap: 0, borderTop: '1px solid var(--border)', borderBottom: '1px solid var(--border)',
      }}>
        {CAPABILITY_STRIP.map(([n, l]) => (
          <CapabilityCell key={l} value={n} label={l} />
        ))}
      </div>
    </div>
  );
}
//-------------------- UploadScreen ------------- END ----------------
