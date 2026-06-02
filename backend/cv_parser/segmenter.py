import re

from cv_parser.cleaner import CleanedText
from cv_parser.leaves.segmentation_leaves import (
    CANONICAL_SECTIONS,
    find_date_range,
    is_heading,
    label_for_heading,
    split_blocks_by_blank_line,
)
from cv_parser.models import (
    EducationEntry,
    ExperienceEntry,
    Sections,
    SkillsBlock,
)


# -------------------- _group_by_heading ----------- START ----------
# -- Calls : is_heading, label_for_heading
# -- Called by: segment
def _group_by_heading(lines: list[str]) -> dict[str, str]:
    buckets: dict[str, list[str]] = {name: [] for name in CANONICAL_SECTIONS}
    current = "other"
    for line in lines:
        if is_heading(line):
            label = label_for_heading(line)
            if label is not None:
                current = label
                continue
        buckets[current].append(line)
    return {k: "\n".join(v).strip() for k, v in buckets.items()}
# -------------------- _group_by_heading ------------- END ----------------


# -------------------- _parse_experience_entry ----------- START ----------
# -- Calls : find_date_range
# -- Called by: _split_experience
def _parse_experience_entry(block: str) -> ExperienceEntry:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    dates = find_date_range(block)
    title = lines[0] if lines else None
    org = lines[1] if len(lines) > 1 else None
    return ExperienceEntry(title=title, org=org, dates=dates, description=block)
# -------------------- _parse_experience_entry ------------- END ----------------


# -------------------- _split_experience ----------- START ----------
# -- Calls : split_blocks_by_blank_line, _parse_experience_entry
# -- Called by: segment
def _split_experience(text: str) -> list[ExperienceEntry]:
    return [_parse_experience_entry(b) for b in split_blocks_by_blank_line(text)]
# -------------------- _split_experience ------------- END ----------------


# -------------------- _parse_education_entry ----------- START ----------
# -- Calls : find_date_range
# -- Called by: _split_education
def _parse_education_entry(block: str) -> EducationEntry:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    dates = find_date_range(block)
    degree = lines[0] if lines else None
    institution = lines[1] if len(lines) > 1 else None
    return EducationEntry(degree=degree, institution=institution, dates=dates)
# -------------------- _parse_education_entry ------------- END ----------------


# -------------------- _split_education ----------- START ----------
# -- Calls : split_blocks_by_blank_line, _parse_education_entry
# -- Called by: segment
def _split_education(text: str) -> list[EducationEntry]:
    return [_parse_education_entry(b) for b in split_blocks_by_blank_line(text)]
# -------------------- _split_education ------------- END ----------------


# -------------------- _build_skills_block ----------- START ----------
# -- Calls : nothing (leaf-ish)
# -- Called by: segment
def _build_skills_block(text: str) -> SkillsBlock:
    items: list[str] = []
    for chunk in re.split(r"[,\n•●◦▪◆\-\*\|;]+", text):
        token = chunk.strip(" .:")
        if token and len(token) <= 60:
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
# -- Calls : _group_by_heading, _split_experience, _split_education,
#            _build_skills_block, _split_certifications
# -- Called by: parse_cv (parser.py)
def segment(cleaned: CleanedText) -> Sections:
    buckets = _group_by_heading(cleaned.lines)
    return Sections(
        summary=buckets["summary"],
        experience=_split_experience(buckets["experience"]),
        education=_split_education(buckets["education"]),
        skills=_build_skills_block(buckets["skills"]),
        projects=buckets["projects"],
        certifications=_split_certifications(buckets["certifications"]),
        other=buckets["other"],
    )
# -------------------- segment ------------- END ----------------
