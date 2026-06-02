# cv_parser

Parses CVs (`.pdf`, `.docx`, `.txt`) into a `ParsedCV` object and computes ATS red-flag signals along the way. Lives inside the `analyser` service (port `8002`); called by the `api` service over the docker network.

---

## Architecture

The module follows the project's 4-layer rule (higher number = leaf, lower = caller). One file per concern, one objective per function. Every function carries the standard `Calls` / `Called by` header.

```
backend/cv_parser/
├── models.py                       ParsedCV, Sections, AtsRedFlags (Pydantic, public)
│
├── leaves/                         L4 — unit functions (pure, no I/O)
│   ├── extraction_leaves.py        stream_order_anomaly, text_density,
│   │                               encoding_anomaly_rate, page_area
│   ├── cleaning_leaves.py          normalise_whitespace, distinct_bullet_chars,
│   │                               line_length_bimodality, hyphenation_break_rate
│   └── segmentation_leaves.py      is_heading, label_for_heading,
│                                   section_coherence_score, split_blocks_by_blank_line,
│                                   find_date_range
│
├── extractors.py                   L3 — extract_pdf, extract_docx, extract_text,
│                                        dispatch_by_extension
├── cleaner.py                      L3 — clean_text(raw) -> CleanedText
├── segmenter.py                    L3 — segment(cleaned) -> Sections
├── redflags.py                     L3 — build_ats_redflags(raw, cleaned, sections)
│
├── parser.py                       L2 — parse_cv(file_bytes, filename) -> ParsedCV
└── interface.py                    L1 — APIRouter, POST /cv/parse
```

### Data flow

```
file_bytes ──► dispatch_by_extension ──► RawExtraction
                                          │
                                          ├─► clean_text         ──► CleanedText
                                          │       │
                                          │       └──► segment   ──► Sections
                                          │
                                          └──► build_ats_redflags(raw, cleaned, sections)
                                                                    │
                                                                    ▼
                                                                ParsedCV
                                                                ├─ raw_text
                                                                ├─ sections
                                                                ├─ extraction_method
                                                                └─ ats_redflags
```

### Entry points

- **Library:** `from cv_parser.parser import parse_cv; parse_cv(file_bytes, filename)` — returns `ParsedCV`.
- **HTTP:** `POST /cv/parse` (multipart, field `file`) on the analyser service. Used by `API/clients/analyser_client.py`, which is called from `API/user_profile/service.create_profile`.

---

## What's done

### Extraction (`extractors.py`)
- Digital PDFs via `pdfplumber` — per-page text, per-char bboxes, page areas.
- DOCX via `python-docx` — paragraphs + table cell text.
- Plain text — UTF-8 with latin-1 fallback.
- Dispatch by file extension; unsupported extensions return `extraction_method="failed"`.
- Image-only PDFs are detected (empty text from `pdfplumber`) and flagged as `extraction_method="ocr_pdf"` — see *Pending* below.

### Cleaning (`cleaner.py`)
- Line-ending normalisation (`\r\n` / `\r` → `\n`).
- Whitespace collapsing.
- Returns a `CleanedText` carrying both the text and a list of lines (used downstream by line-shape signals).

### Segmentation (`segmenter.py`)
- Heading detector recognises a small canonical lexicon (`summary`, `experience`, `education`, `skills`, `projects`, `certifications`) plus aliases and ALL-CAPS / Title-Case heuristics.
- Experience and education blocks split on blank lines; first line ≈ title/degree, second line ≈ org/institution, date range pulled by regex; full block preserved in `description`.
- Skills bullet/comma split into `items`.
- Anything unclassified lands in `other`.

### ATS red flags (`redflags.py`)
All 10 signals from the spec are computed:

| Stage | Signal | Where |
|-------|--------|-------|
| extraction | `stream_order_anomaly` | char-stream reading-order checks |
| extraction | `text_density` | non-ws chars ÷ page area |
| extraction | `encoding_anomaly_rate` | weighted ratio of bad chars / mojibake |
| extraction | `extraction_method` | `digital_pdf` \| `ocr_pdf` \| `docx` \| `text` \| `failed` |
| cleaning   | `distinct_bullet_chars` | count of distinct bullet glyphs |
| cleaning   | `line_length_bimodality` | 0..1, >0.5 hints at columns |
| cleaning   | `hyphenation_break_rate` | mid-word `-\n` joins ÷ lines |
| segmentation | `heading_detection_rate` | sections found ÷ 7 expected |
| segmentation | `section_coherence` | per-section keyword hit rate (averaged) |
| segmentation | `unclassified_ratio` | `len(other) / len(raw_text)` |

