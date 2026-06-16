import re


CANONICAL_SECTIONS = (
    "summary",
    "experience",
    "education",
    "skills",
    "projects",
    "certifications",
    "other",
)

# Frozen v1 canonical header list. Feeds ats_redflags (heading_detection_rate)
# and MUST NEVER inherit extraction improvements — bump the version and add a
# new constant if the ATS-signal definition itself ever changes.
STRICT_SECTION_ALIASES_V1 = {
    "summary":        ("summary", "profile", "objective", "about me", "about", "professional summary"),
    "experience":     ("experience", "work experience", "employment", "professional experience", "work history", "career"),
    "education":      ("education", "academic background", "qualifications", "academics"),
    "skills":         ("skills", "technical skills", "core competencies", "competencies", "key skills"),
    "projects":       ("projects", "personal projects", "selected projects", "portfolio"),
    "certifications": ("certifications", "certificates", "licenses", "courses"),
}

# Backward-compatible name; strict list is the default matching behaviour.
SECTION_ALIASES = STRICT_SECTION_ALIASES_V1

# Synonym list for section extraction only. Grows freely as new header
# variants are discovered; never feeds heading_detection_rate.
FUZZY_SECTION_ALIASES = {
    "summary":        STRICT_SECTION_ALIASES_V1["summary"] + (
        "professional profile", "executive summary", "executive profile",
        "career overview", "career focus", "summary of qualifications",
        "career summary", "professional overview",
    ),
    "experience":     STRICT_SECTION_ALIASES_V1["experience"] + (
        "relevant experience", "career history", "employment history",
        "work experience and qualifications",
    ),
    "education":      STRICT_SECTION_ALIASES_V1["education"] + (
        "education and training", "academic qualifications", "educational background",
    ),
    "skills":         STRICT_SECTION_ALIASES_V1["skills"] + (
        "skill highlights", "highlights", "areas of expertise", "expertise",
        "technical proficiencies", "summary of skills",
    ),
    "projects":       STRICT_SECTION_ALIASES_V1["projects"] + (
        "key projects", "academic projects",
    ),
    "certifications": STRICT_SECTION_ALIASES_V1["certifications"] + (
        "certifications and licenses", "licenses and certifications",
    ),
}

SECTION_KEYWORDS = {
    "summary":        ("years", "experienced", "passionate", "specialist", "background"),
    "experience":     ("manager", "engineer", "developer", "led", "managed", "team", "company", "ltd", "inc"),
    "education":      ("university", "college", "school", "bachelor", "master", "phd", "degree", "diploma", "gpa"),
    "skills":         ("python", "java", "sql", "aws", "docker", "react", "kubernetes", "javascript", "agile"),
    "projects":       ("built", "developed", "designed", "implemented", "github", "open source"),
    "certifications": ("certified", "certificate", "certification", "license", "issued"),
}

_DATE_RANGE_RE = re.compile(
    r"(?P<start>(?:\d{1,2}[/-])?(?:\d{4}|\w+\s+\d{4}|\w+\.\s*\d{4}))"
    r"\s*(?:-|–|—|to)\s*"
    r"(?P<end>present|current|\d{1,2}[/-]?\d{0,4}|\w+\s+\d{4}|\w+\.\s*\d{4}|\d{4})",
    re.IGNORECASE,
)


# -------------------- is_heading ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: group_lines_by_heading
def is_heading(line: str, alias_map: dict[str, tuple[str, ...]] = STRICT_SECTION_ALIASES_V1) -> bool:
    stripped = line.strip().rstrip(":")
    if not stripped or len(stripped) > 40:
        return False
    if stripped.isupper():
        return True
    lower = stripped.lower()
    for aliases in alias_map.values():
        if lower in aliases:
            return True
    words = stripped.split()
    if len(words) <= 5 and all(w[:1].isupper() for w in words if w):
        return any(lower.startswith(a.split()[0]) for aliases in alias_map.values() for a in aliases)
    return False
# -------------------- is_heading ------------- END ----------------


# -------------------- label_for_heading ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: group_lines_by_heading
def label_for_heading(line: str, alias_map: dict[str, tuple[str, ...]] = STRICT_SECTION_ALIASES_V1) -> str | None:
    lower = line.strip().rstrip(":").lower()
    for canonical, aliases in alias_map.items():
        for alias in aliases:
            if lower == alias or lower.startswith(alias + " "):
                return canonical
    return None
# -------------------- label_for_heading ------------- END ----------------


