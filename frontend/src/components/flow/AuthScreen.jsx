// Layer: 1 (screen) — landing auth page; login, signup, or continue as guest
import { useState, useCallback } from 'react';
import { useAuth } from '../../context/AuthContext';

const INPUT = {
  width: '100%', padding: '11px 14px',
  background: 'var(--ink-2)', border: '1px solid var(--border)',
  borderRadius: 4, color: 'var(--text)', fontSize: 14,
  outline: 'none', fontFamily: 'var(--font-sans)',
  boxSizing: 'border-box', transition: '120ms ease',
};
const LABEL = {
  fontSize: 11, fontFamily: 'var(--font-mono)', color: 'var(--muted)',
  letterSpacing: '0.08em', display: 'block', marginBottom: 6,
};

function AuthField({ label, type = 'text', value, onChange, placeholder, autoComplete }) {
  return (
    <div>
      <label style={LABEL}>{label}</label>
      <input style={INPUT} type={type} value={value} onChange={e => onChange(e.target.value)}
        placeholder={placeholder} autoComplete={autoComplete} required />
    </div>
  );
}

// -------------------- AuthScreen ----------- START ----------
// -- Calls : sha256hex, useAuth, AuthField
// -- Called by: AppRoot
export function AuthScreen({ onAuthComplete, onGuestContinue }) {
  const { login, signup } = useAuth();
  const [mode, setMode] = useState('login');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const [loginFields, setLoginFields] = useState({ username: '', password: '' });
  const [signupFields, setSignupFields] = useState({
    username: '', email: '', password: '', full_name: '', date_of_birth: '', location: '',
  });
  const [cvFile, setCvFile] = useState(null);

  // -------------------- handleLogin ----------- START ----------
  // -- Calls : sha256hex, login
  // -- Called by: AuthScreen form submit
  const handleLogin = useCallback(async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    const res = await login(loginFields.username, loginFields.password);
    setLoading(false);
    if (res.ok) onAuthComplete();
    else setError(res.error);
  }, [login, loginFields, onAuthComplete]);
  // -------------------- handleLogin ------------- END ----------------

  // -------------------- handleSignup ----------- START ----------
  // -- Calls : sha256hex, signup
  // -- Called by: AuthScreen form submit
  const handleSignup = useCallback(async (e) => {
    e.preventDefault();
    setError('');
    if (!cvFile) return setError('Please upload your CV to create an account.');
    setLoading(true);
    const fd = new FormData();
    fd.append('username', signupFields.username);
    fd.append('email', signupFields.email);
    fd.append('password', signupFields.password);
    fd.append('full_name', signupFields.full_name);
    fd.append('date_of_birth', signupFields.date_of_birth);
    if (signupFields.location) fd.append('location', signupFields.location);
    fd.append('cv', cvFile);
    const res = await signup(fd);
    setLoading(false);
    if (res.ok) onAuthComplete();
    else setError(res.error);
  }, [signup, signupFields, cvFile, onAuthComplete]);
  // -------------------- handleSignup ------------- END ----------------

  const set = (field) => (v) => setSignupFields(f => ({ ...f, [field]: v }));

  return (
    <div style={{
      minHeight: '100vh', background: 'var(--ink)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '40px 20px',
    }}>
      <div style={{ width: '100%', maxWidth: 440 }}>

        {/* Brand */}
        <div style={{ textAlign: 'center', marginBottom: 36 }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
            width: 52, height: 52, borderRadius: 10,
            background: 'var(--accent)',
            fontFamily: 'var(--font-display)', fontStyle: 'italic', fontSize: 34,
            color: 'var(--ink)', boxShadow: '0 0 28px var(--accent-glow)', marginBottom: 14,
          }}>S</div>
          <div className="t-display" style={{ fontSize: 34, fontStyle: 'italic' }}>Strata</div>
          <div className="t-mono" style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: '0.18em', marginTop: 5 }}>
            CAREER INTELLIGENCE
          </div>
        </div>

        {/* Mode tabs */}
        <div style={{
          display: 'flex', marginBottom: 20,
          border: '1px solid var(--border)', borderRadius: 6, overflow: 'hidden',
          background: 'var(--ink-2)',
        }}>
          {[['login', 'Sign in'], ['signup', 'Create account']].map(([m, label]) => (
            <button key={m} onClick={() => { setMode(m); setError(''); }} style={{
              flex: 1, padding: '11px 0', background: mode === m ? 'var(--surface)' : 'transparent',
              border: 0, color: mode === m ? 'var(--text)' : 'var(--muted)',
              fontSize: 13, cursor: 'pointer', fontFamily: 'var(--font-sans)',
              fontWeight: mode === m ? 500 : 400, transition: '120ms ease',
            }}>{label}</button>
          ))}
        </div>

        {/* Card */}
        <div style={{
          background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: 8, padding: '28px 28px 24px', marginBottom: 14,
        }}>
          {mode === 'login' ? (
            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <AuthField label="USERNAME" value={loginFields.username}
                onChange={v => setLoginFields(f => ({ ...f, username: v }))}
                autoComplete="username" />
              <AuthField label="PASSWORD" type="password" value={loginFields.password}
                onChange={v => setLoginFields(f => ({ ...f, password: v }))}
                autoComplete="current-password" />
              {error && <ErrorBanner msg={error} />}
              <button className="btn btn-primary" type="submit" disabled={loading} style={{ marginTop: 4 }}>
                {loading ? 'Signing in…' : 'Sign in →'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleSignup} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                <AuthField label="USERNAME" value={signupFields.username} onChange={set('username')} autoComplete="username" />
                <AuthField label="FULL NAME" value={signupFields.full_name} onChange={set('full_name')} autoComplete="name" />
              </div>
              <AuthField label="EMAIL" type="email" value={signupFields.email} onChange={set('email')} autoComplete="email" />
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                <AuthField label="PASSWORD" type="password" value={signupFields.password} onChange={set('password')} autoComplete="new-password" />
                <AuthField label="DATE OF BIRTH" type="date" value={signupFields.date_of_birth} onChange={set('date_of_birth')} />
              </div>
              <AuthField label="LOCATION (optional)" value={signupFields.location} onChange={set('location')} placeholder="City, Country" />
              <CvUploadField file={cvFile} onFile={setCvFile} />
              {error && <ErrorBanner msg={error} />}
              <button className="btn btn-primary" type="submit" disabled={loading} style={{ marginTop: 4 }}>
                {loading ? 'Creating account…' : 'Create account →'}
              </button>
            </form>
          )}
        </div>

        {/* Guest option */}
        <div style={{ textAlign: 'center' }}>
          <div className="t-mono" style={{ fontSize: 11, color: 'var(--muted)', letterSpacing: '0.1em', marginBottom: 10 }}>
            — OR —
          </div>
          <button className="btn btn-ghost" style={{ width: '100%', justifyContent: 'center' }} onClick={onGuestContinue}>
            Continue as guest →
          </button>
          <div style={{ marginTop: 10, fontSize: 11, color: 'var(--muted)' }}>
            Guest mode shows a limited preview. Sign up for full CV analysis.
          </div>
        </div>

      </div>
    </div>
  );
}
// -------------------- AuthScreen ------------- END ----------------

