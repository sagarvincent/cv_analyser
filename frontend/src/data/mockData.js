// ─────────────────────────────────────────────────────────────
// STRATA — Central mock data store
// Edit this file to change any displayed content in the app.
// ─────────────────────────────────────────────────────────────

// ── App config ────────────────────────────────────────────────
export const TWEAK_DEFAULTS = {
  theme: 'dark',
  density: 'regular',
  layout: 'grid',
  chartStyleOverride: 'auto',
  startScreen: 'dashboard',
};

export const CHART_STYLE_BY_MODULE = {
  paths: 'dots',
  jdfit: 'blocks',
  ats: 'blocks',
  skills: 'blocks',
  peer: 'blocks',
  comp: 'blocks',
  trends: 'blocks',
  align: 'blocks',
  overview: 'blocks',
};

export const MODULES = [
  { id: 'overview', label: 'Overview',          code: '00' },
  { id: 'jdfit',    label: 'JD Fit',            code: '01' },
  { id: 'ats',      label: 'ATS Readability',   code: '02' },
  { id: 'skills',   label: 'Skill Matrix',      code: '03' },
  { id: 'peer',     label: 'Peer Benchmark',    code: '04' },
  { id: 'comp',     label: 'Compensation',      code: '05' },
  { id: 'paths',    label: 'Alternative Paths', code: '06' },
  { id: 'trends',   label: 'Market Trends',     code: '07' },
  { id: 'align',    label: 'Market Alignment',  code: '08' },
];

// ── Upload / Analysis flow ─────────────────────────────────────
export const SAMPLE_CV = {
  name: 'Aria Chen',
  role: 'Senior Product Designer',
  years: 8,
  company: 'Lumina Health',
  file: 'aria-chen-cv.pdf',
};

export const SAMPLE_JD = `Director of Product Design — fintech scale-up, Series C
We're looking for a design leader to own end-to-end product design for our consumer wealth platform. 8+ years experience, 3+ leading teams. Strong systems thinking, comfortable with quantitative product work, partnership with PM & Eng leadership at the executive level. Bonus: regulated-industry experience, design system stewardship, hiring at scale.`;

export const CAPABILITY_STRIP = [
  ['2.4M', 'PROFILES INDEXED'],
  ['180K', 'LIVE POSTINGS'],
  ['320',  'MARKETS TRACKED'],
  ['14s',  'MEDIAN ANALYSIS'],
];

export const REASONING_TRACE = [
  { stage: 'INGEST',    text: 'Parsing CV structure · 3 employers · 14 projects · 47 skills detected' },
  { stage: 'INGEST',    text: 'Extracting JD signal · seniority=Director · domain=fintech · scope=consumer' },
  { stage: 'EMBED',     text: 'Encoding profile into 1536-d career-space vector · model: strata-emb-3' },
  { stage: 'MATCH',     text: 'Cross-referencing against 2,438,221 peer profiles · k=128 nearest neighbors' },
  { stage: 'MATCH',     text: 'Locating you on the design-leadership trajectory · cohort: Sr.→Dir transition' },
  { stage: 'MARKET',    text: 'Pulling 14-day rolling demand for ~Director, Product Design~ · n=412 postings' },
  { stage: 'MARKET',    text: 'Compensation distribution converged · σ=22%, p50=$214k, p90=$281k' },
  { stage: 'FIT',       text: 'Running JD↔CV semantic alignment · 12 evidence-backed matches, 4 gaps flagged' },
  { stage: 'FIT',       text: 'ATS readability simulation · keyword density 64%, structural risk: LOW' },
  { stage: 'GAP',       text: 'Surfacing the 3 highest-leverage skills missing · ranked by salary delta' },
  { stage: 'PATHS',     text: "Mapping 6 adjacent roles you'd ladder into · weighted by market liquidity" },
  { stage: 'SYNTHESIS', text: 'Assembling brief · drafting executive summary · finalizing recommendations' },
];