# -------------------- group_lines_by_heading ----------- START ----------
# -- Calls : is_heading, label_for_heading
# -- Called by: segment (segmenter.py), build_ats_redflags (redflags.py)
def group_lines_by_heading(
    lines: list[str],
    alias_map: dict[str, tuple[str, ...]],
) -> dict[str, str]:
    buckets: dict[str, list[str]] = {name: [] for name in CANONICAL_SECTIONS}
    current = "other"
    for line in lines:
        if is_heading(line, alias_map):
            label = label_for_heading(line, alias_map)
            if label is not None:
                current = label
                continue
        buckets[current].append(line)
    return {k: "\n".join(v).strip() for k, v in buckets.items()}
# -------------------- group_lines_by_heading ------------- END ----------------


# -------------------- section_coherence_score ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def section_coherence_score(section_name: str, content: str) -> float:
    keywords = SECTION_KEYWORDS.get(section_name)
    if not keywords or not content:
        return 0.0
    lines = [ln for ln in content.splitlines() if ln.strip()]
    if not lines:
        return 0.0
    hits = 0
    for ln in lines:
        low = ln.lower()
        if any(kw in low for kw in keywords):
            hits += 1
    return hits / len(lines)
# -------------------- section_coherence_score ------------- END ----------------


# -------------------- split_blocks_by_blank_line ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: _split_entries (segmenter.py)
def split_blocks_by_blank_line(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.strip():
            current.append(line)
        elif current:
            blocks.append("\n".join(current))
            current = []
    if current:
        blocks.append("\n".join(current))
    return blocks
# -------------------- split_blocks_by_blank_line ------------- END ----------------


# -------------------- find_date_range ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: _split_entries (segmenter.py)
def find_date_range(text: str) -> str | None:
    m = _DATE_RANGE_RE.search(text)
    return m.group(0) if m else None
# -------------------- find_date_range ------------- END ----------------


_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")


# -------------------- find_year ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: _split_education (segmenter.py)
def find_year(text: str) -> str | None:
    m = _YEAR_RE.search(text)
    return m.group(0) if m else None
# -------------------- find_year ------------- END ----------------


# -------------------- count_date_ranges ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def count_date_ranges(text: str) -> int:
    return len(_DATE_RANGE_RE.findall(text))
# -------------------- count_date_ranges ------------- END ----------------


# -------------------- strip_date_substrings ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: _parse_experience_entry, _parse_education_entry (segmenter.py)
def strip_date_substrings(line: str) -> str:
    stripped = _DATE_RANGE_RE.sub("", line)
    stripped = re.sub(r"\s{2,}", " ", stripped)
    return stripped.strip(" \t-–—:|,.")
# -------------------- strip_date_substrings ------------- END ----------------


# -------------------- strip_year_substrings ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: _parse_education_entry (segmenter.py)
def strip_year_substrings(line: str) -> str:
    stripped = _YEAR_RE.sub("", line)
    stripped = re.sub(r"\s{2,}", " ", stripped)
    return stripped.strip(" \t-–—:|,.")
# -------------------- strip_year_substrings ------------- END ----------------


# -- look-back guards: a pulled line must plausibly be a title/org line,
#    not a wrapped sentence or description bullet
_MAX_PULL_LINES = 2
_MAX_PULL_LEN = 80


def _pullable(line: str) -> bool:
    if not line or len(line) > _MAX_PULL_LEN:
        return False
    # sentence-like (long + trailing period) → description/objective text
    if line.endswith(".") and len(line.split()) > 4:
        return False
    return True


# -------------------- split_blocks_by_anchor ----------- START ----------
# -- Calls : _pullable
# -- Called by: _split_experience, _split_education (segmenter.py)
def split_blocks_by_anchor(text: str, is_anchor, anchor_remainder=None) -> tuple[str, list[str]]:
    """Split text into (preamble, blocks). Each anchor line starts a new
    block; lines before the first anchor form the preamble.

    When `anchor_remainder` is given and the anchor line is date-only
    (remainder empty), up to 2 short preceding lines are pulled into the
    block as title/org candidates — handles the `Title\\nOrg\\nDates` layout
    without letting sentence-like preamble leak into entries."""
    lines = text.splitlines()
    anchor_idx = [i for i, ln in enumerate(lines) if is_anchor(ln)]
    if not anchor_idx:
        return text.strip(), []

    starts: list[int] = []
    prev_anchor = -1
    for i in anchor_idx:
        start = i
        if anchor_remainder is not None and not anchor_remainder(lines[i]):
            j = i - 1
            pulled = 0
            while j > prev_anchor and pulled < _MAX_PULL_LINES:
                cand = lines[j].strip()
                if is_anchor(cand) or not _pullable(cand):
                    break
                start = j
                pulled += 1
                j -= 1
        starts.append(start)
        prev_anchor = i

    preamble = "\n".join(lines[: starts[0]]).strip()
    bounds = starts + [len(lines)]
    blocks = ["\n".join(lines[bounds[k]: bounds[k + 1]]).strip() for k in range(len(starts))]
    return preamble, blocks
# -------------------- split_blocks_by_anchor ------------- END ----------------
