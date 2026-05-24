# Strata — Frontend

React + Vite frontend for the Strata CV analysis platform.

## Architecture

The codebase enforces a strict **3-layer separation of concerns** at the file level. Every change to logic touches only utils; every change to UI touches only rendering files.

| Layer | Location | Rule |
|-------|----------|------|
| **Leaf (Layer 3)** | `src/utils/` | Pure functions. No JSX, no React hooks. Calculation, classification, geometry, formatting. |
| **Layer 2** | `src/components/charts/`, `src/components/ui/`, sub-component files | React components that render a single item or call leaf utils. No top-level data orchestration. |
| **Layer 1** | `src/components/modules/`, `src/components/layout/`, `src/components/flow/`, `src/App.jsx` | Screen-level composers. Map data arrays to Layer 2 sub-components. Minimal logic. |

Every function carries a call-graph comment so dependencies are self-documenting:

```js
// -------------------- FunctionName ----------- START ----------
// -- Calls : funcA, funcB   (or "nothing (leaf)")
// -- Called by: CallerA, CallerB
export function FunctionName(...) { ... }
//-------------------- FunctionName ------------- END ----------------
```

Every file declares its layer at the top:

```js
// Layer: 2 (chart sub-component) — renders one distribution bar
```

## Project Structure

```
frontend/src/
├── App.jsx                          # Layer 1 — mounts screens, wires global state
├── main.jsx
├── styles/
│   └── globals.css
├── data/
│   └── mockData.js                  # All mock data (single source of truth)
├── hooks/
│   └── useTweaks.js                 # Stateful settings hook
│
├── utils/                           # Layer 3 (Leaf) — pure calculation, no JSX
│   ├── animationUtils.js            # cubicEaseOut, springStep, clampNorm, calcRingGeometry,
│   │                                #   calcStepDuration, generateTraceId
│   ├── colorUtils.js                # toneToColor (good/warn/bad/muted → CSS var)
│   ├── alignUtils.js                # buildAlignRows, delta/tone/format helpers
│   ├── atsUtils.js                  # countPassedChecks
│   ├── careerNetworkUtils.js        # buildCareerNetworkLayout, placeOnRing,
│   │                                #   calcNodeRadius, resolveLinkEndpoints,
│   │                                #   calcLinkStrokeWidth, formatFitPct, colorForFit
│   ├── compBandUtils.js             # scaleCompValue, formatComp
│   ├── distributionUtils.js         # distributionBarFill, buildDistributionGeometry
│   ├── jdFitUtils.js                # formatStrengthPct, impactTone
│   ├── overviewUtils.js             # overviewCellBorders
│   ├── passwordUtils.js             # scorePassword
│   ├── peerUtils.js                 # formatPeerDelta
│   ├── radarUtils.js                # buildRadarGeometry, buildRadarPath, calcRadarPoint
│   ├── skillHeatmapUtils.js         # colorForSkill, calcCellPosition, calcDotRadius
│   └── sparklineUtils.js            # buildSparklineGeometry
│
└── components/
    ├── charts/                      # Layer 2 — SVG chart composers + atom sub-components
    │   ├── CareerNetwork.jsx        # composer: calls buildCareerNetworkLayout, maps to sub-components
    │   ├── CareerNetworkLink.jsx    # sub-component: one link line
    │   ├── CareerNetworkNode.jsx    # sub-component: one role node
    │   ├── CompBand.jsx             # salary band chart
    │   ├── Distribution.jsx         # composer: calls buildDistributionGeometry, maps to DistributionBar
    │   ├── DistributionBar.jsx      # sub-component: one bar or dot-stack column
    │   ├── Radar.jsx                # composer: calls buildRadarGeometry, maps to SVG elements
    │   ├── SkillHeatmap.jsx         # composer: maps cells to SkillHeatmapCell
    │   ├── SkillHeatmapCell.jsx     # sub-component: one heatmap cell (block or dot)
    │   └── index.js
    │
    ├── devtools/                    # Dev-only tweak panel (hidden in production)
    │   ├── TweaksPanel.jsx          # Layer 1 — draggable panel
    │   ├── TweakSection.jsx         # Layer 2
    │   ├── TweakRadio.jsx           # Layer 2
    │   └── TweakButton.jsx          # Layer 2
    │
    ├── flow/                        # Layer 1 — upload and analysis screens
    │   ├── UploadScreen.jsx         # CV + JD upload form
    │   ├── AnalysisScreen.jsx       # animated reasoning trace
    │   ├── CapabilityCell.jsx       # Layer 2 sub-component: one stat cell in capability strip
    │   └── TraceRow.jsx             # Layer 2 sub-component: one reasoning trace row
    │
    ├── layout/                      # Layer 1 — app chrome
    │   ├── Dashboard.jsx            # grid: Sidebar + TopBar + module panel
    │   ├── Sidebar.jsx              # brand + profile card + nav
    │   ├── SidebarNavItem.jsx       # Layer 2 sub-component: one nav button
    │   └── TopBar.jsx               # breadcrumb + controls
    │
    ├── modules/                     # Layer 1 — nine analysis module screens
    │   ├── OverviewModule.jsx       + OverviewMetricCard.jsx
    │   │                            + OverviewRecommendation.jsx
    │   │                            + OverviewMarketSignal.jsx
    │   ├── ATSModule.jsx            + ATSCheckItem.jsx
    │   ├── JDFitModule.jsx          + JDFitMatchItem.jsx + JDFitGapItem.jsx
    │   ├── AlignModule.jsx          + AlignRow.jsx
    │   ├── PeerModule.jsx           + PeerDimensionCard.jsx
    │   ├── CompModule.jsx           + CompRefCard.jsx
    │   ├── TrendsModule.jsx         + TrendItem.jsx
    │   ├── SkillGapModule.jsx       + SkillGapDeltaCard.jsx
    │   ├── AltPathsModule.jsx
    │   └── index.js
    │
    ├── profile/                     # Profile/settings page
    │   ├── ProfilePage.jsx          # Layer 1
    │   ├── Field.jsx                # Layer 2 — labelled input field
    │   ├── PwField.jsx              # Layer 2 — password input with toggle
    │   ├── PwStrength.jsx           # Layer 2 — password strength meter
    │   ├── Toggle.jsx               # Layer 2 — toggle switch
    │   └── Mini.jsx                 # Layer 2 — small stat badge
    │
    └── ui/                          # Layer 2 — shared UI atoms
        ├── Bar.jsx                  # horizontal progress bar (toneToColor, clampNorm)
        ├── Card.jsx                 # surface card wrapper
        ├── CountUp.jsx              # animated number (cubicEaseOut)
        ├── Insight.jsx              # insight blurb with tone accent
        ├── Pill.jsx                 # label badge
        ├── Ring.jsx                 # circular progress ring (calcRingGeometry, cubicEaseOut)
        ├── Spark.jsx                # sparkline (buildSparklineGeometry)
        ├── SectionHeader.jsx        # section title + optional action
        └── index.js
```

