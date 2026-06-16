"""
Generates eval_data/labelled/pairs.jsonl for scorer benchmarking.

Three pair types:
  high_match    – same domain + skills aligned + seniority/experience aligned
  confusing     – same domain + skills NOT aligned (TF-IDF blind spot)
  high_mismatch – completely different domain (obvious mismatch)

JD and CV selections are explicit (not random). Sub-scores are derived from
reading the actual content of each document.

Usage (from backend/ directory):
    python -m cv_jd_scorer.common.scripts.generate_pairs
"""
import json
import random
import re
import sys
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

SEED = 42
N_PER_TYPE = 100
BACKEND = Path("BES02_JDResumeScorer")
JD_FILE = BACKEND / "eval_data/raw_jd/selected_job_descriptions.jsonl"
CV_DIR = BACKEND / "eval_data/raw/triaged"
OUT_FILE = BACKEND / "eval_data/labelled/pairs.jsonl"

# ── Manually selected JD IDs ──────────────────────────────────────────────────
# Each domain group chosen for coverage; IDs verified to have raw_text + requirements.

SELECTED_JD_IDS_BY_DOMAIN = {
    # ── Software Engineering (Java/Python/TS/full-stack) ──
    "SWE": [
        18583,   # Sr. Software Engineer – Java, Node.js, TypeScript, REST, NCR
        18472,   # Senior Software Engineer – Java, Integration Platform, UKG
        15560,   # Sr. Fullstack Engineer – React, TS, NodeJS, MongoDB, Zeal
        17790,   # Senior Android Engineer – Kotlin, Java, Instacart
        16048,   # Backend Software Engineer – Python 5yrs, McGovern Foundation
        985,     # Senior Software Engineer – TDD, full-stack, 7-10yrs
        9747,    # Senior Software Engineer – bodyport (general SE)
        8944,    # Staff Software Engineer – Cloud Networking, Starburst
        11903,   # Lead Software Engineer – BOSSCAT
        6790,    # Team Lead Engineering – SoSafe (3yrs leadership + SWE)
    ],
    # ── Data Engineering ──
    "DATA_ENG": [
        9723,    # Senior Data Engineer – Python, Kafka, Ethereum, 5yrs
        14308,   # Sr. Data Engineer BigQuery – SQL, GCP, 8yrs, Applied Systems
        14662,   # Senior Data Engineer – Scala, Java, Python, Quantexa
    ],
    # ── Data Science / ML / AI ──
    "DATA_SCI": [
        13711,   # Data Scientist Media Consultant – ML, statistics, media analytics
        7341,    # Senior AI Engineer – CS/AI degree, remberg
        14894,   # Data Scientist II Customer Analytics – 3yrs, stats
        9515,    # Data Scientist Customer Experience – General Motors
    ],
    # ── DevOps / SRE / Cloud ──
    "DEVOPS": [
        2586,    # Senior Cloud Engineer – 10yrs infra, 5yrs cloud, Advantage
        544,     # Senior Site Reliability Engineer – K8s, Docker, Python, Grafana
        12596,   # Principal DevOps Engineer – SME, cloud platforms
        10026,   # Sr. DevOps Engineer – 6yrs SRE/DevOps
    ],
    # ── Analytics / Data Analyst ──
    "ANALYTICS": [
        20052,   # Consultant PMO/Data Analytics – 2yrs, master's, SQL
        8691,    # Senior Data Analyst – SQL/Tableau/PowerBI, 2-4yrs
        11033,   # Lead Data Analyst – 8-9yrs, business analysis
    ],
    # ── QA / Testing ──
    "QA": [
        5697,    # QA Engineer – 3-5yrs, Selenium, RSpec, jMeter
        6815,    # Senior QA Engineer – Scalapay
    ],
    # ── Engineering Management ──
    "MANAGEMENT": [
        10719,   # Director Partner Strategy – enterprise deals, Metropolis
        21115,   # Director Data & Analytics – 8yrs, team building
        18791,   # Manager Engineering Operations – Wavelo/Tucows
        19755,   # VP of Engineering
    ],
    # ── Finance / Accounting ──
    "FINANCE": [
        102,     # Finance Business Analyst – Apex Fintech
        16406,   # Senior Accountant Technical Accounting – 4yrs, Big4
    ],
    # ── Sales ──
    "SALES": [
        8377,    # Account Executive – Merit, client relationships
        830,     # Sales Data Analyst – Madhive, SQL, Looker
    ],
}

# ── CV category pools per pair type ──────────────────────────────────────────

