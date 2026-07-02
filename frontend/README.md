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
├── config/
│   └── appConfig.js                 # Mode-aware config (apiBaseUrl, useMockData)
├── context/
│   └── AnalysisContext.jsx          # Analysis data provider + useAnalysis / useSetAnalysis hooks
├── data/
│   └── mockData.js                  # Mock data — consumed only in dev_local mode
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

## API Endpoints

All requests are routed through `/api`. In `dev_cluster` the Vite dev server proxies `/api` to `VITE_DEV_BACKEND_URL`; in `production` the frontend calls `VITE_API_BASE_URL` directly.

### Analysis

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/analyze` | Submit a CV and optional JD; returns the full analysis result |

**Request** — `multipart/form-data`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `cv` | file | yes | PDF, DOCX, or DOC, max 16 MB |
| `jd` | string | no | Raw job-description text; omit for a general market analysis |

**Response** — `application/json`

The response object is consumed directly by `AnalysisContext` and distributed to every module. All keys are required unless marked optional.

```jsonc
{
  // Reasoning trace shown during the analysis animation (optional)
  "reasoningTrace": [{ "label": "…", "detail": "…", "ms": 120 }],

  // Overview module
  "overviewSummary":         { "eyebrow": "…", "titleStrong": "…", "titleRest": "…", "body": "…" },
  "overviewCards":           [{ "id": "…", "label": "…", "value": "…", "sub": "…", "tone": "good|warn|bad" }],
  "overviewRecommendations": [{ "n": 1, "title": "…", "body": "…", "impact": "…" }],
  "overviewInsight":         { "text": "…", "source": "…" },
  "overviewMarketData":      { "openRoles": 0, "openRolesTrend": "…", "openRolesChange": "…",
                               "applicantsPerRole": 0, "applicantsTrend": "…", "applicantsChange": "…",
                               "commentary": "…" },
  "overviewVectorSignature": { "model": "…", "preview": "…", "dims": 0, "cohort": "…" },

  // JD Fit module (only present when a JD was submitted)
  "jdFitSummary":  { "eyebrow": "…", "titleReach": "…", "titleRest": "…", "sub": "…",
                     "score": 0, "evidencedMatches": 0, "totalRequirements": 0,
                     "gapsFlagged": 0, "gapBreakdown": "…", "keywordDensity": 0 },
  "jdFitMatches":  [{ "req": "…", "evidence": "…", "strength": 0 }],
  "jdFitGaps":     [{ "req": "…", "impact": "…", "fix": "…" }],

  // ATS module
  "atsSummary": { "eyebrow": "…", "titleScore": "…", "titleRest": "…", "sub": "…",
                  "score": 0, "dwellTime": "…", "normDwellTime": "…" },
  "atsChecks":  [{ "label": "…", "passed": true, "note": "…" }],

  // Skill Matrix module (BES04 — bucket → JD categories → semantic score)
  "skillMatrixSummary":    { "eyebrow": "…", "bucket": "…", "overIndexTopic": "…", "underIndexTopic": "…", "sub": "…" },
  "skillMatrixCategories": ["…"],
  "skillMatrixCohorts":    ["YOU", "JD ASK", "BUCKET NORM", "PEER P50"],
  "skillMatrixData":       [[0]],
  "skillMatrixDeltaCards": [{ "label": "…", "topic": "…", "delta": "…", "color": "…", "note": "…" }],

  // Alternative Paths module
  "altPathsSummary": { "eyebrow": "…", "titleWarn": "…", "titleRest": "…", "sub": "…" },
  "altPathsCenter":  { "id": "…", "label": "…", "fit": 0 },
  "altPathsNodes":   [{ "id": "…", "label": "…", "fit": 0, "ring": 0 }],
  "altPathsLinks":   [{ "source": "…", "target": "…" }],
  "altPathsInsight": { "text": "…", "source": "…" },

  // Peer Benchmark module
  "peerSummary":    { "eyebrow": "…", "titlePercentile": "…", "sub": "…" },
  "peerBuckets":    [{ "lo": 0, "hi": 0, "count": 0 }],
  "peerYouBucket":  { "lo": 0, "hi": 0 },
  "peerP50Bucket":  { "lo": 0, "hi": 0 },
  "peerDimensions": [{ "dim": "…", "you": 0, "p50": 0, "p90": 0 }],

  // Compensation module
  "compSummary":  { "eyebrow": "…", "titleUnderpaid": "…", "sub": "…", "bandTitle": "…" },
  "compBandData": { "min": 0, "p25": 0, "median": 0, "p75": 0, "max": 0, "you": 0 },
  "compRefCards": [{ "label": "…", "value": "…", "sub": "…" }],

  // Trends module
  "trendsSummary": { "eyebrow": "…", "titleGrowing": "…", "sub": "…" },
  "trendRising":   [{ "topic": "…", "delta": 0, "note": "…" }],
  "trendFalling":  [{ "topic": "…", "delta": 0, "note": "…" }],
  "trendsInsight": { "text": "…", "source": "…" },

  // Alignment module
  "alignSummary": { "eyebrow": "…", "titleAccent": "…", "titleWarn": "…", "sub": "…" },
  "alignAxes":    ["…"],
  "alignYou":     [0],
  "alignMarket":  [0]
}
```

---

### User Profile

Implemented in `API/user_profile/interface.py`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/profile/{username}` | Fetch a user's profile |
| `POST` | `/api/profile/` | Create a new profile (registration) |
| `PATCH` | `/api/profile/{username}` | Update account information |
| `POST` | `/api/profile/{username}/password` | Change password |
| `DELETE` | `/api/profile/{username}/sessions/{sessionId}` | Revoke an active session |
| `DELETE` | `/api/profile/{username}` | Permanently delete account |

