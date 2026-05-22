// Layer: 1 — top-level orchestrator, mounts screens and wires global state
import { useState, useEffect } from 'react';
import { useTweaks } from './hooks/useTweaks';
import { Dashboard } from './components/layout/Dashboard';
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
// -- Calls : restart, handleUploadComplete, handleAnalysisComplete, useTweaks, Dashboard, UploadScreen, AnalysisScreen, TweaksPanel, TweakSection, TweakRadio, TweakButton
// -- Called by: main.jsx
export default function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [stage, setStage] = useState(t.startScreen === 'upload' ? 'upload' : 'dashboard');
  const [profile, setProfile] = useState(null);
  const [activeId, setActiveId] = useState('overview');
  const [showProfile, setShowProfile] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', t.theme);
    document.documentElement.setAttribute('data-density', t.density);
  }, [t.theme, t.density]);

  // -------------------- restart ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: App, Dashboard (via onRestart), TweakButton
  const restart = () => { setStage('upload'); setProfile(null); };
  //-------------------- restart ------------- END ----------------

  // -------------------- handleUploadComplete ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: UploadScreen (via onComplete)
  const handleUploadComplete = (p) => { setProfile(p); setStage('analysing'); };
  //-------------------- handleUploadComplete ------------- END ----------------

  // -------------------- handleAnalysisComplete ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: AnalysisScreen (via onComplete)
  const handleAnalysisComplete = () => { setStage('dashboard'); setActiveId('overview'); };
  //-------------------- handleAnalysisComplete ------------- END ----------------

  const ActiveModule = MODULE_COMPONENTS[activeId];
  const effectiveChartStyle = t.chartStyleOverride === 'auto'
    ? (CHART_STYLE_BY_MODULE[activeId] || 'blocks')
    : t.chartStyleOverride;

  return (
    <>
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
//-------------------- App ------------- END ----------------