### Plumbing
- FastAPI app at `backend/main.py` mounts the `cv_parser` router.
- Dedicated Dockerfile + Dockerfile.dev exposing port 8002.
- Added to both compose files; `api.depends_on` now includes `analyser` and gets `ANALYSER_URL=http://analyser:8002`.
- `API/clients/analyser_client.py` wraps the HTTP call.
- `API/user_profile/service.create_profile` reads the upload once, saves to disk, and fires a best-effort parse — failures are logged but don't break profile creation.
- `backend/upload_validation/file_validator.py` allow-list updated to `{pdf, docx, txt}` (dropped `.doc`).

---

## What's pending

### 1. Real OCR for image-only PDFs *(must-do before ingesting scanned résumés)*
Right now `extract_pdf` correctly identifies an image-only PDF and returns `extraction_method="ocr_pdf"` with empty text. The OCR step itself is stubbed.

**To finish:**
- Add `pytesseract` and `pdf2image` to `backend/requirements.txt`.
- Install `tesseract-ocr` and `poppler-utils` in `backend/Dockerfile` and `Dockerfile.dev` (`apt-get install -y tesseract-ocr poppler-utils`).
- In `extractors.extract_pdf`, when the digital path yields no text, rasterise via `pdf2image.convert_from_bytes(file_bytes, dpi=300)` and run `pytesseract.image_to_string` per page. Concatenate into `text` and keep `method="ocr_pdf"`.

### 2. Persistence of `ParsedCV`
Today, `create_profile` calls the analyser and only **logs** the result. The parsed object is not stored. Future work:
- New table `parsed_cvs` (one row per `cv_upload_id`) with JSONB columns for `sections` and `ats_redflags`, plus scalar columns for `extraction_method` and the top-line red-flag floats (so we can index/sort).
- `API/user_profile/queries.py` gains `insert_parsed_cv`.
- `service.create_profile` writes it inside the same transaction as `insert_cv_upload`.

### 3. Two-column reflow
When `line_length_bimodality > 0.5` we currently just flag it; the text still arrives in interleaved column order and segmentation suffers. Plan: post-process pdfplumber chars by x-clustering into column bands, re-emit the text in column-then-row order before handing to `clean_text`.

### 4. Heading & keyword lexicon
`SECTION_ALIASES` and `SECTION_KEYWORDS` in `leaves/segmentation_leaves.py` cover the obvious cases only. Extend as real CVs surface mis-classifications. Consider moving the lexicon to a YAML/JSON asset so non-engineers can edit it.

### 5. Date parsing
`find_date_range` is a single regex tuned for common English formats (`Jan 2022 - Present`, `2020-2024`). For non-English or unusual layouts, swap to `dateparser`.

### 6. Tests
No tests yet. Plan:
- Fixtures in `test/real_data/cv_parser/`: clean digital PDF, image-only PDF, two-column PDF, docx, txt.
- Unit tests calling `parse_cv` directly and asserting `extraction_method`, key sections, and red-flag sanity bounds.
- HTTP integration test against the running analyser container (`POST /cv/parse`).

### 7. Public `/api/cv/parse` proxy *(optional)*
If the frontend ever needs to parse a CV outside the profile-creation flow, add a thin router in `API/cv_parser/interface.py` that just calls `analyser_client.parse_cv`.

---

## Next steps (priority order)

1. **Persist `ParsedCV`** — without this the downstream lenses (`ats_scorer`, `skill_matrix`, …) have nothing to read from. Add table + `insert_parsed_cv` + transactional write.
2. **Write tests + sample fixtures** before extending heuristics, so future tuning doesn't silently regress.
3. **Wire OCR** (#1 above) so scanned résumés stop returning empty text.
4. **Column reflow** (#3) — biggest quality lift for real-world CVs.
5. **Lexicon expansion** (#4) — incremental, driven by mis-classifications we see in real data.
6. **Date parsing upgrade** (#5) — defer until non-English CVs become a use case.
