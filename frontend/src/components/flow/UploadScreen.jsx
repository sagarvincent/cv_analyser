// Layer: 1 (flow screen) — CV and JD upload interaction
import { useState, useRef } from 'react';
import { CapabilityCell } from './CapabilityCell';
import { validateFile } from '../../utils/fileValidationUtils';
import { appConfig } from '../../config/appConfig';
import { useAnalysis } from '../../context/AnalysisContext';

const JD_ALLOWED = ['pdf', 'doc', 'docx', 'json', 'csv'];
const JD_MAX_BYTES = 16 * 1024 * 1024;

// -------------------- UploadScreen ----------- START ----------
// -- Calls : useSample, handleFile, handleJdFile, submit, CapabilityCell
// -- Called by: App
export function UploadScreen({ onComplete }) {
  const { sampleCv, sampleJd, capabilityStrip = [] } = useAnalysis();

  const [cv, setCv] = useState(null);
  const [jd, setJd] = useState('');
  const [jdMode, setJdMode] = useState('text'); // 'text' | 'file'
  const [jdFile, setJdFile] = useState(null);
  const [jdDragOver, setJdDragOver] = useState(false);
  const [jdError, setJdError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const fileInputRef = useRef(null);
  const jdFileInputRef = useRef(null);

  // -------------------- useSample ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: UploadScreen
  const useSample = () => {
    setError(null); setJdError(null);
    setCv(sampleCv); setJd(sampleJd);
    setJdFile(null); setJdMode('text');
  };
  // -------------------- useSample ------------- END ----------------

  // -------------------- handleFile ----------- START ----------
  // -- Calls : validateFile
  // -- Called by: UploadScreen (drop handler, file input onChange)
  const handleFile = (file) => {
    const err = validateFile(file);
    if (err) { setError(err); return; }
    setError(null);
    setCv({ file: file.name, _file: file });
  };
  // -------------------- handleFile ------------- END ----------------

  // -------------------- handleJdFile ----------- START ----------
  // -- Calls : nothing (leaf validation)
  // -- Called by: UploadScreen (JD drop handler, JD file input onChange)
  const handleJdFile = (file) => {
    const ext = file.name.includes('.') ? file.name.split('.').pop().toLowerCase() : '';
    if (!JD_ALLOWED.includes(ext)) {
      setJdError(`'.${ext || '?'}' not supported. Upload ${JD_ALLOWED.map(e => e.toUpperCase()).join(', ')}.`);
      return;
    }
    if (file.size > JD_MAX_BYTES) {
      setJdError(`File is ${(file.size / 1024 / 1024).toFixed(1)} MB — exceeds the 16 MB limit.`);
      return;
    }
    setJdError(null);
    setJdFile({ file: file.name, _file: file });
  };
  // -------------------- handleJdFile ------------- END ----------------

  // -------------------- submit ----------- START ----------
  // -- Calls : onComplete
  // -- Called by: UploadScreen
  const submit = async () => {
    if (appConfig.useMockData) {
      onComplete({ cv: cv || sampleCv, jd: jd || sampleJd });
      return;
    }
    if (!cv?._file) { setError('Please upload a CV file to continue.'); return; }
    setError(null);
    setSubmitting(true);
    try {
      const form = new FormData();
      form.append('cv', cv._file);
      if (jdMode === 'file' && jdFile?._file) {
        form.append('jd_file', jdFile._file);
      } else {
        form.append('jd', jd);
      }
      const res = await fetch(`${appConfig.apiBaseUrl}/analyze`, { method: 'POST', body: form });
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data = await res.json();
      onComplete(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };
  // -------------------- submit ------------- END ----------------

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

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.doc"
            style={{ display: 'none' }}
            onChange={(e) => { if (e.target.files[0]) handleFile(e.target.files[0]); e.target.value = ''; }}
          />

          {!cv ? (
            <>
              <div
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault(); setDragOver(false);
                  const file = e.dataTransfer.files[0];
                  if (file) handleFile(file);
                }}
                style={{
                  border: `1px dashed ${error ? 'var(--error, #e05)' : dragOver ? 'var(--accent)' : 'var(--border-2)'}`,
                  borderRadius: 6, padding: '44px 20px', textAlign: 'center',
                  background: dragOver ? 'var(--accent-glow)' : 'transparent',
                  transition: '200ms ease', cursor: 'pointer',
                }}
                onClick={() => fileInputRef.current?.click()}
              >
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.14em', color: 'var(--muted)', marginBottom: 14 }}>
                  PDF · DOCX · DOC · max 16 MB
                </div>
                <div style={{ color: 'var(--text-2)' }}>
                  Drag & drop or <span style={{ color: 'var(--accent)', textDecoration: 'underline', textUnderlineOffset: 3 }}>browse</span>
                </div>
                <div style={{ marginTop: 18, fontSize: 11.5, color: 'var(--muted)' }}>
                  Encrypted in transit · purged after analysis
                </div>
              </div>
              {error && (
                <div style={{
                  marginTop: 10, padding: '8px 12px', borderRadius: 4,
                  background: 'rgba(220,38,38,0.08)', border: '1px solid rgba(220,38,38,0.3)',
                  color: 'var(--error, #e05)', fontSize: 12, fontFamily: 'var(--font-mono)',
                }}>
                  {error}
                </div>
              )}
            </>
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
              }}>
                {cv.file.split('.').pop().toUpperCase()}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 500, fontSize: 14 }}>{cv.file}</div>
                {cv.name && (
                  <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 2, fontFamily: 'var(--font-mono)' }}>
                    → {cv.name} · {cv.role} · {cv.years}y · {cv.company}
                  </div>
                )}
              </div>
              <button className="btn btn-ghost" onClick={() => { setCv(null); setError(null); }}>✕</button>
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

          {/* Mode toggle */}
          <div style={{
            display: 'flex', gap: 2, marginBottom: 12,
            background: 'var(--ink-2)', borderRadius: 5, padding: 3,
          }}>
            {[['text', '// PASTE TEXT'], ['file', '↑ UPLOAD FILE']].map(([mode, label]) => (
              <button
                key={mode}
                onClick={() => { setJdMode(mode); setJdError(null); }}
                style={{
                  flex: 1, padding: '5px 10px', borderRadius: 3, border: 'none', cursor: 'pointer',
                  background: jdMode === mode ? 'var(--surface-2)' : 'transparent',
                  color: jdMode === mode ? 'var(--text)' : 'var(--muted)',
                  fontSize: 11, fontFamily: 'var(--font-mono)', letterSpacing: '0.1em',
                  fontWeight: jdMode === mode ? 600 : 400, transition: '150ms ease',
                }}
              >
                {label}
              </button>
            ))}
          </div>

          {jdMode === 'text' ? (
            <textarea
              value={jd}
              onChange={(e) => setJd(e.target.value)}
              placeholder="Paste a JD here, or leave blank to receive a general market analysis."
              style={{
                width: '100%', height: 160, padding: 14,
                background: 'var(--ink-2)', border: '1px solid var(--border)',
                borderRadius: 4, color: 'var(--text)', fontSize: 13,
                resize: 'none', outline: 'none', lineHeight: 1.55, boxSizing: 'border-box',
              }}
            />
          ) : (
            <>
              <input
                ref={jdFileInputRef}
                type="file"
                accept=".pdf,.doc,.docx,.json,.csv"
                style={{ display: 'none' }}
                onChange={(e) => { if (e.target.files[0]) handleJdFile(e.target.files[0]); e.target.value = ''; }}
              />
              {!jdFile ? (
                <div
                  onDragOver={(e) => { e.preventDefault(); setJdDragOver(true); }}
                  onDragLeave={() => setJdDragOver(false)}
                  onDrop={(e) => {
                    e.preventDefault(); setJdDragOver(false);
                    const file = e.dataTransfer.files[0];
                    if (file) handleJdFile(file);
                  }}
                  onClick={() => jdFileInputRef.current?.click()}
                  style={{
                    border: `1px dashed ${jdError ? 'var(--error, #e05)' : jdDragOver ? 'var(--accent)' : 'var(--border-2)'}`,
                    borderRadius: 6, padding: '36px 20px', textAlign: 'center',
                    background: jdDragOver ? 'var(--accent-glow)' : 'transparent',
                    transition: '200ms ease', cursor: 'pointer',
                  }}
                >
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.14em', color: 'var(--muted)', marginBottom: 14 }}>
                    PDF · DOC · DOCX · JSON · CSV · max 16 MB
                  </div>
                  <div style={{ color: 'var(--text-2)' }}>
                    Drag & drop or <span style={{ color: 'var(--accent)', textDecoration: 'underline', textUnderlineOffset: 3 }}>browse</span>
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
                  }}>
                    {jdFile.file.split('.').pop().toUpperCase()}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: 500, fontSize: 14 }}>{jdFile.file}</div>
                  </div>
                  <button className="btn btn-ghost" onClick={() => { setJdFile(null); setJdError(null); }}>✕</button>
                </div>
              )}
              {jdError && (
                <div style={{
                  marginTop: 10, padding: '8px 12px', borderRadius: 4,
                  background: 'rgba(220,38,38,0.08)', border: '1px solid rgba(220,38,38,0.3)',
                  color: 'var(--error, #e05)', fontSize: 12, fontFamily: 'var(--font-mono)',
                }}>
                  {jdError}
                </div>
              )}
            </>
          )}
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 32, gap: 16 }}>
        {sampleCv && (
          <button className="btn btn-ghost" onClick={useSample}>↻ Load sample profile (Aria Chen)</button>
        )}
        <button className="btn btn-primary" onClick={submit} disabled={submitting} style={{ padding: '12px 22px', fontSize: 12, marginLeft: 'auto' }}>
          {submitting ? 'Submitting…' : 'Run analysis ⏵'}
        </button>
      </div>

      {capabilityStrip.length > 0 && (
        <div style={{
          marginTop: 64, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
          gap: 0, borderTop: '1px solid var(--border)', borderBottom: '1px solid var(--border)',
        }}>
          {capabilityStrip.map(([n, l]) => (
            <CapabilityCell key={l} value={n} label={l} />
          ))}
        </div>
      )}
    </div>
  );
}
// -------------------- UploadScreen ------------- END ----------------
