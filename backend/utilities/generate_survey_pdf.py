"""Generate the STRATA software-survey PDF.

Run from project root:
    python utilities/generate_survey_pdf.py
Output: STRATA_software_survey.pdf
"""

from fpdf import FPDF
from pathlib import Path


# fpdf 1.7 is latin-1 only. Substitute any non-latin-1 chars before write.
_SUBS = {
    "–": "-",   # en dash
    "—": "--",  # em dash
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "•": "-",   # bullet
    "→": "->",
    "←": "<-",
    "…": "...",
    "·": "-",
    "×": "x",
    "≈": "~",
    "±": "+/-",
    "≤": "<=",
    "≥": ">=",
    "●": "*",
    "▲": "^",
    "°": " deg",
}


def san(text: str) -> str:
    for k, v in _SUBS.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "replace").decode("latin-1")


class SurveyPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, san("STRATA - Software Survey"), 0, 0, "L")
        self.cell(0, 8, f"Page {self.page_no()}", 0, 1, "R")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 6, san("Prepared 2026-05-19 - cv_analyser repo"), 0, 0, "C")
        self.set_text_color(0, 0, 0)

    # ---- helpers -------------------------------------------------
    def h1(self, text: str):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 9, san(text))
        self.ln(2)

    def h2(self, text: str):
        if self.get_y() > 250:
            self.add_page()
        self.ln(3)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(20, 50, 90)
        self.multi_cell(0, 7, san(text))
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def h3(self, text: str):
        if self.get_y() > 255:
            self.add_page()
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, san(text))
        self.set_text_color(0, 0, 0)
        self.ln(0.5)

    def body(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.2, san(text))
        self.ln(1.5)

    def bullets(self, items: list[str], indent: float = 4):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        for it in items:
            self.set_x(self.l_margin + indent)
            # render bullet glyph + text via multi_cell so wrapping works
            avail = self.w - self.r_margin - self.l_margin - indent
            self.multi_cell(avail, 5.2, san("- " + it))
        self.ln(1.5)

    def numbered(self, items: list[str]):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        for i, it in enumerate(items, 1):
            avail = self.w - self.r_margin - self.l_margin - 4
            self.set_x(self.l_margin + 4)
            self.multi_cell(avail, 5.2, san(f"{i:02d}. {it}"))
        self.ln(1.5)

    def kv_table(self, rows: list[tuple[str, str]], col1: float = 55):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        for k, v in rows:
            y0 = self.get_y()
            x0 = self.l_margin
            self.set_font("Helvetica", "B", 10)
            self.multi_cell(col1, 5.2, san(k))
            y1 = self.get_y()
            self.set_xy(x0 + col1, y0)
            self.set_font("Helvetica", "", 10)
            self.multi_cell(self.w - self.r_margin - self.l_margin - col1, 5.2, san(v))
            y2 = self.get_y()
            self.set_y(max(y1, y2))
        self.ln(1.5)

    def hrule(self):
        self.ln(1)
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)