// ── Overview module ────────────────────────────────────────────
export const overviewCards = [
  { id: 'jdfit',  label: 'JD FIT',          value: 78, suffix: '/100', tone: 'warn',   sub: '12 matches · 4 gaps' },
  { id: 'ats',    label: 'ATS SCORE',       value: 91, suffix: '/100', tone: 'good',   sub: 'Top 7% structural clarity' },
  { id: 'peer',   label: 'PEER PERCENTILE', value: 84, suffix: 'p',    tone: 'accent', sub: 'vs 12,400 similar profiles' },
  { id: 'comp',   label: 'COMP POSITION',   value: 62, suffix: 'p',    tone: 'warn',   sub: '$8k below market median' },
  { id: 'align',  label: 'MARKET ALIGN',    value: 71, suffix: '%',    tone: 'warn',   sub: 'Demand cooling in 2 of 5 sk.' },
  { id: 'trends', label: 'MOMENTUM',        value: 'B+', suffix: '',   tone: 'accent', sub: 'Field growth: +14% YoY' },
];

export const overviewSummary = {
  eyebrow: 'Executive brief · 0x4A7F2',
  titleStrong: 'well-positioned',
  titleRest: 'but underpaid.',
  body: "Across the eight lenses, you outrank 84% of peer profiles for the Director, Product Design transition. Your compensation sits 8 points below market median, your strongest gap is regulated-industry experience, and your highest-leverage adjacent path is Head of Design Systems.",
};

export const overviewRecommendations = [
  {
    n: '01',
    title: 'Quantify your design-system stewardship.',
    body: 'You led the Lumina DS but never put numbers on adoption. Add: ~80% screen coverage, 14 squads consuming, 31% velocity uplift. Estimated JD fit gain: +9.',
    tag: '+9 JD FIT',
  },
  {
    n: '02',
    title: 'Acquire one regulated-industry artifact.',
    body: 'Healthcare counts, but JD-language reads as fintech-first. A short consulting engagement, a compliance-flavoured case study, or an SEC/FINRA writing sample closes the gap.',
    tag: '+12 ALIGN',
  },
  {
    n: '03',
    title: 'Re-price yourself before negotiating.',
    body: 'Your current band is $186–198k. Comparable Dir-track ICs in NYC/SF fintech sit at $214k p50, $246k p75. You\'re leaving $16–48k on the table.',
    tag: '+$28K',
  },
];

export const overviewInsight = {
  text: 'You design like a Director already. The market just doesn\'t have the receipts yet.',
  source: 'STRATA SYNTHESIS · 14:02 UTC',
};

export const overviewMarketData = {
  openRoles: 412,
  openRolesTrend: [40, 52, 48, 60, 72, 81, 92],
  openRolesChange: '+14% / 30d',
  applicantsPerRole: 48,
  applicantsTrend: [28, 32, 35, 41, 44, 46, 48],
  applicantsChange: '+71% / 30d',
  commentary: 'Hiring is up — but so is competition. Apply selectively; the top 5% of openings absorb most of the qualified flow.',
};

export const overviewVectorSignature = {
  model: 'strata-v3',
  preview: '[0.842, -0.193, 0.667, 0.412, -0.038,\n 0.221, 0.901, -0.114, 0.473, 0.589,\n 0.318, -0.247, 0.802, 0.155, 0.694,\n -0.052, 0.398, 0.741, 0.286, 0.633…]',
  dims: '1,536',
  cohort: 'SR.DESIGNER.PRODUCT_LED.B2C2B',
};

// ── JD Fit module ──────────────────────────────────────────────
export const jdFitSummary = {
  eyebrow: 'JD↔CV Alignment · target role match',
  titleReach: 'within reach',
  titleRest: '— with three concrete moves.',
  sub: 'Director of Product Design · fintech scale-up · Series C',
  score: 78,
  evidencedMatches: 12,
  totalRequirements: 16,
  gapsFlagged: 4,
  gapBreakdown: '1 high · 2 med · 1 low',
  keywordDensity: 64,
};

export const jdFitMatches = [
  { topic: 'Design leadership (3+ yrs leading)', evidence: 'Led 6-person design pod at Lumina',         strength: 0.92 },
  { topic: 'Systems thinking',                   evidence: 'Owned Lumina Design System v1→v3',          strength: 0.95 },
  { topic: 'Consumer-facing surface',            evidence: 'Patient-facing app, 1.2M MAU',              strength: 0.86 },
  { topic: 'Cross-functional partnership',       evidence: 'Joint OKRs with PM + Eng',                  strength: 0.81 },
  { topic: 'Quantitative product work',          evidence: 'Drove 18% activation lift via A/B program', strength: 0.74 },
];

