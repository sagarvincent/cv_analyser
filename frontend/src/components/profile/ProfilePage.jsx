// Layer: 1 (screen) — user profile settings, four-tab layout
import { useState } from 'react';
import { Card } from '../ui/Card';
import { Field } from './Field';
import { PwField } from './PwField';
import { PwStrength } from './PwStrength';
import { Toggle } from './Toggle';
import { Mini } from './Mini';
import { useAnalysis } from '../../context/AnalysisContext';
import { useAuth } from '../../context/AuthContext';

const TABS = [
  { id: 'account',  label: 'Account',        code: '01' },
  { id: 'security', label: 'Security',       code: '02' },
  { id: 'data',     label: 'Data & Privacy', code: '03' },
  { id: 'danger',   label: 'Danger Zone',    code: '04' },
];

// -------------------- ProfilePage ----------- START ----------
// -- Calls : savePassword, Card, Field, PwField, PwStrength, Toggle, Mini
// -- Called by: Dashboard
function yearsOfExp(experience) {
  if (!experience?.length) return 0;
  const earliest = experience.reduce((min, e) => e.joining_date < min ? e.joining_date : min, experience[0].joining_date);
  return Math.max(0, Math.floor((Date.now() - new Date(earliest)) / 3.156e10));
}

function buildFieldsFromUser(user) {
  const exp = user.experience?.[0];
  return [
    { label: 'Full name',     value: user.full_name },
    { label: 'Email',         value: user.email },
    { label: 'Current title', value: exp?.job_title || '—' },
    { label: 'Company',       value: exp?.company || '—' },
    { label: 'Location',      value: user.location || '—' },
    { label: 'Age',           value: user.age ? `${user.age} years old` : '—' },
    { label: 'Years exp.',    value: `${yearsOfExp(user.experience)} years` },
    { label: 'Username',      value: user.username, link: true },
  ];
}

