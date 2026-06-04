# cv_analyser

STRATA — a career intelligence platform that ingests a CV (and optionally a target job description) and runs eight analytical "lenses" over it: JD Fit, ATS Readability, Skill Matrix, Peer Benchmark, Compensation, Alternative Paths, Market Trends, and Market Alignment.

The frontend (React 18 + Vite, in [frontend/](frontend/)) is a hi-fi prototype matching the design handoff in [design/design_handoff_strata/](design/design_handoff_strata/). The platform is now backed by two FastAPI services: an API gateway ([API/](API/)) handling auth and user profiles, and a dedicated analyser service ([backend/](backend/)) that parses CVs. Dashboard lens numbers still come from [frontend/src/data/mockData.js](frontend/src/data/mockData.js) until the lens analyzers are wired up.

The full pre-build survey (utilities the dashboard offers, requirements per service, constraints, risks) is in **[STRATA_software_survey.pdf](STRATA_software_survey.pdf)** (re-generate via [utilities/generate_survey_pdf.py](utilities/generate_survey_pdf.py)).

---

## Current build status

| Layer | Status |
|---|---|
| Frontend (upload → analysing → dashboard → profile) | Built |
| Auth — `POST /api/auth/verify` (bcrypt, asyncpg) | Built |
| User profile CRUD | Built |
| CV parser (PDF / DOCX / TXT → sections + ATS red-flags) | Built |
| Database schema (users, profiles, cv_uploads, …) | Built |
| Production HTTPS (nginx-proxy + Let's Encrypt) | Built |
| Lens analyzers (JD Fit, ATS, SkillMatrix, Peer, Comp, Paths, Trends, Align) | Stubbed / mock data |
| Embedding service + vector cache | Not started |
| Orchestrator + SSE trace | Not started |
| Export (PDF brief, share link) | Not started |
| Observability | Not started |

---

## Architecture

The system as it would look once the survey's build-targets are in place. The frontend and core services are built; the ML pipeline layers are next.

### System diagram

```
                     ┌────────────────────────────────────────────────────┐
                     │                     BROWSER (user)                 │
                     │   React 18 + Vite  •  served from /frontend/dist   │
                     │   stages: upload → analysing (SSE) → dashboard     │
                     └─────────┬────────────────────────────┬─────────────┘
                          HTTPS│  REST/JSON              SSE│ trace events
                               ▼                            ▼
       ┌──────────────────────────────────────────────────────────────────┐
       │                  API GATEWAY (FastAPI, :8001)                    │
       │   auth middleware • rate-limit • upload cap 16MB • CORS • CSRF   │
       └──┬─────────┬──────────┬───────────┬──────────┬─────────┬─────────┘
          │         │          │           │          │         │
          ▼         ▼          ▼           ▼          ▼         ▼
     ┌────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐ ┌──────┐ ┌───────────┐
     │ AUTH & │ │ INGEST │ │ANALYSIS │ │ PROFILE  │ │EXPORT│ │OBSERVABIL.│
     │BILLING │ │SERVICE │ │ ORCHES- │ │ SERVICE  │ │ SVC  │ │  traces / │
     │  svc   │ │CV + JD │ │ TRATOR  │ │ acct/2FA │ │PDF / │ │  metrics  │
     │ OAuth, │ │parsers │ │  + SSE  │ │sessions, │ │share │ │  / logs   │
     │ Stripe │ │ + norm.│ │ stream  │ │ delete   │ │ link │ │           │
     └───┬────┘ └───┬────┘ └────┬────┘ └────┬─────┘ └──┬───┘ └─────┬─────┘
         │          │           │           │          │           │
         │          ▼           ▼           │          │           │
         │   ┌──────────────────────────┐   │          │           │
         │   │   EMBEDDING SERVICE      │   │          │           │
         │   │  model:strata-emb-v1     │   │          │           │
         │   │  (OpenAI / Cohere / …)   │   │          │           │
         │   │  hash-keyed vector cache │   │          │           │
         │   └──────────┬───────────────┘   │          │           │
         │              │                   │          │           │
         │              ▼                   │          │           │
         │   ┌────────────────────────────────────────┐│          │
         │   │             LENS ANALYZERS              ││          │
         │   │  JDFit · ATS · SkillMatrix · Peer ·     ││          │
         │   │  Comp  · Paths · Trends · Align         ││          │
         │   │      ↑ fan-out, parallel, idempotent ↑  ││          │
         │   └─┬───────────┬──────────┬───────────┬───┘│          │
         │     │           │          │           │    │          │
         │     ▼           ▼          ▼           ▼    │          │
         │  ┌──────────────────────────────────────┐   │          │
         │  │       REFERENCE DATA LAYER           │   │          │
         │  │  peer corpus  · taxonomy (ESCO)      │   │          │
         │  │  live postings · comp dataset        │   │          │
         │  │  refresh ETL jobs (nightly / hourly) │   │          │
         │  └──────────────────────────────────────┘   │          │
         │                                             │          │
         ▼              ▼                              ▼          ▼
     ┌──────────────────────────────────────────────────────────────────┐
     │                          PERSISTENCE                              │
     │  Postgres: users · plans · 2FA · sessions · analyses · deletion-q │
     │  Object store (S3): raw CVs (retention-tagged)                    │
     │  Vector store (pgvector / Pinecone): embeddings cache             │
     │  Redis: trace pub/sub · rate-limit · session cache                │
     └──────────────────────────────────────────────────────────────────┘
```

### Component responsibilities

| Component | Owns | Reads from | Writes to | Notes |
|---|---|---|---|---|
| **Frontend** | Stages, lens routing, profile UI, SSE consumer | API gateway | — | Built; needs router + a11y, drop TweaksPanel for prod. |
| **API gateway** | Auth check, rate limit, request routing, file-size cap | All services | Audit log | FastAPI; gunicorn + nginx in prod. |
| **Auth & billing** | Credentials, bcrypt hashing, sessions, Stripe webhooks, plan state | Postgres | Postgres | OAuth / TOTP / Stripe still to add. |
| **Ingest service** | CV parser (PDF/DOC/DOCX/TXT → structured), JD NLP, taxonomy normalisation | Object store | Postgres, vector cache key | CV parser is built; JD parsing and taxonomy normalisation still to add. |
| **Embedding service** | One vector per CV, one per JD, versioned, cached | Ingest output | Vector store | Drives the "1536-d preview" the UI shows. |
| **Orchestrator** | Fan-out across 8 lens analyzers, stream 12 trace stages, assemble overview brief | Embeddings + ref data + analyzers | Postgres (`analyses`) | Owns the 14 s p50 budget. Trace via SSE, backed by Redis pub/sub. |
| **Lens analyzers** | One pure function per lens, returns the exact shape `mockData.js` declares | parsed_cv, parsed_jd, embeddings, ref data | — | Stateless. Can run in-process or split out per scale need. |
| **Reference data layer** | Peer corpus, comp dataset, posting feed, taxonomy | External partners / opt-in feed / scrape (decide) | — | Refresh ETL is its own pipeline. |
| **Profile service** | Account fields, security, data toggles, deletion scheduler | Postgres | Postgres | Soft-delete (30 d) then cascade purge to vectors + analyses. |
| **Export service** | Server-side PDF (Overview + active lens), share-brief signed URLs | Analyses, brand assets (fonts/OKLCH) | Object store | Headless Chromium or React-PDF. |
| **Observability** | Trace IDs (`0xNNNNN`), per-lens latency, model version, cost | All services emit | OTLP / log sink | Trace ID surfaces back into the UI. |

### Key request flows

#### Auth (POST)

```
Browser ──POST /api/auth/verify {username, password}──► API Gateway
   Gateway ─► auth.service.verify_user(pool, username, password)
       asyncpg: SELECT user WHERE email = username
       bcrypt: compare SHA-256(password) against stored hash
   ◄── 200 ProfileResponse  |  401 Invalid username or password.
```

#### CV parse (POST)

```
Browser ──POST /api/user-profile/upload-cv (multipart)──► API Gateway
   Gateway: validate file (16 MB cap, pdf/docx/txt only)
   Gateway ─► analyser_client.parse_cv(file_bytes, filename)
       Analyser (:8002): dispatch_by_extension → extract text
                         clean_text → CleanedText
                         segment → Sections (experience, education, skills, …)
                         build_ats_redflags → AtsRedFlags (10 signals)
   ◄── ParsedCV {raw_text, sections, extraction_method, ats_redflags}
   Gateway: stores cv_uploads record in Postgres
```

#### Analyze (POST → SSE) — planned

```
Browser ──POST /analyse (cv file, optional jd text)──► Gateway
   Gateway: authn, validate, persist raw CV (S3, retention-tagged)
   Gateway ─► Orchestrator (analysis_id, trace_id=0xNNNNN)
       Orchestrator opens SSE channel; emits stages as work progresses:
         1. INGEST    ◄── Ingest service (parse CV) ─┐
         2. INGEST    ◄── Ingest service (parse JD) ─┤  parallel
         3. EMBED     ◄── Embedding service ─────────┘
         4. MATCH     ◄── Peer retrieval (vector kNN)
         5. MARKET    ◄── Posting feed query
         6. FIT       ◄── JD-Fit analyzer
         7. FIT       ◄── ATS analyzer
         8. GAP       ◄── SkillMatrix + Comp deltas
         9. PATHS     ◄── Alt-Paths analyzer
        10. SYNTHESIS ◄── Overview composer (consumes lens outputs)
   Orchestrator persists analysis row; closes SSE with final payload.
Browser routes to /dashboard/overview.
```

#### Lens fetch (GET) — planned

```
Browser ──GET /api/analyses/{id}/lens/{lensId}──► Gateway
   Gateway ─► Orchestrator cache (Postgres `analyses.lens_payloads`)
   ◄── JSON in the exact shape mockData expects.
```

### Data model (core tables)

```
-- currently live (database/user_profile/init.sql)
users(id, username, email, password_hash, created_at)
qualifications(id, user_id, type, institution, grade, start_date, end_date, source)
experience(id, user_id, job_title, company, start_date, end_date, description, source)
aspirations(id, user_id, role, industry, location, salary_min, salary_max, source)
projects(id, user_id, name, description, url, start_date, end_date, source)
skills(id, user_id, name, level, years_experience, source)
cv_uploads(id, user_id, filename, file_path, file_size, status, uploaded_at, parsed_at)

-- planned (full roadmap)
plans(id, name, stripe_customer_id, renews_at, …)
sessions(id, user_id, device, ip, last_active, current)
recovery_codes(id, user_id, code_hash, used_at)
deletion_requests(id, user_id, scheduled_at, status)
cvs(id, user_id, sha256, storage_url, retention_until, parsed_at)
embeddings(cv_id|jd_id, model_version, vector)   -- pgvector
analyses(id, user_id, cv_id, jd_text, trace_id, model_version, started_at, finished_at, lens_payloads jsonb)
reference.peers / reference.postings / reference.comp / reference.taxonomy
```

### Deployment topology

```
                       ┌───────────────────┐
                       │     CloudFront    │
                       │ (frontend assets) │
                       └────────┬──────────┘
                                │
                       ┌────────▼──────────┐
                       │  nginx-proxy      │  TLS termination (Let's Encrypt)
                       │  + acme-companion │  virtual-host routing
                       └────────┬──────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
   ┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
   │  frontend       │ │  api (:8001)    │ │  analyser       │
   │  (nginx, built  │ │  FastAPI        │ │  (:8002)        │
   │   React dist)   │ │  auth + profile │ │  FastAPI        │
   └─────────────────┘ └────────┬────────┘ │  cv_parser      │
                                │          └─────────────────┘
                       ┌────────▼──────────┐
                       │  db (Postgres 16) │
                       └───────────────────┘
```

---

## Repository layout

```
API/
  auth/
    interface.py        POST /api/auth/verify
    service.py          verify_user — bcrypt credential check
    models.py           VerifyRequest
  user_profile/
    interface.py        profile CRUD endpoints
    service.py          asyncpg queries + CV upload, delegates parse to analyser
  clients/
    analyser_client.py  async HTTP wrapper → POST http://analyser:8002/cv/parse
  main.py               FastAPI app, mounts auth + user_profile routers
  requirements.txt
  Dockerfile / Dockerfile.dev

backend/
  cv_parser/            CV parsing pipeline (4-layer architecture)
    leaves/
      extraction_leaves.py   signal computation (stream order, density, encoding)
      cleaning_leaves.py     whitespace normalization helpers
      segmentation_leaves.py section detection, heading recognition
    extractors.py        dispatch_by_extension → PDF / DOCX / TXT extraction
    cleaner.py           text cleaning → CleanedText
    segmenter.py         section splitting (Experience, Education, Skills, …)
    redflags.py          10 ATS red-flag signals
    parser.py            parse_cv(file_bytes, filename) → ParsedCV  (L2 entry)
    interface.py         POST /cv/parse  (FastAPI router, L1)
    models.py            ParsedCV, Sections, AtsRedFlags, …
  upload_validation/
    file_validator.py    file type + 16 MB size guard
  tests/
    test_cv_parser_extractors.py
    test_cv_parser_leaves.py
    test_cv_parser_parse_cv.py
    test_file_validator.py
  main.py               FastAPI app, mounts cv_parser router
  pytest.ini
  requirements.txt
  Dockerfile / Dockerfile.dev

frontend/               React 18 + Vite app (hi-fi prototype)
  src/
    components/flow/    Upload, Analysing, Dashboard, AuthScreen
    context/AuthContext.jsx
    data/mockData.js    All lens outputs (used until analyzers are live)
  vite.config.js
  nginx.conf            Production static-file serving

database/
  user_profile/
    init.sql            PostgreSQL schema (users, qualifications, experience, …)

certs/                  Local HTTPS material (gitignored)
  README.md             openssl / mkcert / ACM generation recipes

design/
  design_handoff_strata/  Canonical design reference (HTML / JSX / CSS)

test/
  integration/data/     CV/JD fixtures
  real_data/            Real CV fixtures

docker-compose.yaml     Production stack (nginx-proxy + acme-companion + services)
docker-compose.dev.yaml Dev stack (hot-reload, local HTTPS on :5200/:8010/:8011)
.env.example            Environment variable template
```

---

## Local development

### Prerequisites

- Docker Desktop (or Docker Engine + Compose v2)
- Node 20+ (for frontend-only work without Docker)
- Python 3.11+ (for backend-only work without Docker)

### Docker (recommended — runs all services together)

**Development** (hot-reload on all services, HTTPS on localhost):

```
# 1. Generate local certs first (see certs/README.md for options, e.g. mkcert)
mkcert -install
mkcert -cert-file certs/fullchain.pem -key-file certs/privkey.pem localhost 127.0.0.1

# 2. Copy and fill env (DB defaults are fine for local dev)
cp .env.example .env

# 3. Start
docker compose -f docker-compose.dev.yaml up --build
```

Services (host ports remapped to avoid local clashes; container ports unchanged):
- Frontend (Vite HMR): https://localhost:5200
- API gateway: http://localhost:8010 — OpenAPI at `/openapi.json`
- Analyser: http://localhost:8011 — OpenAPI at `/openapi.json`
- Postgres: localhost:5440

**Production** (nginx-proxy + Let's Encrypt, requires a public domain):

```
# Set PROD_DOMAIN and ACME_EMAIL in .env, then:
docker compose up --build -d
```

### Running services individually (without Docker)

**API gateway:**

```
cd API
pip install -r requirements.txt
DB_HOST=localhost DB_USER=cv_user DB_PASSWORD=changeme \
  ANALYSER_URL=http://localhost:8011 \
  uvicorn main:app --reload --port 8010
```

**Analyser / CV parser:**

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8011
```

**Frontend:**

```
cd frontend
npm install
npm run dev -- --port 5200   # Vite (dev_local) on :5200
npm run build                # writes frontend/dist (served by production nginx)
```

**Backend tests:**

```
cd backend
pytest
```

---

## CV parser

The CV parser (`backend/cv_parser/`) follows a 4-layer architecture (leaves → L3 → L2 → L1):

```
file_bytes + filename
    │
    ▼  extractors.dispatch_by_extension
    │  → extract_pdf (pdfplumber, digital text or OCR fallback)
    │  → extract_docx (python-docx)
    │  → extract_text (plain UTF-8)
    │
    ▼  cleaner.clean_text
    │  → whitespace normalisation → CleanedText
    │
    ▼  segmenter.segment
    │  → heading detection, section splitting
    │  → Sections { experience[], education[], skills[], other[] }
    │
    ▼  redflags.build_ats_redflags
       → 10 ATS signals:
         stream_order_anomaly, text_density, encoding_anomaly_rate,
         extraction_method (digital_pdf|ocr_pdf|docx|text|failed),
         distinct_bullet_chars, line_length_bimodality,
         hyphenation_break_rate, heading_detection_rate,
         section_coherence, unclassified_ratio
         → AtsRedFlags

ParsedCV { raw_text, sections, extraction_method, ats_redflags }
```

**Endpoint:** `POST /cv/parse` (multipart, `file` field) → `ParsedCV` JSON

**Pending:**
- OCR for image-only PDFs (pytesseract + pdf2image, currently stubbed)
- Two-column PDF reflow
- Database persistence to `parsed_cvs` table
- Extended heading / keyword lexicon

---

## Build order

1. **API gateway + ingest service + JDFit/ATS analyzers** — first vertical slice that produces honest numbers.
2. **Embedding service + vector cache** — unblocks every other lens.
3. **Reference data layer + ETL** — gate for SkillMatrix, Peer, Comp, Trends, Align.
4. **Orchestrator + SSE trace** — turns the animation into something real.
5. **Auth + billing + profile** — unlocks shippable accounts.
6. **Export + share** — last-mile polish.
7. **Observability + a11y + cross-browser** — pre-launch hardening.