export const jdFitGaps = [
  { topic: 'Regulated fintech experience',  impact: 'HIGH', note: 'Your domain (healthcare) signals adjacent regulatory fluency, but JD language indexes fintech-first.' },
  { topic: 'Executive-level partnership',   impact: 'MED',  note: 'Reports-to suggests CPO; your last skip-level was VP. Show one C-suite presentation.' },
  { topic: 'Hiring at scale',               impact: 'MED',  note: 'You\'ve hired 4. JD asks for \'team building to 20+\'. Lean into your hiring rubric work.' },
  { topic: 'Wealth / investing fluency',    impact: 'LOW',  note: 'Not blocking — but a domain artefact would help.' },
];

// ── Skill Gap module ───────────────────────────────────────────
export const skillGapSummary = {
  eyebrow: 'Skill Matrix · cohort = Sr→Dir design leadership',
  overIndexTopic: 'craft',
  underIndexTopic: 'compliance',
  sub: 'The matrix below ranks you against four reference tracks. The largest negative deltas — strategy and regulatory fluency — are the levers worth pulling.',
};

export const skillGapSkills = [
  'Design Systems', 'Research', 'Prototyping', 'Strategy',
  'Hiring', 'Data/Analytics', 'Storytelling', 'Compliance/Reg',
];

export const skillGapTracks = ['YOU', 'PEER P50', 'PEER P90', 'JD ASK', 'DIRECTOR TIER'];

export const skillGapData = [
  [0.95, 0.72, 0.91, 0.85, 0.70],
  [0.78, 0.68, 0.84, 0.65, 0.68],
  [0.88, 0.74, 0.82, 0.55, 0.58],
  [0.72, 0.62, 0.86, 0.88, 0.92],
  [0.55, 0.50, 0.78, 0.82, 0.85],
  [0.62, 0.58, 0.80, 0.75, 0.82],
  [0.85, 0.68, 0.78, 0.72, 0.85],
  [0.28, 0.45, 0.62, 0.75, 0.70],
];

export const skillGapDeltaCards = [
  { label: 'BIGGEST OVER-INDEX',  topic: 'Design Systems', delta: '+27', color: 'var(--good)',   note: 'You sit 27 points above peer P50 — your strongest weapon when negotiating.' },
  { label: 'BIGGEST UNDER-INDEX', topic: 'Compliance/Reg', delta: '−42', color: 'var(--bad)',    note: 'Closing this gap by 20 pts roughly doubles your fintech-Director shortlist surface.' },
  { label: 'MOST UNDERVALUED',    topic: 'Storytelling',   delta: '+13', color: 'var(--accent)', note: 'Strong but invisible — your CV under-narrates impact. Re-frame three bullets.' },
];

// ── Alt Paths module ───────────────────────────────────────────
export const altPathsSummary = {
  eyebrow: 'Career Topology · adjacent roles, ranked by fit × market liquidity',
  titleWarn: 'not',
  titleRest: ' your strongest move.',
  sub: 'Head of Design Systems lands a higher fit (91 vs 78), pays $18k more, and has 2.3× the open-role density right now. The ring map below shows the trajectories — inner ring is one career hop, outer ring is two.',
};

export const altPathsCenter = { title: 'Sr. Product Designer' };

export const altPathsNodes = [
  { id: 'n1',  title: 'Director, Product Design',    fit: 0.78, salary: '$214k', ring: 1 },
  { id: 'n2',  title: 'Head of Design Systems',      fit: 0.91, salary: '$232k', ring: 1 },
  { id: 'n3',  title: 'Principal IC Designer',       fit: 0.88, salary: '$226k', ring: 1 },
  { id: 'n4',  title: 'Design Manager',              fit: 0.83, salary: '$198k', ring: 1 },
  { id: 'n5',  title: 'Staff Product Designer',      fit: 0.86, salary: '$218k', ring: 1 },
  { id: 'n6',  title: 'VP Design',                   fit: 0.52, salary: '$298k', ring: 2 },
  { id: 'n7',  title: 'Founding Designer (early)',   fit: 0.74, salary: '+equity', ring: 2 },
  { id: 'n8',  title: 'Design Partner (VC)',         fit: 0.62, salary: '$262k', ring: 2 },
  { id: 'n9',  title: 'Chief of Staff (Product)',    fit: 0.58, salary: '$240k', ring: 2 },
  { id: 'n10', title: 'Director of UX Research',     fit: 0.45, salary: '$192k', ring: 2 },
];

