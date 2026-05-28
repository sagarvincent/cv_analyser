// Layer: 1 — top-level orchestrator, mounts screens and wires global state
import { useState, useEffect } from 'react';
import { useTweaks } from './hooks/useTweaks';
import { Dashboard } from './components/layout/Dashboard';
import { AuthScreen } from './components/flow/AuthScreen';
import { UploadScreen } from './components/flow/UploadScreen';
import { AnalysisScreen } from './components/flow/AnalysisScreen';
import { TweaksPanel } from './components/devtools/TweaksPanel';
import { TweakSection } from './components/devtools/TweakSection';
import { TweakRadio } from './components/devtools/TweakRadio';
import { TweakButton } from './components/devtools/TweakButton';
import {
  OverviewModule, JDFitModule, SkillGapModule, AltPathsModule,
  ATSModule, PeerModule, CompModule, TrendsModule, AlignModule,
} from './components/modules';
import { MODULES, TWEAK_DEFAULTS, CHART_STYLE_BY_MODULE } from './data/mockData';
import { AnalysisProvider, useSetAnalysis } from './context/AnalysisContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import { appConfig } from './config/appConfig';

const MODULE_COMPONENTS = {
  overview: OverviewModule,
  jdfit:    JDFitModule,
  ats:      ATSModule,
  skills:   SkillGapModule,
  peer:     PeerModule,
  comp:     CompModule,
  paths:    AltPathsModule,
  trends:   TrendsModule,
  align:    AlignModule,
};

const NAV_ALIAS = { ats: 'ats', jdfit: 'jdfit', peer: 'peer', comp: 'comp', align: 'align', trends: 'trends' };

// -------------------- App ----------- START ----------
// -- Calls : AnalysisProvider, AuthProvider, AppRoot
// -- Called by: main.jsx
export default function App() {
  return (
    <AnalysisProvider>
      <AuthProvider>
        <AppRoot />
      </AuthProvider>
    </AnalysisProvider>
  );
}
// -------------------- App ------------- END ----------------

// -------------------- AppRoot ----------- START ----------
// -- Calls : restart, handleAuthComplete, handleGuestContinue, handleUploadComplete, handleAnalysisComplete
// -- Called by: App
function AppRoot() {
  const setAnalysis = useSetAnalysis();
  const { logout } = useAuth();
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [stage, setStage] = useState('auth');
  const [profile, setProfile] = useState(null);
  const [activeId, setActiveId] = useState('overview');
  const [showProfile, setShowProfile] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', t.theme);
    document.documentElement.setAttribute('data-density', t.density);
  }, [t.theme, t.density]);

  // -------------------- restart ----------- START ----------
  // -- Calls : logout
  // -- Called by: AppRoot, Dashboard (via onRestart), TweakButton
  const restart = () => { setStage('auth'); setProfile(null); logout(); };
  // -------------------- restart ------------- END ----------------

  // -------------------- handleAuthComplete ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: AuthScreen (after login or signup)
  const handleAuthComplete = () => { setStage('upload'); };
  // -------------------- handleAuthComplete ------------- END ----------------

  // -------------------- handleUploadComplete ----------- START ----------
  // -- Calls : setAnalysis
  // -- Called by: UploadScreen (via onComplete)
  const handleUploadComplete = (data) => {
    if (!appConfig.useMockData) setAnalysis(data);
    setProfile(data);
    setStage('analysing');
  };
  // -------------------- handleUploadComplete ------------- END ----------------

  // -------------------- handleAnalysisComplete ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: AnalysisScreen (via onComplete)
  const handleAnalysisComplete = () => { setStage('dashboard'); setActiveId('overview'); };
  // -------------------- handleAnalysisComplete ------------- END ----------------

  const ActiveModule = MODULE_COMPONENTS[activeId];
  const effectiveChartStyle = t.chartStyleOverride === 'auto'
    ? (CHART_STYLE_BY_MODULE[activeId] || 'blocks')
    : t.chartStyleOverride;

  return (
    <>
      {stage === 'auth' && (
        <AuthScreenWrapper
          onAuthComplete={handleAuthComplete}
          onGuestContinue={() => { setStage('dashboard'); setActiveId('overview'); }}
        />
      )}
      {stage === 'upload' && <UploadScreen onComplete={handleUploadComplete} />}
      {stage === 'analysing' && <AnalysisScreen onComplete={handleAnalysisComplete} />}
      {stage === 'dashboard' && (
        <Dashboard
          profile={profile}
          modules={MODULES}
          activeId={activeId}
          setActiveId={setActiveId}
          ActiveModule={ActiveModule}
          tweaks={t}
          effectiveChartStyle={effectiveChartStyle}
          onRestart={restart}
          onNav={(id) => setActiveId(NAV_ALIAS[id] || id)}
          showProfile={showProfile}
          setShowProfile={setShowProfile}
        />
      )}

      <TweaksPanel>
        <TweakSection label="Theme" />
        <TweakRadio label="Mode"    value={t.theme}   options={['dark', 'light']}              onChange={(v) => setTweak('theme', v)} />
        <TweakRadio label="Density" value={t.density} options={['compact', 'regular', 'comfy']} onChange={(v) => setTweak('density', v)} />
        <TweakSection label="Layout" />
        <TweakRadio label="Module layout" value={t.layout} options={['grid', 'list']} onChange={(v) => setTweak('layout', v)} />
        <TweakSection label="Charts" />
        <TweakRadio label="Chart style" value={t.chartStyleOverride} options={['auto', 'blocks', 'dots']} onChange={(v) => setTweak('chartStyleOverride', v)} />
        <TweakSection label="Flow" />
        <TweakButton label="Restart from upload" onClick={restart} />
      </TweaksPanel>
    </>
  );
}
// -------------------- AppRoot ------------- END ----------------

// -------------------- AuthScreenWrapper ----------- START ----------
// -- Calls : useAuth, AuthScreen
// -- Called by: AppRoot (ensures loginAsGuest is called within AuthProvider)
function AuthScreenWrapper({ onAuthComplete, onGuestContinue }) {
  const { loginAsGuest } = useAuth();
  return (
    <AuthScreen
      onAuthComplete={onAuthComplete}
      onGuestContinue={() => { loginAsGuest(); onGuestContinue(); }}
    />
  );
}
// -------------------- AuthScreenWrapper ------------- END ----------------
