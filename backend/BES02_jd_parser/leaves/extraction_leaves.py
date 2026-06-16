import csv
import io
import json
import re


# ── Seniority ────────────────────────────────────────────────────────────────

_SENIORITY_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bintern(ship)?\b", re.I),                              "intern"),
    (re.compile(r"\bjunior\b|\bassociate\b|\bentry.level\b", re.I),       "junior"),
    (re.compile(r"\bsenior\b|\bsr\.?\b", re.I),                           "senior"),
    (re.compile(r"\blead\b|\bstaff\b|\bprincipal\b", re.I),               "lead"),
    (re.compile(r"\bmanager\b|\bhead\s+of\b", re.I),                      "manager"),
    (re.compile(r"\bdirector\b|\bvp\b|\bvice\s+president\b|\bchief\b", re.I), "director"),
]


# -------------------- infer_seniority ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: extractor.extract_header
def infer_seniority(title: str) -> str:
    """Return seniority level derived from the job title string.
    Falls back to 'mid' when no pattern matches."""
    for pattern, level in _SENIORITY_PATTERNS:
        if pattern.search(title):
            return level
    return "mid"
# -------------------- infer_seniority ------------- END ----------------


# ── Salary ───────────────────────────────────────────────────────────────────

_CURRENCY_MAP = {"£": "GBP", "$": "USD", "€": "EUR"}

_SALARY_RE = re.compile(
    r"(?P<sym>[£$€]|USD|GBP|EUR)\s*"
    r"(?P<min>\d[\d,]*(?:\.\d+)?)\s*(?P<mink>[kK])?"
    r"(?:"
    r"\s*[-–—to]+\s*"
    r"(?:[£$€])?\s*"
    r"(?P<max>\d[\d,]*(?:\.\d+)?)\s*(?P<maxk>[kK])?"
    r")?",
    re.IGNORECASE,
)


def _parse_amount(digits: str, k_suffix: str | None) -> float | None:
    stripped = digits.replace(",", "")
    if not stripped:
        return None
    val = float(stripped)
    if k_suffix:
        val *= 1000
    return val


# -------------------- extract_salary ----------- START ----------
# -- Calls : _parse_amount
# -- Called by: extractor.extract_header
def extract_salary(text: str) -> dict | None:
    """Return a salary dict {min, max, currency, raw} or None if not found."""
    m = _SALARY_RE.search(text)
    if not m:
        return None
    sym = m.group("sym")
    currency = _CURRENCY_MAP.get(sym, sym.upper())
    min_val = _parse_amount(m.group("min"), m.group("mink"))
    if min_val is None:
        return None
    max_val = _parse_amount(m.group("max"), m.group("maxk")) if m.group("max") else None
    return {
        "min": min_val,
        "max": max_val,
        "currency": currency,
        "raw": m.group(0).strip(),
    }
# -------------------- extract_salary ------------- END ----------------


# ── Location ─────────────────────────────────────────────────────────────────

_LOCATION_RE = re.compile(
    r"\b(remote|hybrid|on.?site|london|manchester|edinburgh|bristol|birmingham|"
    r"leeds|glasgow|liverpool|cambridge|oxford|new york|san francisco|"
    r"[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2})\b",
    re.IGNORECASE,
)


# -------------------- extract_location ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: extractor.extract_header
def extract_location(lines: list[str]) -> str | None:
    """Scan header lines for a location token. Returns first match or None."""
    for line in lines:
        m = _LOCATION_RE.search(line)
        if m:
            return m.group(0).strip()
    return None
# -------------------- extract_location ------------- END ----------------


# ── Employment type ───────────────────────────────────────────────────────────

_EMPLOYMENT_RE = re.compile(
    r"\b(full.?time|part.?time|contract|permanent|freelance|temporary|fixed.?term)\b",
    re.IGNORECASE,
)

_EMPLOYMENT_CANONICAL = {
    "fulltime": "full-time", "full-time": "full-time", "full time": "full-time",
    "parttime": "part-time", "part-time": "part-time", "part time": "part-time",
    "contract": "contract",
    "permanent": "permanent",
    "freelance": "freelance",
    "temporary": "temporary",
    "fixedterm": "fixed-term", "fixed-term": "fixed-term", "fixed term": "fixed-term",
}


# -------------------- extract_employment_type ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: extractor.extract_header
def extract_employment_type(lines: list[str]) -> str | None:
    for line in lines:
        m = _EMPLOYMENT_RE.search(line)
        if m:
            raw = m.group(0).lower().replace(" ", "")
            return _EMPLOYMENT_CANONICAL.get(raw, m.group(0).lower())
    return None
# -------------------- extract_employment_type ------------- END ----------------


# ── Company ───────────────────────────────────────────────────────────────────

_AT_COMPANY_RE = re.compile(r"\bat\s+([A-Z][A-Za-z0-9\s&.,'-]{1,50}?)(?:\s*[,|·\-–—]|$)")
_STANDALONE_ORG_RE = re.compile(r"^([A-Z][A-Za-z0-9\s&.,'-]{2,50}(?:\s(?:Ltd|Limited|Inc|LLC|PLC|Corp|Group|Technologies?|Solutions?|Systems?|Digital|Labs?)))\s*$")


# -------------------- extract_company ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: extractor.extract_header
def extract_company(header_lines: list[str]) -> str | None:
    """Try 'at Company' suffix on any header line, then standalone org-looking lines."""
    for line in header_lines:
        m = _AT_COMPANY_RE.search(line)
        if m:
            return m.group(1).strip()
    for line in header_lines:
        m = _STANDALONE_ORG_RE.match(line.strip())
        if m:
            return m.group(1).strip()
    return None
# -------------------- extract_company ------------- END ----------------


# ── JSON / CSV flattening ─────────────────────────────────────────────────────

def _collect_strings(obj) -> list[str]:
    if isinstance(obj, str):
        return [obj] if obj.strip() else []
    if isinstance(obj, dict):
        parts = []
        for k, v in obj.items():
            parts.extend(_collect_strings(v))
        return parts
    if isinstance(obj, list):
        parts = []
        for item in obj:
            parts.extend(_collect_strings(item))
        return parts
    return []


# -------------------- flatten_json ----------- START ----------
# -- Calls : _collect_strings
# -- Called by: extractor.dispatch_file
def flatten_json(data: bytes) -> str:
    """Recursively collect all string leaf values from a JSON blob."""
    try:
        obj = json.loads(data.decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        return data.decode("utf-8", errors="replace")
    return "\n".join(_collect_strings(obj))
# -------------------- flatten_json ------------- END ----------------


# -------------------- flatten_csv ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: extractor.dispatch_file
def flatten_csv(data: bytes) -> str:
    """Flatten a CSV into plain text. Header row used as field-name prefixes."""
    text = data.decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return ""
    headers = rows[0] if rows else []
    use_headers = all(h and not h.strip().lstrip("-").isdigit() and len(h) <= 30 for h in headers)
    parts: list[str] = []
    for row in (rows[1:] if use_headers else rows):
        for i, cell in enumerate(row):
            cell = cell.strip()
            if not cell:
                continue
            if use_headers and i < len(headers):
                parts.append(f"{headers[i]}: {cell}")
            else:
                parts.append(cell)
    return "\n".join(parts)
# -------------------- flatten_csv ------------- END ----------------