export const altPathsLinks = [
  { from: 'center', to: 'n1',  fit: 0.78 },
  { from: 'center', to: 'n2',  fit: 0.91 },
  { from: 'center', to: 'n3',  fit: 0.88 },
  { from: 'center', to: 'n4',  fit: 0.83 },
  { from: 'center', to: 'n5',  fit: 0.86 },
  { from: 'n1',     to: 'n6',  fit: 0.52 },
  { from: 'n2',     to: 'n7',  fit: 0.74 },
  { from: 'n4',     to: 'n8',  fit: 0.62 },
  { from: 'n3',     to: 'n9',  fit: 0.58 },
  { from: 'n5',     to: 'n10', fit: 0.45 },
];

export const altPathsInsight = {
  text: 'Optimise for the role you\'d be best at, not the one with the biggest title. Head of Design Systems is the answer this engine keeps returning.',
  source: 'STRATA · PATH SYNTHESIS',
};

// ── ATS module ─────────────────────────────────────────────────
export const atsSummary = {
  eyebrow: 'ATS & Recruiter Readability',
  titleScore: '91/100.',
  titleRest: ' Machines love your CV. Humans need more numbers.',
  sub: 'Structural parsing is essentially perfect. The two failures are content-level — weak verb leads and under-quantification. Fixing both takes about 40 minutes and lifts recruiter dwell-time materially.',
  score: 91,
  dwellTime: '32s',
  normDwellTime: '7s',
};

export const atsChecks = [
  { label: 'Parseable structure (sections, dates, contact)', pass: true,  note: 'Clean. All 4 employers parsed, all date ranges valid.' },
  { label: 'Standard section headers',                       pass: true,  note: 'EXPERIENCE / EDUCATION / SKILLS — recognised.' },
  { label: 'No images / icons / multi-column layout',        pass: true,  note: 'Single-column. ATS-safe.' },
  { label: 'Job titles match common taxonomy',               pass: true,  note: 'All 4 titles normalise to standard ESCO codes.' },
  { label: 'Keyword density vs target JD',                   pass: true,  note: '64% — above 60% threshold.' },
  { label: 'Action-verb leading bullets',                    pass: false, note: '12 of 47 bullets start with weak verbs (managed, helped, worked on).' },
  { label: 'Quantified outcomes',                            pass: false, note: 'Only 19/47 bullets carry a number. Target ≥ 60%.' },
  { label: 'Skill section taxonomy match',                   pass: true,  note: '37/41 skills mapped to canonical taxonomy.' },
];

// ── Peer Benchmark module ──────────────────────────────────────
export const peerSummary = {
  eyebrow: 'Peer Benchmarking · n = 12,438 similar profiles',
  titlePercentile: '84th percentile.',
  sub: 'Of profiles with comparable seniority, domain, and trajectory, ~16% outrank you. Within your own employer cohort (healthtech-to-fintech transitioners), you\'re in the top 9%.',
};

// Bimodal-ish distribution; "you" are in bucket index 12 of 16
export const peerBuckets = [12, 28, 44, 68, 96, 142, 188, 222, 248, 232, 198, 154, 112, 76, 44, 18];
export const peerYouBucket = 12;
export const peerP50Bucket = 8;

export const peerDimensions = [
  { dim: 'Tenure',   you: 78, p50: 64 },
  { dim: 'Mobility', you: 91, p50: 58 },
  { dim: 'Impact',   you: 82, p50: 70 },
  { dim: 'Breadth',  you: 86, p50: 68 },
];

// ── Compensation module ────────────────────────────────────────
export const compSummary = {
  eyebrow: 'Compensation Intelligence · n = 1,840 verified offers · last 90 days',
  titleUnderpaid: '$28k.',
  sub: "Your current $186k base sits below the p25 of comparable roles in your two strongest markets. The asymmetric move: don't ask for a raise — interview for a Director-track Staff role and let the market re-price you.",
  bandTitle: 'Total comp · Sr. Product Designer · NYC/SF · fintech',
};

export const compBandData = {
  min: 150000,
  p25: 196000,
  p50: 214000,
  p75: 238000,
  max: 285000,
  you: 186000,
};

export const compRefCards = [
  { label: 'MARKET MEDIAN', value: '$214k', sub: '+$28k vs your base',    tone: 'good'   },
  { label: 'TARGET (DIR)',  value: '$262k', sub: 'Realistic 12-mo target', tone: 'accent' },
  { label: 'EQUITY WEIGHT', value: '0.18',  sub: 'Cash-heavy vs cohort',   tone: 'warn'   },
];

