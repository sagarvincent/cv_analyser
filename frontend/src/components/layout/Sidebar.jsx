// Layer: 1 (layout) — composes brand, profile card, nav items, and footer
import { SidebarNavItem } from './SidebarNavItem';
import { useAuth } from '../../context/AuthContext';

// -------------------- Sidebar ----------- START ----------
// -- Calls : SidebarNavItem
// -- Called by: Dashboard
export function Sidebar({ profile, modules, activeId, setActiveId, onRestart, showProfile, setShowProfile }) {
  const { user, isGuest } = useAuth();
  const displayName = user?.full_name || profile?.cv?.name || (isGuest ? 'Guest' : 'Aria Chen');
  const displayRole = user?.experience?.[0]?.job_title || profile?.cv?.role || (isGuest ? 'Guest' : 'SR. PRODUCT DESIGNER');
  const displayYears = user?.experience?.length
    ? Math.max(1, Math.floor((Date.now() - new Date(user.experience.at(-1).joining_date)) / 3.156e10))
    : (profile?.cv?.years ?? (isGuest ? null : 8));

  return (
    <aside style={{
      borderRight: '1px solid var(--border)',
      background: 'var(--ink-2)',
      padding: '20px 0',
      display: 'flex', flexDirection: 'column',
      position: 'sticky', top: 0, height: '100vh',
    }}>
      {/* Brand */}
      <div style={{ padding: '8px 24px 24px', display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 28, height: 28, borderRadius: 4,
          background: 'var(--accent)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: 'var(--font-display)', fontStyle: 'italic', fontSize: 22, color: 'var(--ink)',
          boxShadow: '0 0 12px var(--accent-glow)',
        }}>S</div>
        <div style={{ lineHeight: 1 }}>
          <div className="t-display" style={{ fontSize: 22, fontStyle: 'italic' }}>Strata</div>
          <div className="t-mono" style={{ fontSize: 9, color: 'var(--muted)', letterSpacing: '0.16em', marginTop: 2 }}>
            CAREER INTELLIGENCE
          </div>
        </div>
      </div>

      {/* Profile card */}
      <button
        onClick={() => setShowProfile(true)}
        style={{
          textAlign: 'left', margin: '0 16px 18px', padding: '14px 14px',
          border: `1px solid ${showProfile ? 'var(--accent)' : 'var(--border)'}`, borderRadius: 6,
          background: showProfile ? 'var(--accent-glow)' : 'var(--surface)', color: 'inherit',
          cursor: 'pointer', transition: '150ms ease', width: 'calc(100% - 32px)',
          boxShadow: showProfile ? '0 0 12px var(--accent-glow)' : 'none',
        }}
      >
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <div style={{
            width: 36, height: 36, borderRadius: 99,
            background: 'linear-gradient(135deg, var(--accent), var(--violet))',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: 'var(--font-display)', fontSize: 16, color: 'var(--ink)', fontWeight: 500, fontStyle: 'italic',
          }}>{displayName[0]?.toUpperCase() || 'G'}</div>
          <div style={{ minWidth: 0, flex: 1 }}>
            <div style={{ fontSize: 13, fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {displayName}
            </div>
            <div className="t-mono" style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: '0.06em' }}>
              {displayRole.toUpperCase()}
            </div>
          </div>
          <span style={{ color: showProfile ? 'var(--accent)' : 'var(--muted)', fontSize: 12 }}>›</span>
        </div>
        <div className="hairline" style={{ margin: '12px -2px' }} />
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10.5, fontFamily: 'var(--font-mono)', color: 'var(--muted)', letterSpacing: '0.06em' }}>
          <span>{displayYears != null ? `${displayYears}Y EXP` : 'GUEST'}{!isGuest && ' · PRO'}</span>
          {isGuest
            ? <span style={{ color: 'var(--muted)' }}>○ GUEST</span>
            : <span style={{ color: 'var(--accent)' }}>● ANALYSED</span>
          }
        </div>
      </button>

      {/* Module list */}
      <nav style={{ flex: 1, padding: '0 12px', overflowY: 'auto' }} className="scroll-clean">
        <div className="t-label" style={{ padding: '8px 14px 10px' }}>LENSES</div>
        {modules.map((m) => (
          <SidebarNavItem key={m.id} module={m} isActive={m.id === activeId} onClick={() => setActiveId(m.id)} />
        ))}
      </nav>

      {/* Footer */}
      <div style={{ padding: '14px 22px 4px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', fontSize: 10, fontFamily: 'var(--font-mono)', color: 'var(--muted)', letterSpacing: '0.08em' }}>
        <span>STRATA v4.2.1</span>
        <span>● LIVE</span>
      </div>
      <div style={{ padding: '12px 18px 4px' }}>
        <button className="btn btn-ghost" style={{ width: '100%', justifyContent: 'center' }} onClick={onRestart}>
          ↻ NEW ANALYSIS
        </button>
      </div>
    </aside>
  );
}
//-------------------- Sidebar ------------- END ----------------