## Testing

### Running Tests

```bash
cd frontend
npm test               # run all tests once (verbose — each test case shown)
npm run test:watch     # watch mode for development
npm run test:coverage  # generate coverage report (coverage/index.html)
```

### Test Suite Summary

**19 test files · 213 test cases · 100% pass**

All tests live in [`test/frontend/`](../test/frontend/) (at the repo root) and mirror the `src/` structure.

#### Utility Tests (`test/frontend/utils/`) — 14 files, 168 tests

| File | Functions Covered | Tests |
|------|-------------------|-------|
| `animationUtils.test.js` | `cubicEaseOut`, `springStep`, `clampNorm`, `calcRingGeometry`, `calcStepDuration`, `generateTraceId` | 18 |
| `alignUtils.test.js` | `calcAlignDelta`, `alignDeltaTone`, `formatAlignDelta`, `buildAlignRows` | 17 |
| `careerNetworkUtils.test.js` | `colorForFit`, `findPlacedNode`, `placeOnRing`, `buildCareerNetworkLayout`, `calcNodeRadius`, `formatFitPct`, `resolveLinkEndpoints`, `calcLinkStrokeWidth` | 26 |
| `colorUtils.test.js` | `toneToColor` | 7 |
| `compBandUtils.test.js` | `scaleCompValue`, `formatComp` | 7 |
| `distributionUtils.test.js` | `distributionBarFill`, `buildDistributionGeometry` | 11 |
| `jdFitUtils.test.js` | `formatStrengthPct`, `impactTone` | 10 |
| `overviewUtils.test.js` | `overviewCellBorders` | 8 |
| `passwordUtils.test.js` | `scorePassword` | 9 |
| `peerUtils.test.js` | `formatPeerDelta` | 4 |
| `radarUtils.test.js` | `calcRadarAngle`, `calcRadarPoint`, `buildRadarPath`, `buildRadarGeometry` | 17 |
| `skillHeatmapUtils.test.js` | `colorForSkill`, `calcCellPosition`, `calcDotRadius` | 11 |
| `sparklineUtils.test.js` | `buildSparklineGeometry` | 7 |
| `atsUtils.test.js` | `countPassedChecks` | 4 |

#### Component Tests (`test/frontend/components/`) — 5 files, 45 tests

| File | Component | Tests |
|------|-----------|-------|
| `Pill.test.jsx` | `Pill` — tone modifier classes, dot class | 8 |
| `Card.test.jsx` | `Card` — header visibility, padding, className | 10 |
| `Insight.test.jsx` | `Insight` — quoted text, source rendering | 6 |
| `Bar.test.jsx` | `Bar` — width clamping, label rendering | 9 |
| `CountUp.test.jsx` | `CountUp` — animation, suffix, decimals | 6 |

### Test Infrastructure

- **Framework**: [Vitest](https://vitest.dev/) v4 (native Vite integration)
- **Component testing**: [@testing-library/react](https://testing-library.com/react) v16 + jsdom
- **Matchers**: `@testing-library/jest-dom`
- **Coverage**: `@vitest/coverage-v8` (provider: v8)
- **Coverage scope**: `src/utils/**` + `src/components/ui/**`

## Running Locally

```bash
cd frontend
npm install
npm run dev
```

The backend API is served separately; see the root `README.md` for Docker Compose setup.

## Contributing

Follow the layer rules to keep logic and UI independently changeable:

- **Adding a calculation, threshold, or formatter** → add or edit a file in `src/utils/` only. No JSX.
- **Changing a visual style or layout** → edit the relevant Layer 1 or Layer 2 component only. No logic.
- **Adding a new list item type** → create a Layer 2 sub-component, then call it from the parent Layer 1 composer via `.map()`.
- **All functions** must carry the call-graph comment template (START/END + Calls/Called-by).
- **File-level layer annotation** (`// Layer: N`) is required on every new file.