export function ProfilePage({ profile, onBack }) {
  const { user } = useAuth();
  const {
    profileAccountFields = () => [],
    profileAccountStats = [],
    profileSessions = [],
    profileDataStats = [],
    profileToggles = [],
    profileDeletionDate = '',
    profileLastUpdated = '',
  } = useAnalysis();

  const [tab, setTab] = useState('account');
  const [pw, setPw] = useState({ current: '', next: '', confirm: '' });
  const [pwSaved, setPwSaved] = useState(false);
  const [pwError, setPwError] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState('');
  const [deleted, setDeleted] = useState(false);

  const cv = user
    ? { name: user.full_name, role: user.experience?.[0]?.job_title || '—', years: yearsOfExp(user.experience), company: user.experience?.[0]?.company || '—' }
    : (profile?.cv || { name: 'Aria Chen', role: 'Senior Product Designer', years: 8, company: 'Lumina Health' });

  const fields = user ? buildFieldsFromUser(user) : profileAccountFields(cv);

  // -------------------- savePassword ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: ProfilePage
  const savePassword = () => {
    setPwError('');
    setPwSaved(false);
    if (!pw.current) return setPwError('Enter your current password.');
    if (pw.next.length < 10) return setPwError('New password must be at least 10 characters.');
    if (pw.next !== pw.confirm) return setPwError("New password and confirmation don't match.");
    setPwSaved(true);
    setPw({ current: '', next: '', confirm: '' });
    setTimeout(() => setPwSaved(false), 3500);
  };
  //-------------------- savePassword ------------- END ----------------

  return (
    <div className="fade-in" style={{ maxWidth: 1100, margin: '0 auto', padding: '40px 48px 80px' }}>
      {/* Hero header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 36 }}>
        <div>
          <button className="btn btn-ghost" onClick={onBack} style={{ marginBottom: 18 }}>← Back to analysis</button>
          <div className="t-eyebrow" style={{ color: 'var(--accent)', marginBottom: 12 }}>Profile · 0xUSR-4A7F2</div>
          <div className="t-display" style={{ fontSize: 56, lineHeight: 1, letterSpacing: '-0.02em' }}>{cv.name}</div>
          <div style={{ marginTop: 12, color: 'var(--text-2)', fontSize: 16 }}>
            {cv.role} · {cv.years} yrs · {cv.company}
          </div>
        </div>
        <div style={{
          width: 88, height: 88, borderRadius: 999,
          background: 'linear-gradient(135deg, var(--accent), var(--violet))',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: 'var(--font-display)', fontSize: 44, color: 'var(--ink)', fontStyle: 'italic',
          boxShadow: '0 0 24px var(--accent-glow)',
        }}>{cv.name[0]}</div>
      </div>

      {/* Account stats strip */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 0, border: '1px solid var(--border)', borderRadius: 8, marginBottom: 32, overflow: 'hidden' }}>
        {profileAccountStats.map((c, i) => (
          <div key={c.label} style={{ padding: 22, background: 'var(--surface)', borderRight: i < 3 ? '1px solid var(--border)' : 'none' }}>
            <div className="t-label" style={{ marginBottom: 14 }}>{c.label}</div>
            <div className="t-num" style={{ fontSize: 28, lineHeight: 1 }}>{c.value}</div>
            <div style={{ marginTop: 8, fontSize: 12, color: 'var(--muted)' }}>{c.sub}</div>
          </div>
        ))}
      </div>

      {/* Two-column layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', gap: 32, alignItems: 'start' }}>
        <nav style={{ position: 'sticky', top: 92, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <div className="t-label" style={{ padding: '0 14px 12px' }}>SETTINGS</div>
          {TABS.map((t) => {
            const active = t.id === tab;
            return (
              <button key={t.id} onClick={() => setTab(t.id)} style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '10px 14px',
                background: active ? 'var(--surface-2)' : 'transparent',
                border: 0,
                borderLeft: `2px solid ${active ? (t.id === 'danger' ? 'var(--bad)' : 'var(--accent)') : 'transparent'}`,
                color: active ? 'var(--text)' : 'var(--text-2)',
                fontSize: 13, cursor: 'pointer', textAlign: 'left',
                fontFamily: 'var(--font-sans)',
                transition: '120ms ease',
              }}>
                <span className="t-mono" style={{ fontSize: 10, color: active ? (t.id === 'danger' ? 'var(--bad)' : 'var(--accent)') : 'var(--muted)', letterSpacing: '0.08em' }}>
                  {t.code}
                </span>
                <span>{t.label}</span>
              </button>
            );
          })}
        </nav>

        <div style={{ minWidth: 0 }}>
          {tab === 'account' && (
            <Card eyebrow="01 / 04" title="Account information">
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
                {fields.map((f) => <Field key={f.label} {...f} />)}
              </div>
              <div className="hairline" style={{ margin: '24px 0 20px' }} />
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ color: 'var(--muted)', fontSize: 12 }}>Last updated {profileLastUpdated}</div>
                <button className="btn btn-primary">Save changes</button>
              </div>
            </Card>
          )}

          {tab === 'security' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <Card eyebrow="02 / 04" title="Change password">
                <div style={{ display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 460 }}>
                  <PwField label="Current password" value={pw.current} onChange={(v) => setPw({ ...pw, current: v })} />
                  <PwField label="New password" value={pw.next} onChange={(v) => setPw({ ...pw, next: v })} hint="At least 10 characters · mix letters, numbers, symbols" />
                  <PwField label="Confirm new" value={pw.confirm} onChange={(v) => setPw({ ...pw, confirm: v })} />
                  <PwStrength value={pw.next} />
                  {pwError && (
                    <div style={{ padding: '10px 14px', background: 'oklch(0.30 0.10 25 / 0.25)', border: '1px solid var(--bad)', color: 'var(--bad)', borderRadius: 4, fontSize: 13 }}>
                      ⚠ {pwError}
                    </div>
                  )}
                  {pwSaved && (
                    <div style={{ padding: '10px 14px', background: 'oklch(0.30 0.10 155 / 0.18)', border: '1px solid var(--good)', color: 'var(--good)', borderRadius: 4, fontSize: 13 }}>
                      ✓ Password updated. You'll stay signed in on this device.
                    </div>
                  )}
                  <button className="btn btn-primary" onClick={savePassword} style={{ alignSelf: 'flex-start', marginTop: 4 }}>
                    Update password
                  </button>
                </div>
              </Card>

              <Card eyebrow="—" title="Two-factor authentication">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 500, marginBottom: 4 }}>Authenticator app</div>
                    <div style={{ color: 'var(--text-2)', fontSize: 13 }}>Active on iPhone · added 4 Feb 2026</div>
                  </div>
                  <span className="pill pill-good pill-dot">ENABLED</span>
                </div>
                <div className="hairline" style={{ margin: '16px 0' }} />
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 500, marginBottom: 4 }}>Recovery codes</div>
                    <div style={{ color: 'var(--text-2)', fontSize: 13 }}>8 of 10 unused</div>
                  </div>
                  <button className="btn">Regenerate</button>
                </div>
              </Card>

              <Card eyebrow="—" title="Active sessions">
                {profileSessions.map((s, i) => (
                  <div key={i} style={{ padding: '14px 0', borderBottom: i < profileSessions.length - 1 ? '1px solid var(--border)' : 'none', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ fontWeight: 500, marginBottom: 2 }}>
                        {s.device}
                        {s.current && <span style={{ color: 'var(--accent)', fontSize: 11, marginLeft: 6, fontFamily: 'var(--font-mono)', letterSpacing: '0.08em' }}>● THIS DEVICE</span>}
                      </div>
                      <div style={{ color: 'var(--muted)', fontSize: 12, fontFamily: 'var(--font-mono)' }}>{s.loc} · {s.when}</div>
                    </div>
                    {!s.current && <button className="btn btn-ghost">Revoke</button>}
                  </div>
                ))}
              </Card>
            </div>
          )}

          {tab === 'data' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <Card eyebrow="03 / 04" title="Your data on STRATA">
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, marginBottom: 18 }}>
                  {profileDataStats.map((s) => <Mini key={s.label} label={s.label} value={s.value} />)}
                </div>
                <div style={{ color: 'var(--text-2)', fontSize: 13, lineHeight: 1.6 }}>
                  We retain raw CVs for 30 days and the derived analyses for 12 months. Vector embeddings are anonymised after 7 days. You can export everything or request immediate purge.
                </div>
                <div className="hairline" style={{ margin: '20px 0' }} />
                <div style={{ display: 'flex', gap: 10 }}>
                  <button className="btn">⇣ Export all data (JSON)</button>
                  <button className="btn">⇣ Export analyses (PDF bundle)</button>
                  <button className="btn btn-ghost">Purge all data</button>
                </div>
              </Card>

              <Card eyebrow="—" title="Analytics & marketing">
                {profileToggles.map((t) => <Toggle key={t.label} {...t} />)}
              </Card>
            </div>
          )}

          {tab === 'danger' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <div style={{ border: '1px solid var(--bad)', borderRadius: 8, background: 'var(--surface)', overflow: 'hidden' }}>
                <div style={{ padding: '14px 18px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'baseline', gap: 12 }}>
                  <span className="t-label" style={{ color: 'var(--bad)' }}>04 / 04 · DANGER ZONE</span>
                  <span style={{ fontWeight: 500 }}>Irreversible actions</span>
                </div>
                <div style={{ padding: 'var(--pad)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px 0', borderBottom: '1px solid var(--border)' }}>
                    <div>
                      <div style={{ fontWeight: 500, marginBottom: 4 }}>Deactivate account</div>
                      <div style={{ color: 'var(--text-2)', fontSize: 13 }}>Sign out everywhere and freeze your account. Reversible within 30 days.</div>
                    </div>
                    <button className="btn">Deactivate</button>
                  </div>

                  {!deleted ? (
                    <div style={{ paddingTop: 18 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 24 }}>
                        <div style={{ flex: 1 }}>
                          <div style={{ fontWeight: 500, marginBottom: 6, color: 'var(--bad)' }}>Delete account permanently</div>
                          <div style={{ color: 'var(--text-2)', fontSize: 13, lineHeight: 1.6, marginBottom: 14 }}>
                            Erases your CVs, analyses, embeddings, and account. We will keep an anonymised invoice record for tax compliance for 7 years. <strong style={{ color: 'var(--text)' }}>This cannot be undone.</strong>
                          </div>
                          <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                            <input
                              value={deleteConfirm}
                              onChange={(e) => setDeleteConfirm(e.target.value)}
                              placeholder='Type "DELETE" to confirm'
                              style={{
                                flex: 1, padding: '10px 12px',
                                background: 'var(--ink-2)', border: '1px solid var(--border)',
                                borderRadius: 4, color: 'var(--text)', fontSize: 13, outline: 'none',
                                fontFamily: 'var(--font-mono)', letterSpacing: '0.08em',
                              }}
                            />
                            <button
                              disabled={deleteConfirm !== 'DELETE'}
                              onClick={() => setDeleted(true)}
                              className="btn"
                              style={{
                                background: deleteConfirm === 'DELETE' ? 'var(--bad)' : 'var(--surface-2)',
                                color: deleteConfirm === 'DELETE' ? 'var(--ink)' : 'var(--muted)',
                                borderColor: deleteConfirm === 'DELETE' ? 'var(--bad)' : 'var(--border)',
                                cursor: deleteConfirm === 'DELETE' ? 'pointer' : 'not-allowed',
                                boxShadow: deleteConfirm === 'DELETE' ? '0 0 12px oklch(0.72 0.18 25 / 0.4)' : 'none',
                              }}
                            >
                              Delete account
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div style={{ padding: '24px 0', textAlign: 'center' }}>
                      <div className="t-display" style={{ fontSize: 28, fontStyle: 'italic', color: 'var(--bad)' }}>
                        Account scheduled for deletion.
                      </div>
                      <div style={{ marginTop: 10, color: 'var(--text-2)', fontSize: 13 }}>
                        We've queued a complete purge for {profileDeletionDate}. Sign in before then to cancel.
                      </div>
                      <button className="btn" style={{ marginTop: 18 }} onClick={() => { setDeleted(false); setDeleteConfirm(''); }}>
                        ↺ Cancel deletion
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
//-------------------- ProfilePage ------------- END ----------------
