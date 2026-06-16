import re

CANONICAL_SECTIONS = (
    "overview",
    "responsibilities",
    "requirements",
    "preferred",
    "skills",
    "about_company",
    "benefits",
    "other",
)

JD_SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "overview": (
        "overview", "about the role", "role overview", "the role",
        "position overview", "job summary", "position summary",
        "role description", "job description", "role summary",
        "about this role", "about the position", "about the job",
    ),
    "responsibilities": (
        "responsibilities", "what you'll do", "key responsibilities",
        "your responsibilities", "role responsibilities", "duties",
        "what you will do", "in this role", "day-to-day", "day to day",
        "you will", "the role involves", "key duties",
        "in this role you can expect to", "in this role, you can expect to",
        "what you'll be doing", "you will be", "you can expect to",
    ),
    "requirements": (
        "requirements", "what we're looking for", "what you'll need",
        "required qualifications", "minimum qualifications", "qualifications",
        "must have", "you should have", "essential", "essential requirements",
        "required skills", "required experience", "what you need",
        "about you", "who you are",
        "you have", "you'll have", "you will have", "what you bring",
        "what you have",
    ),
    "preferred": (
        "preferred qualifications", "nice to have", "nice-to-have",
        "bonus points", "preferred skills", "preferred experience",
        "desirable", "good to have", "what's a plus", "plus",
        "ideally", "advantageous", "preferred requirements",
        "it would be great if", "it would be nice if",
        "even better if you have", "even better if", "bonus if you have",
    ),
    "skills": (
        "skills", "technical skills", "tech stack", "technologies",
        "tools", "technical requirements", "tools and technologies",
        "key skills", "core skills", "skill set",
    ),
    "about_company": (
        "about us", "about the company", "who we are", "the company",
        "company overview", "our company", "about", "our story",
        "the opportunity", "why us",
    ),
    "benefits": (
        "benefits", "what we offer", "perks", "perks and benefits",
        "why join us", "compensation and benefits", "we offer",
        "what you'll get", "what's in it for you", "our offer",
        "salary and benefits", "compensation",
    ),
}


# -------------------- is_heading ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: group_lines_by_heading
def is_heading(line: str, alias_map: dict[str, tuple[str, ...]] = JD_SECTION_ALIASES) -> bool:
    stripped = line.strip().rstrip(":")
    if not stripped or len(stripped) > 60:
        return False
    if stripped.isupper() and len(stripped) <= 40:
        return True
    lower = stripped.lower()
    for aliases in alias_map.values():
        if lower in aliases:
            return True
    words = stripped.split()
    if len(words) <= 6 and all(w[:1].isupper() for w in words if w):
        return any(lower.startswith(a.split()[0]) for aliases in alias_map.values() for a in aliases)
    return False
# -------------------- is_heading ------------- END ----------------


# -------------------- label_for_heading ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: group_lines_by_heading
def label_for_heading(line: str, alias_map: dict[str, tuple[str, ...]] = JD_SECTION_ALIASES) -> str | None:
    lower = line.strip().rstrip(":").lower()
    for canonical, aliases in alias_map.items():
        for alias in aliases:
            if lower == alias or lower.startswith(alias + " "):
                return canonical
    return None
# -------------------- label_for_heading ------------- END ----------------


# -------------------- group_lines_by_heading ----------- START ----------
# -- Calls : is_heading, label_for_heading
# -- Called by: segment (segmenter.py)
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


# -------------------- first_heading_index ----------- START ----------
# -- Calls : is_heading
# -- Called by: extractor.py (to find header block boundary)
def first_heading_index(
    lines: list[str],
    alias_map: dict[str, tuple[str, ...]] = JD_SECTION_ALIASES,
) -> int:
    """Return the index of the first line recognised as a section heading.
    Returns len(lines) if no heading is found (entire text is header block)."""
    for i, line in enumerate(lines):
        if is_heading(line, alias_map):
            label = label_for_heading(line, alias_map)
            if label is not None:
                return i
    return len(lines)
# -------------------- first_heading_index ------------- END ----------------


# -------------------- split_bullets ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: segmenter.py
_BULLET_RE = re.compile(r"^[\s•●◦▪▫◆◇■□○\-*–—»›]+")