HIGH_MATCH_CV_CATS: dict[str, list[str]] = {
    "SWE":        ["INFORMATION-TECHNOLOGY", "ENGINEERING"],
    "DATA_ENG":   ["INFORMATION-TECHNOLOGY", "ENGINEERING"],
    "DATA_SCI":   ["INFORMATION-TECHNOLOGY", "ENGINEERING"],
    "DEVOPS":     ["INFORMATION-TECHNOLOGY", "ENGINEERING"],
    "ANALYTICS":  ["INFORMATION-TECHNOLOGY", "FINANCE"],
    "QA":         ["INFORMATION-TECHNOLOGY", "ENGINEERING"],
    "MANAGEMENT": ["INFORMATION-TECHNOLOGY"],
    "FINANCE":    ["FINANCE", "BANKING", "ACCOUNTANT"],
    "SALES":      ["SALES", "BUSINESS-DEVELOPMENT"],
}

# Confusing CVs come from the SAME broad domain category as high_match but
# represent wrong specialisation or wrong seniority level — the keyword
# matcher can't distinguish these from real matches.
CONFUSING_CV_CATS: dict[str, list[str]] = {
    "SWE":        ["INFORMATION-TECHNOLOGY"],
    "DATA_ENG":   ["INFORMATION-TECHNOLOGY"],
    "DATA_SCI":   ["INFORMATION-TECHNOLOGY"],
    "DEVOPS":     ["INFORMATION-TECHNOLOGY"],
    "ANALYTICS":  ["INFORMATION-TECHNOLOGY"],
    "QA":         ["INFORMATION-TECHNOLOGY"],
    "MANAGEMENT": ["INFORMATION-TECHNOLOGY"],
    "FINANCE":    ["INFORMATION-TECHNOLOGY"],
    "SALES":      ["INFORMATION-TECHNOLOGY", "DIGITAL-MEDIA"],
}

# Mismatch CVs are always from unrelated professions.
MISMATCH_CV_CATS: list[str] = ["CHEF", "TEACHER", "HEALTHCARE", "FITNESS", "AVIATION"]

# ── Helper constants ──────────────────────────────────────────────────────────

STOP_WORDS = {
    "with", "have", "that", "this", "will", "from", "your", "they", "been",
    "more", "also", "such", "other", "into", "than", "some", "their",
    "experience", "work", "team", "role", "must", "able", "good", "what",
    "where", "when", "which", "about", "using", "including", "within",
    "across", "strong", "skills", "ability", "knowledge", "looking",
    "required", "preferred", "years", "least", "least", "minimum",
}

SENIORITY_ORDER = ["intern", "junior", "mid", "senior", "lead", "manager", "director"]
SENIORITY_PATTERNS = [
    (r"\bintern\b|\binternship\b",                         "intern"),
    (r"\bjunior\b|\bassociate\b|\bentry.level\b",          "junior"),
    (r"\bsenior\b|\bsr\.?\b",                              "senior"),
    (r"\blead\b|\bstaff\b|\bprincipal\b",                  "lead"),
    (r"\bmanager\b|\bhead of\b",                           "manager"),
    (r"\bdirector\b|\bvp\b|\bvice president\b|\bchief\b",  "director"),
]

DOMAIN_GROUPS: dict[str, str] = {
    "INFORMATION-TECHNOLOGY": "TECH", "ENGINEERING": "TECH",
    "FINANCE": "FINANCE", "BANKING": "FINANCE", "ACCOUNTANT": "FINANCE",
    "SALES": "SALES", "BUSINESS-DEVELOPMENT": "SALES",
    "DESIGNER": "CREATIVE", "ARTS": "CREATIVE", "DIGITAL-MEDIA": "CREATIVE",
    "HR": "HR", "HEALTHCARE": "HEALTH", "FITNESS": "HEALTH",
    "CHEF": "FOOD", "TEACHER": "EDUCATION",
    "AVIATION": "TRANSPORT", "AUTOMOBILE": "TRANSPORT",
}

JD_DOMAIN_GROUPS: dict[str, str] = {
    "SWE": "TECH", "DATA_ENG": "TECH", "DATA_SCI": "TECH",
    "DEVOPS": "TECH", "ANALYTICS": "TECH", "QA": "TECH", "MANAGEMENT": "TECH",
    "FINANCE": "FINANCE", "SALES": "SALES",
}

# ── Utility functions ─────────────────────────────────────────────────────────

def infer_seniority(title: str) -> str:
    t = (title or "").lower()
    for pat, level in SENIORITY_PATTERNS:
        if re.search(pat, t):
            return level
    return "mid"


def infer_cv_seniority(cv: dict) -> str:
    exp = cv.get("sections", {}).get("experience", [])
    if isinstance(exp, list):
        for e in exp[:2]:
            t = e.get("title", "") or ""
            if t and t not in ("Company Name", ""):
                return infer_seniority(t)
    return "mid"