# ─────────────────────────────────────────────────────────────────
# Content
# ─────────────────────────────────────────────────────────────────
def build():
    pdf = SurveyPDF(format="A4")
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover ──────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(0, 130, 180)
    pdf.cell(0, 6, san("STRATA / CAREER INTELLIGENCE PLATFORM"), 0, 1, "L")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 26)
    pdf.multi_cell(0, 11, san("Software Survey"))
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(
        0, 6,
        san("A pre-build assessment of the dashboard's utilities, component requirements, "
            "constraints, and the risks we should plan around before committing to engineering work."),
    )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)
    pdf.kv_table([
        ("Project",        "cv_analyser (STRATA frontend + Flask backend)"),
        ("Repository",     "d:/Projects/Portfolio/cv_analyser"),
        ("Survey author",  "sagar (sagarvincnt@gmail.com)"),
        ("Date",           "2026-05-19"),
        ("Current state",  "React hi-fi prototype + Flask scaffold with stub scoring"),
        ("Survey scope",   "Functions to ship, requirements, constraints, risks"),
    ], col1=40)
    pdf.hrule()

    # ── 1. Dashboard functions / utilities ─────────────────────────
    pdf.h1("1. Dashboard functions & utilities")
    pdf.body(
        "Before discussing requirements, this section enumerates every function the STRATA "
        "dashboard intends to offer the end user. The list is derived from the design handoff "
        "(design_handoff_strata/README.md), the built React modules under frontend/src/components, "
        "and the central mock store at frontend/src/data/mockData.js. Each item is a discrete "
        "capability that the production system must back with real logic and data."
    )

    pdf.h3("1.1 Intake & ingestion")
    pdf.bullets([
        "Upload a CV file (PDF / DOC / DOCX / TXT) via drag-and-drop or file picker.",
        "Optional paste of a target Job Description (JD) as free text.",
        "Validate file type, file name, and a 16 MB upload cap.",
        "'Load sample profile (Aria Chen)' button to populate a canned demo profile + JD.",
        "Render a 12-stage live 'reasoning trace' animation (INGEST -> EMBED -> MATCH -> "
        "MARKET -> FIT -> GAP -> PATHS -> SYNTHESIS) while the real pipeline runs in the background.",
    ])

    pdf.h3("1.2 Overview lens (executive brief)")
    pdf.bullets([
        "Executive headline + one-paragraph synthesis of all eight analytical lenses.",
        "Six clickable metric cards (JD Fit, ATS Score, Peer Percentile, Comp Position, "
        "Market Align, Momentum) - each navigates to its own lens.",
        "'The three moves' - the three highest-leverage, ranked recommendations with expected delta tags.",
        "Live market mini-card (open roles, applicants/role + 7-point sparklines).",
        "Vector fingerprint card showing 20-of-1536-d embedding preview + cohort tag.",
    ])

    pdf.h3("1.3 JD Fit lens")
    pdf.bullets([
        "Overall JD<->CV alignment score (gauge ring, 0-100).",
        "Counts of evidenced matches vs. JD requirements and gaps flagged (high / med / low).",
        "Keyword density vs. JD threshold.",
        "Evidence stream: top semantic matches with the exact CV phrase that grounds each match.",
        "Gap stream: ranked missing requirements with HIGH/MED/LOW impact pills + remediation notes.",
    ])

    pdf.h3("1.4 ATS Readability lens")
    pdf.bullets([
        "ATS score (0-100) with a large ring visual.",
        "Eight structural checks: parseable structure, standard section headers, no images / "
        "multi-column layout, job-title taxonomy match (ESCO), keyword density, action-verb "
        "leads, quantified outcomes, skill-section taxonomy match.",
        "Per-check PASS / FIX verdict with explanatory notes.",
        "Recruiter dwell-time estimate vs. ATS-corpus norm.",
    ])

    pdf.h3("1.5 Skill Matrix lens")
    pdf.bullets([
        "8 x 5 heatmap of skill strength vs. four reference tracks (YOU / PEER P50 / "
        "PEER P90 / JD ASK / DIRECTOR TIER).",
        "Delta cards: biggest over-index, biggest under-index, most-undervalued skill.",
        "Switchable cell rendering (blocks vs. dots) via the chart-style power-user tweak.",
    ])

    pdf.h3("1.6 Peer Benchmark lens")
    pdf.bullets([
        "16-bucket histogram of overall peer-percentile distribution; user bucket and P50 "
        "bucket highlighted.",
        "Sub-dimension strip: tenure, mobility, impact, breadth - YOU vs. P50 with deltas.",
        "Cohort size disclosed (n = ~12,400).",
    ])

    pdf.h3("1.7 Compensation lens")
    pdf.bullets([
        "Comp-band visual: min / p25 / p50 / p75 / max range with the user's current pay marked.",
        "Reference cards: market median, target band for next role, equity weight vs. cohort.",
        "Cohort definition (role, geo, industry, vintage of source offers).",
    ])

    pdf.h3("1.8 Alternative Paths lens")
    pdf.bullets([
        "Career topology graph (SVG): centre node = current role; ring 1 = one-hop adjacent "
        "roles (n=5); ring 2 = two-hop reachable roles (n=5).",
        "Each node: title, fit score, salary, parent edge.",
        "Edge thickness and node colour encoded by fit.",
        "Two render modes (dots / blocks) with per-lens default.",
    ])

    pdf.h3("1.9 Market Trends lens")
    pdf.bullets([
        "'Rising' and 'Falling' lists of role families / skills with 6-month rolling demand "
        "deltas and 7-point sparklines.",
        "Editorial insight under each list (synthesis copy).",
    ])

    pdf.h3("1.10 Market Alignment lens")
    pdf.bullets([
        "Six-axis radar (Demand / Comp / Mobility / Stability / Growth / Scarcity) overlaying "
        "the user's profile shape against market direction.",
        "Per-axis delta cards with signed +N / -N values, colour-coded by direction.",
    ])

    pdf.h3("1.11 Profile, security & data settings")
    pdf.bullets([
        "Account tab: read-only-then-editable identity fields, last-updated stamp, save.",
        "Security tab: change-password flow with strength meter and validation rules "
        "(>=10 chars, confirm match), 2FA management, recovery-code regeneration, active "
        "session list with revoke.",
        "Data & Privacy tab: data-on-file counters, export-as-JSON, export-analyses-as-PDF, "
        "purge-all, analytics/research toggles.",
        "Danger Zone tab: deactivate (reversible 30 d) and permanent delete with "
        "type-DELETE confirmation + scheduled-deletion view and undo.",
    ])

    pdf.h3("1.12 Chrome utilities (cross-cutting)")
    pdf.bullets([
        "Top-bar Export-PDF (server-rendered active lens + Overview brief).",
        "Top-bar Share-Brief (shareable link to a read-only snapshot).",
        "Sidebar 'NEW ANALYSIS' button (restart flow).",
        "Theme switch (dark default / light) and density (compact / regular / comfy).",
        "Tweaks panel exists as design-time tooling only; strip from production.",
    ])

    # ── 2. What should be built ────────────────────────────────────
    pdf.add_page()
    pdf.h1("2. What should be built")
    pdf.body(
        "The frontend prototype is essentially complete and matches the design spec one-to-one. "
        "The production system on the backend, however, is a thin stub: scoring_fun.score.score_cv "
        "returns a hard-coded 0 and the literal string 'Sample explanation', and "
        "similarity_score.sim_score is a lemma-overlap ratio over spaCy tokens with stopword "
        "removal. None of the eight lenses surfaced on the dashboard are computed by real logic; "
        "all numbers visible in the UI come from frontend/src/data/mockData.js. The build, therefore, "
        "is the entire analytical and data backend behind the dashboard."
    )
    pdf.h3("2.1 Build targets (in priority order)")
    pdf.numbered([
        "CV ingestion service: robust PDF / DOCX / DOC / TXT parser that yields a structured "
        "resume object (employers, dates, titles, bullets, skills, education, contact).",
        "JD ingestion service: light NLP over pasted text to extract seniority, domain, scope, "
        "required skills, and keyword set.",
        "Embedding service: produce a fixed-dimension career-space vector per CV and per JD "
        "(the prototype labels it strata-emb-3 / 1536-d; pick a real model).",
        "Eight lens analyzers, each returning the exact data shape the React module already consumes "
        "(see Section 3 for the contract per lens).",
        "Peer + market + comp reference datasets and the retrieval layer to query them.",
        "Analysis orchestrator: fan-out across the lenses, stream stage events to the frontend's "
        "12-stage trace, return one consolidated brief.",
        "Persistence: users, CVs (with retention rules), analyses, embeddings cache.",
        "Auth + billing: account/security/data tabs already assume Pro plan, 2FA, sessions, "
        "and delete-account flows.",
        "PDF brief export (server-rendered Overview + active lens).",
        "Observability: trace IDs (already shown in the UI - e.g. 0x4A7F2), latency / quality "
        "metrics, model-version logging.",
    ])
    pdf.h3("2.2 Explicit non-goals")
    pdf.bullets([
        "Multi-tenant team workspaces - not in the design.",
        "Inline CV editing inside STRATA - the product critiques but does not author.",
        "Mobile-native apps - the design is desktop-class dark UI.",
        "Replacing the Tweaks panel with a production settings screen - it's a dev tool only.",
    ])

    # ── 3. Requirements per component / service ─────────────────────
    pdf.h1("3. Requirements by component / service")
    pdf.body(
        "Requirements are organised by the service boundaries that should fall out of the "
        "build-targets above. Where the prototype already declares an interface (typed data "
        "shape, mock structure, UI affordance), the production component must honour it."
    )

    pdf.h3("3.1 CV Ingestion Service")
    pdf.bullets([
        "Accept PDF, DOCX, DOC, TXT up to 16 MB; reject anything else with a clear error.",
        "Extract: contact block, summary, employers[], titles[], date-ranges[], bullets[], "
        "skills[], education[], certifications[], links[].",
        "Normalise titles to a canonical taxonomy (ESCO is named in the ATS spec).",
        "Defensive parsing of multi-column / scanned PDFs (fall back to OCR or flag).",
        "Strip secrets / PII for analytics; keep originals only for the user's retention window.",
        "Idempotent: same file content -> same parsed object (hash-keyed).",
    ])

    pdf.h3("3.2 JD Ingestion Service")
    pdf.bullets([
        "Tokenise + classify: extract seniority, domain, scope, function, must-haves, nice-to-haves.",
        "Produce a normalised skill set keyed to the same taxonomy as the CV service.",
        "Handle pasted text from any ATS (LinkedIn / Greenhouse / Lever / freeform).",
    ])

    pdf.h3("3.3 Embedding Service")
    pdf.bullets([
        "Single source of truth for vector dimension; the UI displays a 1536-d preview.",
        "Stable model version exposed in responses (the prototype tags 'strata-v3').",
        "Cache by content hash; recompute only on model version bump.",
        "Latency budget: the 12-stage trace targets a 14 s median total analysis (per "
        "the upload screen's capability strip).",
    ])

    pdf.h3("3.4 Lens analyzers")
    pdf.body(
        "Each lens is a function from (parsed_cv, parsed_jd, reference_data) to the exact "
        "structure rendered by its React module. Contracts:"
    )
    pdf.kv_table([
        ("JD Fit",
         "score 0-100; evidencedMatches; totalRequirements; gapsFlagged (h/m/l breakdown); "
         "keywordDensity; matches[] of (topic, evidence quote, strength 0-1); gaps[] of "
         "(topic, impact, note)."),
        ("ATS",
         "score 0-100; dwellTime / normDwellTime; checks[] of (label, pass: bool, note). "
         "Must include all 8 checks in mockData.js verbatim."),
        ("Skill Matrix",
         "rows[] (skills), cols[] (tracks), data[rows][cols] in 0..1, deltaCards[] for "
         "over-index / under-index / undervalued."),
        ("Peer Benchmark",
         "buckets[16] of histogram counts, youBucket index, p50Bucket index, dimensions[] "
         "(dim, you, p50). Must publish cohort size + definition."),
        ("Compensation",
         "min / p25 / p50 / p75 / max / you (all integers, USD); refCards[] for median, "
         "target band, equity weight. Cohort definition + sample size mandatory."),
        ("Alt Paths",
         "center node + nodes[] (id, title, fit 0-1, salary string, ring 1|2) + links[] "
         "(from, to, fit). 10 nodes total in the mock; production may vary."),
        ("Trends",
         "rising[] and falling[] of (topic, delta string %, spark[7], note)."),
        ("Align",
         "axes[6], you[6], market[6] - all values 0..1."),
        ("Overview",
         "Synthesises the above into 6 metric cards + 3 ranked moves + market mini + "
         "vector fingerprint. Must not duplicate compute - it reads from lens outputs."),
    ], col1=34)

    pdf.h3("3.5 Reference data layer")
    pdf.bullets([
        "Peer profile corpus with cohort filters (role, seniority, geo, vintage).",
        "Live posting feed (the upload screen advertises 180K live postings, 320 markets).",
        "Verified-offer comp dataset (compSummary advertises n=1,840 over 90 d).",
        "Skill / title / industry taxonomy with synonyms.",
        "Refresh cadence and provenance per source - exposed in UI footnotes.",
    ])

    pdf.h3("3.6 Orchestrator + streaming trace")
    pdf.bullets([
        "Server-Sent Events (or WebSocket) channel that streams the 12 trace messages by stage tag.",
        "If real compute returns early, hold on the final stage briefly; if late, the scan-line "
        "must keep moving (per design spec section 5.2).",
        "Trace ID format already shown: 0xNNNNN (5 hex chars).",
    ])

    pdf.h3("3.7 Persistence")
    pdf.bullets([
        "Users, plans (Strata Pro mentioned), 2FA secrets, recovery codes, active sessions.",
        "CVs with explicit retention (the Data & Privacy tab advertises 'auto-purged in 28d', "
        "'30d / 12mo / 7d anonymisation').",
        "Analyses (the profile shows ANALYSES RUN counter).",
        "Embeddings cache (the profile shows VECTORS CACHED counter).",
    ])

    pdf.h3("3.8 Auth, billing, account management")
    pdf.bullets([
        "OAuth (Google / Apple) + email magic link as a baseline.",
        "Stripe (or equivalent) for the Pro plan + renewal date displayed in profile stats.",
        "TOTP-based 2FA, recovery codes, device-session list with revoke.",
        "Permanent-delete pipeline: type-DELETE confirm, 30 d scheduled purge, undo before "
        "the scheduled date - all already designed in the Danger Zone tab."
    ])

    pdf.h3("3.9 PDF / Share export")
    pdf.bullets([
        "Server-side render of the Overview brief plus the currently active lens.",
        "Headless-browser or React-PDF; must reproduce the OKLCH palette and serif headlines.",
        "Share-Brief: signed, read-only public URL with optional expiry.",
    ])

    pdf.h3("3.10 Frontend (already in place, gaps to close)")
    pdf.bullets([
        "Replace MODULES' mock imports with real fetches against the new API.",
        "Add a router (the current App.jsx uses local state; spec recommends URL routes "
        "/upload, /analysing, /dashboard/[lensId], /profile/[tab]).",
        "Add a11y wiring (focus rings, aria labels on SVG, keyboard traversal of the lens list).",
        "Strip the TweaksPanel for production builds.",
    ])

    # ── 4. Constraints ─────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("4. Constraints")

    pdf.h3("4.1 Technical constraints (already locked)")
    pdf.bullets([
        "Frontend stack: React 18 + Vite (see frontend/package.json). The design's "
        "Next.js recommendation is not what we built.",
        "Backend stack: Flask 3 + spaCy en_core_web_sm; PyPDF2 / pdfplumber / "
        "python-docx / docx2txt for parsing (requirements.txt).",
        "Single-server deployment topology today (Dockerfile + docker-compose.yaml + an "
        "ECS task definition under .github/workflows/).",
        "16 MB hard upload cap, file extensions limited to PDF/DOC/DOCX/TXT (interface.py).",
        "spaCy small English model only - no domain vocabulary, no multi-lingual support.",
        "Frontend is bundled and served from frontend/dist by Flask - no separate CDN today.",
    ])

    pdf.h3("4.2 Design constraints")
    pdf.bullets([
        "High-fidelity visual reproduction is required: exact OKLCH tokens, Instrument Serif "
        "/ Space Grotesk / JetBrains Mono fonts, density variants, animation easings.",
        "Editorial voice is part of the brand - terse, confident, numeric. The model output "
        "MUST be post-processed into this register, not surfaced raw.",
        "Glow is reserved for accent / good tones only. Never glow warn / bad / muted.",
        "One chart per card (except Skill Matrix).",
    ])

    pdf.h3("4.3 Product constraints")
    pdf.bullets([
        "Single-user product - no team / org tier in scope.",
        "Desktop-first dark UI; mobile is out of scope until later.",
        "PDF / DOCX / DOC / TXT input only; no LinkedIn-import scraping path defined.",
        "English-only copy and analysis in v1 (the lemma overlap and the spaCy model assume English).",
    ])

    pdf.h3("4.4 Compliance / legal constraints")
    pdf.bullets([
        "CV uploads contain PII. Retention windows are already promised in the UI "
        "('auto-purged in 28d', 30d / 12mo / 7d anonymisation) - those promises become "
        "contractual once shipped.",
        "Peer + comp data sources determine the compliance posture: scraped data has "
        "different exposure than opt-in or partner data.",
        "Permanent-delete must actually delete (incl. derived vectors and analyses) within "
        "the advertised 30 d window.",
        "If analytics opt-out is OFF by default for benchmark contribution (as designed), "
        "the opposite default would breach the displayed copy.",
    ])

    pdf.h3("4.5 Operational constraints")
    pdf.bullets([
        "14 s median analysis target advertised on the upload screen - this becomes the "
        "end-to-end p50 latency budget for the full lens fan-out.",
        "The 12-stage trace must keep moving even if real compute stalls; UI cannot freeze.",
        "Versioning: the chrome already shows 'STRATA v4.2.1' and a trace ID - build/version "
        "headers must be wired through from CI."
    ])

    # ── 5. Risks & potential problems ──────────────────────────────
    pdf.h1("5. Risks & potential problems")

    pdf.h3("5.1 Backend correctness & accuracy")
    pdf.bullets([
        "Current scorer is a stub (scoring_fun.py returns 0 + 'Sample explanation') and "
        "the lemma-overlap fallback in similarity_score.py is a poor proxy for semantic "
        "fit. Shipping the existing UI on top of these will mislead users.",
        "Lemma overlap ignores synonyms, multi-word skills, and weighting - 'Python' and "
        "'python developer' are not equivalent under the current code.",
        "Numbers displayed in the UI today (84p, 91/100, $214k, etc.) are mock and must be "
        "computed; there is no plan-of-record for any of them in the repo.",
        "Risk that the 'evidence quote' in JD Fit can be hallucinated unless we ground each "
        "match to a verbatim CV span.",
    ])

    pdf.h3("5.2 Data sourcing & licensing")
    pdf.bullets([
        "No peer / market / compensation dataset exists in the repo. Acquiring one is the "
        "single largest unscoped expense (Levels.fyi / Pave / Compete / partner ATS feeds).",
        "Scraping LinkedIn or job boards risks ToS / legal exposure.",
        "Opt-in benchmark contribution (designed for the Data & Privacy toggles) seeds the "
        "peer pool, but starts empty - cold-start problem.",
    ])

    pdf.h3("5.3 PII, security & privacy")
    pdf.bullets([
        "CVs leak names, emails, phone, addresses, employers. Encryption at rest + in "
        "transit is mandatory.",
        "The current Flask app uses a default dev secret if SECRET_KEY isn't set "
        "(interface.py:21) - dangerous if shipped that way.",
        "Permanent-delete must cascade to embeddings + cached derivations or the promise "
        "is broken.",
        "No rate limiting visible today - upload endpoint is open to abuse.",
        "The 'secure_filename' helper does not prevent malicious content inside accepted "
        "extensions (PDF parser RCE / docx zip-slip).",
    ])

    pdf.h3("5.4 Parsing fragility")
    pdf.bullets([
        "PDF parsing of scanned / image-only CVs returns empty text - no OCR path today.",
        "Multi-column layouts produce interleaved text from PyPDF2.",
        "DOCX with embedded images / tables can break docx2txt extraction.",
        "parse_cv_file's first branch in parsing_fun.py checks isinstance(file_path, PdfWriter) "
        "but the type hint says str - dead code path, but a smell that the API isn't settled.",
    ])

    pdf.h3("5.5 Latency & cost")
    pdf.bullets([
        "14 s p50 target with embedding + peer retrieval + 8 lens analyzers is tight. "
        "Concurrent fan-out + caching is required, not optional.",
        "If embeddings come from a paid API, per-analysis cost compounds with daily "
        "users; vector cache is a must.",
        "Each lens has its own DB query / data source; without an orchestration layer, "
        "tail latency dominates.",
    ])

    pdf.h3("5.6 UI / UX risks")
    pdf.bullets([
        "Dashboard renders 9 charts in real time on a single page - heavy DOM + SVG. Lens "
        "components re-mount on switch (by design), so fade-ins re-trigger - watch for "
        "layout thrash on slower hardware.",
        "Glow shadows and OKLCH gradients perform differently across Safari / Firefox / "
        "Chromium; visual QA on all three is needed.",
        "No accessibility wiring today - focus rings and aria roles are explicitly out-of-spec "
        "and must be added before launch.",
        "Editorial copy is generated by the model; without human review or a strict tone "
        "prompt, output drifts off-brand.",
    ])

    pdf.h3("5.7 Auth / billing complexity")
    pdf.bullets([
        "Profile page assumes a finished auth system: 2FA, recovery codes, sessions, "
        "subscription plans, deletion queues. None of these exist in the backend today.",
        "Stripe integration + plan-state syncing introduces a separate consistency problem "
        "(webhooks, retries, dunning).",
    ])

    pdf.h3("5.8 Product / scope risks")
    pdf.bullets([
        "The product makes nine independent analytical claims per analysis. Each weak claim "
        "erodes trust in the others; quality bar must be uniform.",
        "Output is advisory but the tone is decisive ('You're underpaid by $28k.'). "
        "Mis-calibrated numbers create reputational risk.",
        "Scope creep is highly likely - 'Director path' calculations alone could expand "
        "into a multi-month research project. Sequencing matters."
    ])

    pdf.h3("5.9 Repo hygiene & deployment")
    pdf.bullets([
        "Hardcoded local Windows paths still appear in parsing_fun.py and similarity_score.py "
        "__main__ blocks - harmless but noisy.",
        "Compiled .pyc files in backend/__pycache__ are tracked / modified - .gitignore "
        "exists but the cache files were already committed previously.",
        "compose.yaml was deleted in working tree; docker-compose.yaml is new (untracked). "
        "Pick one and commit it before CI / ECS workflow drift sets in.",
        "ECS deployment workflow (.github/workflows/ecs-deployment.yaml) implies cloud "
        "infra that the dev environment doesn't reflect.",
    ])

    # ── 6. Recommended build sequence ──────────────────────────────
    pdf.h1("6. Recommended build sequence")
    pdf.numbered([
        "Backend foundation: replace the stub scorer with a deterministic JD Fit + ATS pipeline. "
        "These two lenses don't require external data and unblock honest dashboard demos.",
        "Embedding + caching layer: pick a model, version it, cache by content hash.",
        "Peer / comp / market data acquisition decision (build, partner, or punt). Block "
        "Skill Matrix, Peer, Comp, Trends, Align lenses on this call.",
        "Orchestrator + streaming trace: make the 12-stage trace driven by real backend events.",
        "Auth + persistence + plan management.",
        "Profile / data / danger zone flows (mostly UI already exists; backend behind them is new).",
        "PDF export + Share-Brief.",
        "Accessibility + cross-browser pass + observability + cost dashboards.",
    ])

    # ── 7. Open questions ──────────────────────────────────────────
    pdf.h1("7. Open questions to resolve before kickoff")
    pdf.numbered([
        "CV parsing: roll our own pipeline or adopt Affinda / Docparser / RChilli?",
        "Embedding model: OpenAI text-embedding-3-large (1536-d, matches UI), Cohere "
        "embed-v3, or a custom fine-tune?",
        "Peer dataset provenance: opt-in only, partner ATS, scraped, or hybrid?",
        "Compensation data: Levels.fyi-style scrape vs. partner data (Pave, Compete)?",
        "Auth providers: Google + Apple + magic link sufficient, or do we need SSO?",
        "Billing: Stripe Customer Portal vs. custom plan-management UI?",
        "Production deployment target: stay on AWS ECS (per the existing workflow) or move "
        "to a managed PaaS?",
        "Frontend hosting: continue serving frontend/dist from Flask, or split to a CDN + API?",
    ])

    out = Path(__file__).resolve().parent.parent / "STRATA_software_survey.pdf"
    pdf.output(str(out))
    print(f"Wrote {out}")


if __name__ == "__main__":
    build()