// -------------------- CvUploadField ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: AuthScreen signup form
function CvUploadField({ file, onFile }) {
  return (
    <div>
      <label style={LABEL}>CV / RESUME</label>
      <label style={{
        display: 'block', padding: '11px 14px',
        background: 'var(--ink-2)',
        border: `1px dashed ${file ? 'var(--accent)' : 'var(--border)'}`,
        borderRadius: 4, cursor: 'pointer', fontSize: 13,
        color: file ? 'var(--accent)' : 'var(--muted)', textAlign: 'center',
        transition: '120ms ease',
      }}>
        {file ? `✓ ${file.name}` : '+ Upload PDF, DOCX, or DOC'}
        <input type="file" accept=".pdf,.doc,.docx" style={{ display: 'none' }}
          onChange={e => onFile(e.target.files[0] || null)} />
      </label>
    </div>
  );
}
// -------------------- CvUploadField ------------- END ----------------

// -------------------- ErrorBanner ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: AuthScreen
function ErrorBanner({ msg }) {
  return (
    <div style={{
      padding: '9px 12px',
      background: 'oklch(0.30 0.10 25 / 0.25)',
      border: '1px solid var(--bad)', color: 'var(--bad)',
      borderRadius: 4, fontSize: 13,
    }}>⚠ {msg}</div>
  );
}
// -------------------- ErrorBanner ------------- END ----------------
