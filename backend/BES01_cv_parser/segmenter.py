import re

from BES01_cv_parser.cleaner import CleanedText
from BES01_cv_parser.leaves.segmentation_leaves import (
    FUZZY_SECTION_ALIASES,
    find_date_range,
    find_year,
    group_lines_by_heading,
    label_for_heading,
    split_blocks_by_anchor,
    strip_date_substrings,
    strip_year_substrings,
)
from BES01_cv_parser.models import (
    EducationEntry,
    ExperienceEntry,
    Sections,
    SkillsBlock,
)


# -------------------- _extract_headline ----------- START ----------
# -- Calls : label_for_heading, find_date_range
# -- Called by: segment
def _extract_headline(lines: list[str]) -> tuple[str, list[str]]:
    """The top-of-CV job-title banner: first non-empty line, all-caps,
    no date, not a recognised section header. Routed to `headline`
    deliberately rather than leaking into `other`."""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if (
            stripped.isupper()
            and len(stripped) <= 60
            and find_date_range(stripped) is None
            and label_for_heading(stripped, FUZZY_SECTION_ALIASES) is None
        ):
            return stripped, lines[:i] + lines[i + 1:]
        return "", lines
    return "", lines
# -------------------- _extract_headline ------------- END ----------------


# -------------------- _parse_experience_entry ----------- START ----------
# -- Calls : find_date_range, strip_date_substrings
# -- Called by: _split_experience
def _parse_experience_entry(block: str) -> ExperienceEntry:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    dates = find_date_range(block)
    title = strip_date_substrings(lines[0]) if lines else ""
    org = strip_date_substrings(lines[1]) if len(lines) > 1 else ""
    return ExperienceEntry(
        title=title or None,
        org=org or None,
        dates=dates,
        description=block,
    )
# -------------------- _parse_experience_entry ------------- END ----------------


# -------------------- _split_experience ----------- START ----------
# -- Calls : split_blocks_by_anchor, find_date_range, _parse_experience_entry
# -- Called by: segment
def _split_experience(text: str) -> tuple[list[ExperienceEntry], str]:
    """Date-anchored splitting: each line containing a date range starts a
    new entry. Content before the first anchor is returned as preamble for
    routing to `other` — never an entry's title. Falls back to a single
    entry when the section contains no date anchors at all."""
    if not text:
        return [], ""
    preamble, blocks = split_blocks_by_anchor(
        text,
        lambda ln: find_date_range(ln) is not None,
        anchor_remainder=strip_date_substrings,
    )
    if not blocks:
        return [_parse_experience_entry(text)], ""
    return [_parse_experience_entry(b) for b in blocks], preamble
# -------------------- _split_experience ------------- END ----------------


# -------------------- _parse_education_entry ----------- START ----------
# -- Calls : find_date_range, find_year, strip_date_substrings
# -- Called by: _split_education
def _parse_education_entry(block: str) -> EducationEntry:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    # standalone-year fallback when no full range present (start == end)
    dates = find_date_range(block) or find_year(block)
    degree = strip_year_substrings(strip_date_substrings(lines[0])) if lines else ""
    institution = strip_year_substrings(strip_date_substrings(lines[1])) if len(lines) > 1 else ""
    return EducationEntry(
        degree=degree or None,
        institution=institution or None,
        dates=dates,
    )
# -------------------- _parse_education_entry ------------- END ----------------


# -------------------- _split_education ----------- START ----------
# -- Calls : split_blocks_by_anchor, find_date_range, find_year, _parse_education_entry
# -- Called by: segment
def _split_education(text: str) -> tuple[list[EducationEntry], str]:
    if not text:
        return [], ""
    preamble, blocks = split_blocks_by_anchor(
        text,
        lambda ln: find_date_range(ln) is not None or find_year(ln) is not None,
        anchor_remainder=lambda ln: strip_year_substrings(strip_date_substrings(ln)),
    )
    if not blocks:
        return [_parse_education_entry(text)], ""
    return [_parse_education_entry(b) for b in blocks], preamble
# -------------------- _split_education ------------- END ----------------


_MAX_SKILL_WORDS = 4   # ≥5 words = sentence fragment, not a skill
_MAX_SKILL_CHARS = 60  # whole item kept or dropped — never truncated


# -------------------- _build_skills_block ----------- START ----------
# -- Calls : nothing (leaf-ish)
# -- Called by: segment
def _build_skills_block(text: str) -> SkillsBlock:
    items: list[str] = []
    for chunk in re.split(r"[,\n•●◦▪◆·\-\*\|;]+", text):
        token = chunk.strip(" .:•●◦▪▫◆◇■□○·–—»›")
        if not token:
            continue
        if len(token) > _MAX_SKILL_CHARS or len(token.split()) > _MAX_SKILL_WORDS:
            continue
        items.append(token)
    return SkillsBlock(text=text, items=items)
# -------------------- _build_skills_block ------------- END ----------------


# -------------------- _split_certifications ----------- START ----------
# -- Calls : nothing (leaf-ish)
# -- Called by: segment
def _split_certifications(text: str) -> list[str]:
    out: list[str] = []
    for ln in text.splitlines():
        token = ln.strip(" •●◦▪◆-*").strip()
        if token:
            out.append(token)
    return out
# -------------------- _split_certifications ------------- END ----------------


# -------------------- segment ----------- START ----------
# -- Calls : _extract_headline, group_lines_by_heading, _split_experience,
#            _split_education, _build_skills_block, _split_certifications
# -- Called by: parse_cv (parser.py)
def segment(cleaned: CleanedText) -> Sections:
    headline, lines = _extract_headline(cleaned.lines)
    buckets = group_lines_by_heading(lines, FUZZY_SECTION_ALIASES)
    experience, exp_preamble = _split_experience(buckets["experience"])
    education, edu_preamble = _split_education(buckets["education"])
    other = "\n".join(p for p in (buckets["other"], exp_preamble, edu_preamble) if p)
    return Sections(
        headline=headline,
        summary=buckets["summary"],
        experience=experience,
        education=education,
        skills=_build_skills_block(buckets["skills"]),
        projects=buckets["projects"],
        certifications=_split_certifications(buckets["certifications"]),
        other=other,
    )
# -------------------- segment ------------- END ----------------
