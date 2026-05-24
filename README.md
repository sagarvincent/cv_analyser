# cv_analyser

STRATA — a career intelligence platform that ingests a CV (and optionally a target job description) and runs eight analytical "lenses" over it: JD Fit, ATS Readability, Skill Matrix, Peer Benchmark, Compensation, Alternative Paths, Market Trends, and Market Alignment.

The frontend (React 18 + Vite, in [frontend/](frontend/)) is a hi-fi prototype matching the design handoff in [design_handoff_strata/](design_handoff_strata/). The Flask backend ([interface.py](interface.py), [backend/](backend/)) is a scaffold with a stub scorer — all dashboard numbers come from [frontend/src/data/mockData.js](frontend/src/data/mockData.js) today.

The full pre-build survey (utilities the dashboard offers, requirements per service, constraints, risks) is in **[STRATA_software_survey.pdf](STRATA_software_survey.pdf)** (re-generate via [utilities/generate_survey_pdf.py](utilities/generate_survey_pdf.py)).

---

## Architecture

The system as it would look once the survey's build-targets are in place. The frontend stays where it is; everything else is new or upgraded from the current stub.

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
       │                        API GATEWAY (Flask)                       │
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
| **Frontend** | Stages, lens routing, profile UI, SSE consumer | API gateway | — | Already built; needs router + a11y, drop TweaksPanel for prod. |
| **API gateway** | Auth check, rate limit, request routing, file-size cap | All services | Audit log | Stays as Flask; consider gunicorn + nginx. |
| **Auth & billing** | OAuth, magic-link, 2FA, sessions, Stripe webhooks, plan state | Postgres | Postgres | TOTP + recovery codes; deletion queue cascades here. |
| **Ingest service** | CV parser (PDF/DOC/DOCX/TXT → structured), JD NLP, taxonomy normalisation | Object store | Postgres, vector cache key | Single source for `parsed_cv` / `parsed_jd`. Idempotent on content hash. |
| **Embedding service** | One vector per CV, one per JD, versioned, cached | Ingest output | Vector store | Drives the "1536-d preview" the UI shows. |
| **Orchestrator** | Fan-out across 8 lens analyzers, stream 12 trace stages, assemble overview brief | Embeddings + ref data + analyzers | Postgres (`analyses`) | Owns the 14 s p50 budget. Trace via SSE, backed by Redis pub/sub. |
| **Lens analyzers** | One pure function per lens, returns the exact shape `mockData.js` declares | parsed_cv, parsed_jd, embeddings, ref data | — | Stateless. Can run in-process or split out per scale need. |
| **Reference data layer** | Peer corpus, comp dataset, posting feed, taxonomy | External partners / opt-in feed / scrape (decide) | — | Refresh ETL is its own pipeline. |
| **Profile service** | Account fields, security, data toggles, deletion scheduler | Postgres | Postgres | Soft-delete (30 d) then cascade purge to vectors + analyses. |
| **Export service** | Server-side PDF (Overview + active lens), share-brief signed URLs | Analyses, brand assets (fonts/OKLCH) | Object store | Headless Chromium or React-PDF. |
| **Observability** | Trace IDs (`0xNNNNN`), per-lens latency, model version, cost | All services emit | OTLP / log sink | Trace ID surfaces back into the UI. |

### Key request flows

#### Analyze (POST → SSE)

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

The hold-on / stall rule from the design spec lives in the orchestrator: if all stages complete before the UI animation, slow the last stage; if the engine stalls, the scan-line keeps moving but trace messages pause.

#### Lens fetch (GET)

```
Browser ──GET /api/analyses/{id}/lens/{lensId}──► Gateway
   Gateway ─► Orchestrator cache (Postgres `analyses.lens_payloads`)
   ◄── JSON in the exact shape mockData expects.
```

Cached at write-time during the original run; no recompute on lens switch.

#### Export brief (GET)

```
Browser ──GET /api/analyses/{id}/export.pdf──► Gateway
   Gateway ─► Export service
       Pulls overview + active lens JSON, renders via headless Chromium
       using the same OKLCH tokens + Google Fonts as the live UI.
   ◄── PDF stream.
```

### Data model (core tables)