def split_bullets(text: str) -> list[str]:
    """Split section text into individual bullet / line items.
    No word-count cap — JD responsibilities are full sentences.
    A single very long line (newline-sparse JD) is sentence-split so the
    section yields several items instead of one giant blob."""
    items = []
    for line in text.splitlines():
        cleaned = _BULLET_RE.sub("", line).strip()
        if not cleaned:
            continue
        if len(cleaned) > 300:
            items.extend(_sentence_split(cleaned))
        else:
            items.append(cleaned)
    return items
# -------------------- split_bullets ------------- END ----------------


# -------------------- _sentence_split ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: split_bullets
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")

def _sentence_split(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_RE.split(text) if s.strip()]
# -------------------- _sentence_split ------------- END ----------------


# -------------------- reflow_inline_headings ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: parser._clean
# Header labels that appear inline in scraped JDs ("Title: ... Location: ...").
_INLINE_LABELS = (
    "title", "location", "grade", "salary", "department",
    "employment type", "job type", "reports to",
)

# Colon-terminated section headings, e.g. "Responsibilities:" mid-stream.
_ALIAS_COLON_RE = re.compile(
    r"\s*\b(" + "|".join(
        re.escape(a) for a in sorted(
            {a for aliases in JD_SECTION_ALIASES.values() for a in aliases},
            key=len, reverse=True,
        )
    ) + r")\s*:",
    re.IGNORECASE,
)
_LABEL_COLON_RE = re.compile(
    r"\s+\b(" + "|".join(re.escape(label) for label in _INLINE_LABELS) + r")\s*:",
    re.IGNORECASE,
)
# An ALL-CAPS cue run of 2+ words emerging from normal-case text, isolated
# onto its own line so it can act as a heading boundary, e.g.
# "...peers. YOU ARE Passionate..." -> "...peers.\nYOU ARE\nPassionate...".
_ALLCAPS_RUN_RE = re.compile(
    r"(?<=[a-z0-9.,:)])\s+"
    r"(?P<run>(?:[A-Z][A-Z0-9&]+[ ,]+){1,7}[A-Z][A-Z0-9&]+)"
    r"(?=\s)"
)

# Title-Case heading phrases that appear without a colon, e.g.
# "...firm. Requirements What you'll bring..." or "Minimum Qualifications 5+ years".
# Two precision guards (applied in _wrap_nocolon): the phrase must be followed by
# a capital letter or digit (prose continues lowercase), and the matched text must
# not start lowercase (a lowercase mention is prose, not a heading).
# Weak single words that read as ordinary Title-Case prose are excluded.
_NOCOLON_DENYLIST = {
    "plus", "essential", "ideally", "advantageous", "desirable",
    "good to have", "about", "day-to-day", "day to day",
}
_NOCOLON_RE = re.compile(
    r"\b(" + "|".join(
        re.escape(a) for a in sorted(
            {a for aliases in JD_SECTION_ALIASES.values() for a in aliases}
            - _NOCOLON_DENYLIST,
            key=len, reverse=True,
        )
    ) + r")\b(?=\s+[A-Z0-9])",
    re.IGNORECASE,
)


def _wrap_nocolon(m: "re.Match") -> str:
    text = m.group(1)
    if text[:1].islower():  # lowercase mention -> prose, not a heading
        return m.group(0)
    return "\n" + text + "\n"


def reflow_inline_headings(text: str) -> str:
    """Re-insert line breaks before inline headings in newline-sparse JD text.

    Only activates on single-line / newline-starved input; well-formatted
    multi-line JDs are returned unchanged so the normal path never regresses."""
    if text.count("\n") > 2 or len(text) <= 400:
        return text
    text = _ALIAS_COLON_RE.sub(lambda m: "\n" + m.group(1) + ":", text)
    text = _LABEL_COLON_RE.sub(lambda m: "\n" + m.group(1) + ":", text)
    text = _ALLCAPS_RUN_RE.sub(lambda m: "\n" + m.group("run") + "\n", text)
    text = _NOCOLON_RE.sub(_wrap_nocolon, text)
    return text
# -------------------- reflow_inline_headings ------------- END ----------------
