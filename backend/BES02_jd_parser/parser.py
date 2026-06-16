from dataclasses import dataclass

from BES01_cv_parser.leaves.cleaning_leaves import fix_encoding, normalise_whitespace
from BES02_jd_parser import JD_PARSER_VERSION
from BES02_jd_parser.extractor import extract_header
from BES02_jd_parser.leaves.segmentation_leaves import reflow_inline_headings
from BES02_jd_parser.models import ParsedJD
from BES02_jd_parser.segmenter import build_bullets, collect_warnings, segment


@dataclass
class _CleanedText:
    text: str
    lines: list[str]


def _clean(raw: str) -> _CleanedText:
    normalised = normalise_whitespace(fix_encoding(raw))
    normalised = reflow_inline_headings(normalised)
    return _CleanedText(text=normalised, lines=normalised.split("\n"))


# -------------------- parse_jd ----------- START ----------
# -- Calls : _clean, extract_header, segment, build_bullets, collect_warnings
# -- Called by: interface.parse_jd_endpoint
def parse_jd(jd_text: str) -> ParsedJD:
    """Full JD parsing pipeline.

    Accepts raw text (already extracted from a file or pasted directly).
    Returns a structured ParsedJD."""
    cleaned = _clean(jd_text)

    header = extract_header(cleaned.lines, cleaned.text)
    sections = segment(cleaned.lines)
    bullets = build_bullets(sections)
    warnings = collect_warnings(sections, bullets)

    return ParsedJD(
        title=header["title"],
        company=header["company"],
        location=header["location"],
        employment_type=header["employment_type"],
        seniority=header["seniority"],
        salary_range=header["salary_range"],
        sections=sections,
        responsibilities=bullets["responsibilities"],
        required_qualifications=bullets["required_qualifications"],
        preferred_qualifications=bullets["preferred_qualifications"],
        required_skills=bullets["required_skills"],
        benefits=bullets["benefits"],
        raw_text=cleaned.text,
        parse_warnings=warnings,
        parser_version=JD_PARSER_VERSION,
    )
# -------------------- parse_jd ------------- END ----------------