**`POST /api/profile/`** — `multipart/form-data`

| Field | Type | Required |
|-------|------|----------|
| `username` | string | yes |
| `email` | string | yes |
| `password_hash` | string | yes |
| `full_name` | string | yes |
| `date_of_birth` | string `YYYY-MM-DD` | yes |
| `location` | string | no |
| `cv` | file | yes |

**Profile response shape** (`GET` and `POST` return the same model)

```jsonc
{
  "username": "…",
  "email": "…",
  "full_name": "…",
  "date_of_birth": "YYYY-MM-DD",
  "location": "…",
  "created_at": "ISO-8601",
  // fields below map to the ProfilePage UI
  "profileAccountStats":  [{ "label": "…", "value": "…", "sub": "…" }],
  "profileSessions":      [{ "device": "…", "loc": "…", "when": "…", "current": true }],
  "profileDataStats":     [{ "label": "…", "value": "…" }],
  "profileToggles":       [{ "label": "…", "description": "…", "enabled": true }],
  "profileDeletionDate":  "…",
  "profileLastUpdated":   "…"
}
```

---

### Data & Privacy

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/profile/{username}/export` | Export all user data as JSON |
| `GET` | `/api/profile/{username}/export/pdf` | Export all analyses as a PDF bundle |
| `DELETE` | `/api/profile/{username}/data` | Purge all stored CV and analysis data |

---

## Running Locally

```bash
cd frontend
npm install
npm run dev:local    # dev_local  — mock data, no backend required
npm run dev:cluster  # dev_cluster — proxies /api to VITE_DEV_BACKEND_URL (default localhost:5000)
npm run build        # production build, uses VITE_API_BASE_URL
```

### Modes

| Script | Mode | Data source | Proxy |
|--------|------|-------------|-------|
| `dev:local` | `dev_local` | `mockData.js` via `AnalysisContext` | none |
| `dev:cluster` | `dev_cluster` | Live backend (docker-compose) | `/api` → `VITE_DEV_BACKEND_URL` |
| `build` | `production` | Live backend | none (direct `VITE_API_BASE_URL`) |

Configure each mode by editing the corresponding `.env.<mode>` file at `frontend/`.

The backend API is served separately; see the root `README.md` for Docker Compose setup.

## Contributing

Follow the layer rules to keep logic and UI independently changeable:

- **Adding a calculation, threshold, or formatter** → add or edit a file in `src/utils/` only. No JSX.
- **Changing a visual style or layout** → edit the relevant Layer 1 or Layer 2 component only. No logic.
- **Adding a new list item type** → create a Layer 2 sub-component, then call it from the parent Layer 1 composer via `.map()`.
- **All functions** must carry the call-graph comment template (START/END + Calls/Called-by).
- **File-level layer annotation** (`// Layer: N`) is required on every new file.