def extract_jd_terms(jd: dict) -> set[str]:
    req_text = (
        jd.get("sections", {}).get("requirements", "")
        + " ".join(jd.get("required_qualifications", []))
    )
    if len(req_text) < 100:
        req_text = jd.get("raw_text", "")[:3000]
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.]{2,}\b", req_text)
    return {w.lower() for w in words if w.lower() not in STOP_WORDS and len(w) > 3}


def skill_overlap_ratio(cv: dict, jd_terms: set[str]) -> float:
    items = cv.get("sections", {}).get("skills", {})
    if isinstance(items, dict):
        items = items.get("items", []) or []
    cv_text = " ".join(str(s) for s in items).lower()
    if not jd_terms:
        return 0.0
    hits = sum(1 for t in jd_terms if t in cv_text)
    return hits / len(jd_terms)


def extract_required_years(jd: dict) -> int:
    text = jd.get("raw_text", "") + " ".join(jd.get("required_qualifications", []))
    m = re.search(r"(\d+)\+?\s*(?:to\s*\d+)?\s*years?", text, re.IGNORECASE)
    return int(m.group(1)) if m else 3


def estimate_cv_years(cv: dict) -> int:
    exp = cv.get("sections", {}).get("experience", [])
    if isinstance(exp, list):
        return max(1, len(exp) * 2)
    return 2


# ── Sub-score computation ─────────────────────────────────────────────────────

def compute_subscores(cv: dict, jd: dict, jd_domain: str) -> tuple[dict, int]:
    cv_cat = cv.get("_category", "")

    # 1. keyword_overlap (max 20)
    jd_text_raw = jd.get("raw_text", "").lower()
    cv_text_raw = cv.get("raw_text", "").lower()
    jd_words = {
        w for w in re.findall(r"\b\w{4,}\b", jd_text_raw)
        if w not in STOP_WORDS
    }
    cv_words = set(re.findall(r"\b\w{4,}\b", cv_text_raw))
    kw_overlap = len(jd_words & cv_words) / max(len(jd_words), 1) if jd_words else 0
    keyword_score = min(20, int(kw_overlap * 80))

    # 2. domain (max 20) — computed early; used to scale seniority + experience
    cv_group = DOMAIN_GROUPS.get(cv_cat, "OTHER")
    jd_group = JD_DOMAIN_GROUPS.get(jd_domain, "OTHER")
    if cv_group == jd_group:
        domain_score = 20
    elif cv_group not in ("OTHER", "FOOD", "EDUCATION", "HEALTH", "TRANSPORT"):
        domain_score = 8
    else:
        domain_score = 2
    domain_factor = domain_score / 20  # 0..1; scales seniority + experience

    # 3. seniority (max 15) — only meaningful within the same domain
    jd_seniority = jd.get("seniority") or infer_seniority(jd.get("source_title", ""))
    cv_seniority = infer_cv_seniority(cv)
    try:
        jd_level = SENIORITY_ORDER.index(jd_seniority or "mid")
        cv_level = SENIORITY_ORDER.index(cv_seniority or "mid")
    except ValueError:
        jd_level = cv_level = 2
    gap = abs(jd_level - cv_level)
    raw_seniority = [15, 11, 6, 3, 1, 0, 0][min(gap, 6)]
    seniority_score = max(0, int(raw_seniority * domain_factor))

    # 4. skills (max 25)
    jd_terms = extract_jd_terms(jd)
    cv_skills_raw = cv.get("sections", {}).get("skills", {})
    if isinstance(cv_skills_raw, dict):
        cv_skill_items = set(str(s).lower() for s in (cv_skills_raw.get("items") or []))
    else:
        cv_skill_items = set()
    if jd_terms:
        skill_hits = sum(1 for t in jd_terms if t in cv_skill_items)
        skills_score = min(25, int(skill_hits / len(jd_terms) * 100))
    else:
        skills_score = 5

    # 5. experience (max 20) — only meaningful within same domain
    req_years = extract_required_years(jd)
    cv_years = estimate_cv_years(cv)
    if cv_years >= req_years:
        raw_experience = 18
    elif cv_years >= max(1, int(req_years * 0.7)):
        raw_experience = 12
    elif cv_years >= max(1, int(req_years * 0.4)):
        raw_experience = 6
    else:
        raw_experience = 2
    experience_score = max(0, int(raw_experience * domain_factor))

    total = keyword_score + seniority_score + domain_score + skills_score + experience_score

    subscores = {
        "keyword_overlap": keyword_score,
        "seniority":       seniority_score,
        "domain":          domain_score,
        "skills":          skills_score,
        "experience":      experience_score,
    }
    return subscores, total


