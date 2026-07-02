// Layer: 2 — analysis data provider; no JSX body, wraps Layer 1 screens

import { createContext, useContext, useState } from 'react';

// Seeded only in dev_local. import.meta.env is replaced at build time so
// Rollup eliminates this block — and the mockData import — in other modes.
import * as mock from '../data/mockData';

const INITIAL_DATA = import.meta.env.VITE_APP_MODE === 'dev_local' ? {
  // Upload screen helpers
  sampleCv:                mock.SAMPLE_CV,
  sampleJd:                mock.SAMPLE_JD,
  capabilityStrip:         mock.CAPABILITY_STRIP,
  // Analysis animation
  reasoningTrace:          mock.REASONING_TRACE,
  // Overview
  overviewCards:           mock.overviewCards,
  overviewSummary:         mock.overviewSummary,
  overviewRecommendations: mock.overviewRecommendations,
  overviewInsight:         mock.overviewInsight,
  overviewMarketData:      mock.overviewMarketData,
  overviewVectorSignature: mock.overviewVectorSignature,
  // JD Fit
  jdFitSummary:            mock.jdFitSummary,
  jdFitMatches:            mock.jdFitMatches,
  jdFitGaps:               mock.jdFitGaps,
  // ATS
  atsSummary:              mock.atsSummary,
  atsChecks:               mock.atsChecks,
  // Skill Matrix
  skillMatrixSummary:      mock.skillMatrixSummary,
  skillMatrixCategories:   mock.skillMatrixCategories,
  skillMatrixCohorts:      mock.skillMatrixCohorts,
  skillMatrixData:         mock.skillMatrixData,
  skillMatrixDeltaCards:   mock.skillMatrixDeltaCards,
  // Alt Paths
  altPathsSummary:         mock.altPathsSummary,
  altPathsCenter:          mock.altPathsCenter,
  altPathsNodes:           mock.altPathsNodes,
  altPathsLinks:           mock.altPathsLinks,
  altPathsInsight:         mock.altPathsInsight,
  // Peer
  peerSummary:             mock.peerSummary,
  peerBuckets:             mock.peerBuckets,
  peerYouBucket:           mock.peerYouBucket,
  peerP50Bucket:           mock.peerP50Bucket,
  peerDimensions:          mock.peerDimensions,
  // Comp
  compSummary:             mock.compSummary,
  compBandData:            mock.compBandData,
  compRefCards:            mock.compRefCards,
  // Trends
  trendsSummary:           mock.trendsSummary,
  trendRising:             mock.trendRising,
  trendFalling:            mock.trendFalling,
  trendsInsight:           mock.trendsInsight,
  // Align
  alignSummary:            mock.alignSummary,
  alignAxes:               mock.alignAxes,
  alignYou:                mock.alignYou,
  alignMarket:             mock.alignMarket,
  // Profile
  profileAccountFields:    mock.profileAccountFields,
  profileAccountStats:     mock.profileAccountStats,
  profileSessions:         mock.profileSessions,
  profileDataStats:        mock.profileDataStats,
  profileToggles:          mock.profileToggles,
  profileDeletionDate:     mock.profileDeletionDate,
  profileLastUpdated:      mock.profileLastUpdated,
} : null;

const AnalysisContext = createContext(null);

// -------------------- AnalysisProvider ----------- START ----------
// -- Calls : nothing (leaf — provides context value)
// -- Called by: App
export function AnalysisProvider({ children }) {
  const [data, setData] = useState(INITIAL_DATA);
  return (
    <AnalysisContext.Provider value={{ data, setData }}>
      {children}
    </AnalysisContext.Provider>
  );
}
// -------------------- AnalysisProvider ------------- END ----------------

// -------------------- useAnalysis ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: all module screens, AnalysisScreen, UploadScreen, ProfilePage
export function useAnalysis() {
  const ctx = useContext(AnalysisContext);
  if (!ctx) throw new Error('useAnalysis must be used within AnalysisProvider');
  return ctx.data || {};
}
// -------------------- useAnalysis ------------- END ----------------

// -------------------- useSetAnalysis ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: AppRoot to populate context from API response
export function useSetAnalysis() {
  const ctx = useContext(AnalysisContext);
  if (!ctx) throw new Error('useSetAnalysis must be used within AnalysisProvider');
  return ctx.setData;
}
// -------------------- useSetAnalysis ------------- END ----------------