// ── Market Trends module ───────────────────────────────────────
export const trendsSummary = {
  eyebrow: 'Field Momentum · 6-month rolling demand',
  titleGrowing: 'growing',
  sub: 'The shape of design hiring has reorganised around three poles: AI-native product, design engineering, and systems leadership. Two adjacent disciplines have contracted sharply.',
};

export const trendRising = [
  { topic: 'AI-native product design', delta: '+148%', spark: [10, 14, 22, 38, 64, 102, 148], note: 'From niche to mandatory in 9 months.' },
  { topic: 'Design engineering',       delta: '+62%',  spark: [40, 48, 52, 64, 78, 92, 102],  note: 'Hybrid IC role with the strongest comp inflation.' },
  { topic: 'Design systems lead',      delta: '+34%',  spark: [60, 64, 70, 78, 82, 88, 94],   note: 'Steady, defensible, undersupplied.' },
];

export const trendFalling = [
  { topic: 'Visual / brand designer', delta: '−28%', spark: [100, 96, 88, 78, 72, 66, 58], note: 'Compressed by tool-driven craft uplift.' },
  { topic: 'UX writer (standalone)',  delta: '−41%', spark: [100, 92, 78, 64, 52, 44, 38], note: 'Folded into PM/PD or AI-assisted.' },
];

export const trendsInsight = {
  text: "If your CV doesn't mention how you've thought about AI in the product surface, it reads three years older than it should.",
  source: 'STRATA · TREND SYNTHESIS',
};

// ── Market Alignment module ────────────────────────────────────
export const alignSummary = {
  eyebrow: 'Market Alignment · how today\'s market values you',
  titleAccent: 'scarcity',
  titleWarn: 'demand',
  sub: 'The radar contrasts your profile shape (filled) with where the market is investing fastest (dashed). The gap on demand is closeable in one quarter; the gap on comp is closed via the move you make, not the skill you add.',
};

export const alignAxes = ['Demand', 'Comp', 'Mobility', 'Stability', 'Growth', 'Scarcity'];
export const alignYou    = [0.62, 0.55, 0.92, 0.78, 0.71, 0.84];
export const alignMarket = [0.86, 0.80, 0.70, 0.62, 0.88, 0.55];

// ── Profile page ───────────────────────────────────────────────
export const profileAccountFields = (cv) => [
  { label: 'Full name',     value: cv.name },
  { label: 'Email',         value: 'aria.chen@lumina.health' },
  { label: 'Current title', value: cv.role },
  { label: 'Company',       value: cv.company },
  { label: 'Location',      value: 'San Francisco, CA' },
  { label: 'Time zone',     value: 'UTC−07:00 · PDT' },
  { label: 'Years exp.',    value: `${cv.years} years` },
  { label: 'LinkedIn',      value: 'linkedin.com/in/ariachen', link: true },
];

export const profileAccountStats = [
  { label: 'PLAN',         value: 'Strata Pro', sub: 'renews 14 Jun' },
  { label: 'ANALYSES RUN', value: '12',          sub: 'since 2024' },
  { label: 'CVS ON FILE',  value: '3',           sub: 'auto-purged in 28d' },
  { label: 'LAST ACTIVE',  value: 'Just now',    sub: 'SF · 192.0.2.14' },
];

export const profileSessions = [
  { device: 'MacBook Pro · Chrome', loc: 'San Francisco · 192.0.2.14', when: 'Active now',  current: true },
  { device: 'iPhone · STRATA app',  loc: 'San Francisco · 192.0.2.40', when: '2 hours ago' },
  { device: 'Firefox · Linux',      loc: 'New York · 198.51.100.7',    when: '3 days ago' },
];

export const profileDataStats = [
  { label: 'CVs STORED',      value: '3' },
  { label: 'ANALYSES',        value: '12' },
  { label: 'VECTORS CACHED',  value: '9' },
];

export const profileToggles = [
  { label: 'Product analytics',               desc: 'Helps us understand which lenses you use most. No personal data leaves your account.',              defaultOn: true  },
  { label: 'Anonymised benchmark contribution', desc: 'Your blurred vector contributes to peer-benchmark distributions. Off by default.',                defaultOn: false },
  { label: 'Job recommendation emails',        desc: 'Weekly digest of roles matching your profile.',                                                    defaultOn: true  },
  { label: 'Research participation',           desc: 'STRATA may invite you to user research for new lenses (max 4/yr).',                               defaultOn: false },
];

export const profileDeletionDate = '14 Jun 2026';
export const profileLastUpdated  = '14 May 2026';