# ── Data loading ──────────────────────────────────────────────────────────────

def load_cv_pool(cv_dir: Path) -> dict[str, list[dict]]:
    pool: dict[str, list[dict]] = {}
    for cat_path in sorted(cv_dir.iterdir()):
        if not cat_path.is_dir():
            continue
        ok_file = cat_path / "parsed_ok.jsonl"
        if not ok_file.exists():
            continue
        cvs = [
            json.loads(line)
            for line in ok_file.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip()
        ]
        for cv in cvs:
            cv["_category"] = cat_path.name
        pool[cat_path.name] = cvs
    return pool


def load_jd_pool(jd_file: Path, selected: dict[str, list[int]]) -> dict[str, list[dict]]:
    all_jds: dict[int, dict] = {}
    for line in jd_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        jd = json.loads(line)
        all_jds[int(jd["jd_id"])] = jd
    result: dict[str, list[dict]] = {}
    for domain, ids in selected.items():
        found = [all_jds[i] for i in ids if i in all_jds]
        result[domain] = found
    return result


def get_cvs(cv_pool: dict[str, list[dict]], cats: list[str]) -> list[dict]:
    out = []
    for cat in cats:
        out.extend(cv_pool.get(cat, []))
    return out


# ── Pair construction ─────────────────────────────────────────────────────────

def make_pair(jd: dict, cv: dict, label: str, subscores: dict, total: int, idx: int) -> dict:
    cv_fname = cv.get("filename", "unknown")
    pair_id = f"jd{jd['jd_id']}_{cv_fname.replace('.pdf','')[:10]}_{label[:4]}_{idx}"
    return {
        "pair_id":            pair_id,
        "match_label":        label,
        "jd_id":              jd["jd_id"],
        "parsed_cv": {
            "raw_text":     cv.get("raw_text", ""),
            "sections":     cv.get("sections", {}),
            "ats_redflags": cv.get("ats_redflags", {}),
            "filename":     cv_fname,
        },
        "jd_text":             jd.get("raw_text", ""),
        "parsed_jd":           {k: v for k, v in jd.items() if k != "raw_text"},
        "expected_jd_score":   total,
        "expected_subscores":  subscores,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    rng = random.Random(SEED)
    cv_pool = load_cv_pool(CV_DIR)
    jd_pool = load_jd_pool(JD_FILE, SELECTED_JD_IDS_BY_DOMAIN)

    # Flat list of (domain, jd)
    jd_flat = [(domain, jd) for domain, jds in jd_pool.items() for jd in jds]

    pairs: list[dict] = []
    used: set[tuple] = set()  # (jd_id, cv_filename, label)

    label_configs = [
        (
            "high_match",
            lambda d: HIGH_MATCH_CV_CATS.get(d, []),
            lambda cv, terms: skill_overlap_ratio(cv, terms) >= 0.10,
        ),
        (
            "confusing",
            lambda d: CONFUSING_CV_CATS.get(d, []),
            lambda cv, terms: skill_overlap_ratio(cv, terms) < 0.08,
        ),
        (
            "high_mismatch",
            lambda _: MISMATCH_CV_CATS,
            lambda cv, terms: True,  # no skill filter for cross-domain
        ),
    ]

    for label, get_cats_fn, filter_fn in label_configs:
        added = 0
        counter = 0

        for _pass in range(30):  # multiple passes to hit N_PER_TYPE
            rng.shuffle(jd_flat)
            for domain, jd in jd_flat:
                if added >= N_PER_TYPE:
                    break
                cats = get_cats_fn(domain)
                candidates = get_cvs(cv_pool, cats)
                jd_terms = extract_jd_terms(jd)
                filtered = [cv for cv in candidates if filter_fn(cv, jd_terms)]
                rng.shuffle(filtered)

                for cv in filtered:
                    key = (jd["jd_id"], cv.get("filename", ""), label)
                    if key in used:
                        continue
                    used.add(key)
                    subscores, total = compute_subscores(cv, jd, domain)
                    pairs.append(make_pair(jd, cv, label, subscores, total, counter))
                    counter += 1
                    added += 1
                    if added >= N_PER_TYPE:
                        break

            if added >= N_PER_TYPE:
                break

        print(f"  {label:16s}: {added:3d} pairs", file=sys.stderr)

    OUT_FILE.write_text(
        "\n".join(json.dumps(p, ensure_ascii=False) for p in pairs) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {len(pairs)} pairs → {OUT_FILE}", file=sys.stderr)


if __name__ == "__main__":
    main()