```
users(id, email, oauth_provider, plan_id, two_factor_secret, created_at, …)
plans(id, name, stripe_customer_id, renews_at, …)
sessions(id, user_id, device, ip, last_active, current)
recovery_codes(id, user_id, code_hash, used_at)
deletion_requests(id, user_id, scheduled_at, status)

cvs(id, user_id, sha256, storage_url, retention_until, parsed_at)
parsed_cv(cv_id, structured_json)              -- employers[], titles[], …
embeddings(cv_id|jd_id, model_version, vector) -- pgvector

analyses(
  id, user_id, cv_id, jd_text,
  trace_id, model_version,
  started_at, finished_at,
  lens_payloads jsonb              -- 9 keys: overview, jdfit, ats, …
)

reference.peers(profile_id, vector, cohort_tags[], …)
reference.postings(role, geo, posted_at, jd_text, …)
reference.comp(role, geo, p25, p50, p75, source, vintage)
reference.taxonomy(canonical, synonyms[], type)  -- skills/titles/industries
```

### Deployment topology

Stays compatible with the existing ECS workflow ([.github/workflows/ecs-deployment.yaml](.github/workflows/ecs-deployment.yaml)) but introduces explicit services:

```
                       ┌───────────────────┐
                       │     CloudFront    │
                       │ (frontend assets) │
                       └────────┬──────────┘
                                │
                       ┌────────▼──────────┐
                       │       ALB         │
                       └────────┬──────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
   ┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
   │  api-gateway    │ │ orchestrator +  │ │   profile /     │
   │  (Flask)        │ │ lens analyzers  │ │   auth / billing│
   │  ECS service    │ │ ECS service     │ │   ECS service   │
   └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
            │                   │                   │
            └───────────────────┼───────────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
       ┌─────────┐         ┌─────────┐         ┌──────────┐
       │   RDS   │         │  Redis  │         │    S3    │
       │Postgres │         │ (cache  │         │ raw CVs  │
       │+pgvector│         │ + pub/  │         │+ exports │
       └─────────┘         │  sub)   │         └──────────┘
                           └─────────┘
   ┌───────────────────────────────────────────┐
   │   Reference data ETL (EventBridge cron)   │
   │   → S3 staging → RDS reference.* tables   │
   └───────────────────────────────────────────┘
   ┌───────────────────────────────────────────┐
   │   External: Embedding API, Stripe,        │
   │   OAuth providers, comp/peer data partner │
   └───────────────────────────────────────────┘
```

### Build order

The survey's build order maps onto this diagram:

1. **API gateway + ingest service + JDFit/ATS analyzers** — first vertical slice that produces honest numbers. No external data needed.
2. **Embedding service + vector cache** — unblocks every other lens.
3. **Reference data layer + ETL** — gate for SkillMatrix, Peer, Comp, Trends, Align (the data-acquisition decision).
4. **Orchestrator + SSE trace** — turns the animation into something real.
5. **Auth + billing + profile** — unlocks shippable accounts.
6. **Export + share** — last-mile polish.
7. **Observability + a11y + cross-browser** — pre-launch hardening.

---

## Repository layout

```
backend/
  interface.py           Flask entry point
  parsing_fun.py         CV parser
  similarity_score.py    Lexical scorer (placeholder)
  requirements.txt       Python deps
  utilities/             Helper scripts (PDF generation, …)
frontend/                React 18 + Vite app (hi-fi prototype)
  vitest.setup.js        Vitest runner setup
design_handoff_strata/   Canonical design reference (HTML/JSX/CSS)
test/
  frontend/              Vitest suites (213 tests, mirror frontend/src/)
  integration/data/      CV/JD fixtures
  real_data/             Real CV fixtures
Dockerfile               Container image
docker-compose.yaml      Local stack
.github/workflows/       CI + ECS deploy
```

## Local development

Backend:

```
pip install -r backend/requirements.txt
python -m backend.interface    # Flask dev server on :5000
# (or: cd backend && python interface.py)
```

Frontend:

```
cd frontend
npm install
npm run dev                    # Vite on :5173
npm run build                  # writes to frontend/dist (served by Flask)
```

Docker:

```
docker compose up --build
```
