// Layer: 1 — screen orchestrator, composes Sidebar + TopBar + active module
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { ProfilePage } from '../profile/ProfilePage';

// -------------------- Dashboard ----------- START ----------
// -- Calls : Sidebar, TopBar, ProfilePage
// -- Called by: App
export function Dashboard({ profile, modules, activeId, setActiveId, ActiveModule, tweaks, effectiveChartStyle, onRestart, onNav, showProfile, setShowProfile }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', minHeight: '100vh' }}>
      <Sidebar
        profile={profile}
        modules={modules}
        activeId={activeId}
        setActiveId={(id) => { setShowProfile(false); setActiveId(id); }}
        onRestart={onRestart}
        showProfile={showProfile}
        setShowProfile={setShowProfile}
      />
      <main style={{ minWidth: 0, background: 'var(--ink)' }}>
        <TopBar profile={profile} active={modules.find(m => m.id === activeId)} showProfile={showProfile} />
        <div
          style={{ padding: showProfile ? 0 : '36px 48px 80px', maxWidth: 1340, margin: '0 auto' }}
          key={showProfile ? 'profile' : activeId}
        >
          {showProfile ? (
            <ProfilePage profile={profile} onBack={() => setShowProfile(false)} />
          ) : ActiveModule ? (
            <ActiveModule
              profile={profile}
              layout={tweaks.layout}
              chartStyle={effectiveChartStyle}
              onNav={onNav}
            />
          ) : null}
        </div>
      </main>
    </div>
  );
}
//-------------------- Dashboard ------------- END ----------------
