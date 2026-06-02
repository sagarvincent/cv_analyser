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

SECTION_ALIASES = {
    "summary":        ("summary", "profile", "objective", "about me", "about", "professional summary"),
    "experience":     ("experience", "work experience", "employment", "professional experience", "work history", "career"),
    "education":      ("education", "academic background", "qualifications", "academics"),
    "skills":         ("skills", "technical skills", "core competencies", "competencies", "key skills"),
    "projects":       ("projects", "personal projects", "selected projects", "portfolio"),
    "certifications": ("certifications", "certificates", "licenses", "courses"),
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
# -- Called by: segment (segmenter.py)
def is_heading(line: str) -> bool:
    stripped = line.strip().rstrip(":")
    if not stripped or len(stripped) > 40:
        return False
    if stripped.isupper():
        return True
    lower = stripped.lower()
    for aliases in SECTION_ALIASES.values():
        if lower in aliases:
            return True
    words = stripped.split()
    if len(words) <= 5 and all(w[:1].isupper() for w in words if w):
        return any(lower.startswith(a.split()[0]) for aliases in SECTION_ALIASES.values() for a in aliases)
    return False
# -------------------- is_heading ------------- END ----------------


# -------------------- label_for_heading ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: segment (segmenter.py)
def label_for_heading(line: str) -> str | None:
    lower = line.strip().rstrip(":").lower()
    for canonical, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            if lower == alias or lower.startswith(alias + " "):
                return canonical
    return None
# -------------------- label_for_heading ------------- END ----------------


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
