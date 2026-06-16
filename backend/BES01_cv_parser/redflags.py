from BES01_cv_parser.cleaner import CleanedText
from BES01_cv_parser.extractors import RawExtraction
from BES01_cv_parser.leaves.cleaning_leaves import (
    distinct_bullet_chars,
    hyphenation_break_rate,
    line_length_bimodality,
)
from BES01_cv_parser.leaves.extraction_leaves import (
    encoding_anomaly_rate,
    stream_order_anomaly,
    text_density,
)
from BES01_cv_parser.leaves.segmentation_leaves import (
    CANONICAL_SECTIONS,
    STRICT_SECTION_ALIASES_V1,
    count_date_ranges,
    group_lines_by_heading,
    section_coherence_score,
)
from BES01_cv_parser.models import AtsRedFlags, Sections


_EXPECTED_HEADINGS = 7

# content sections compared between strict and fuzzy passes ('other' excluded)
_CONTENT_SECTIONS = ("summary", "experience", "education", "skills", "projects", "certifications")


# -------------------- _heading_detection_rate ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags
def _heading_detection_rate(strict_buckets: dict[str, str]) -> float:
    # ATS signal: pinned to the frozen strict alias list (v1). Must NOT
    # improve when the fuzzy extraction pass gains new aliases.
    found = sum(1 for name in CANONICAL_SECTIONS if strict_buckets[name])
    return found / _EXPECTED_HEADINGS
# -------------------- _heading_detection_rate ------------- END ----------------


# -------------------- _sections_recovered_by_fuzzy_only ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags
def _sections_recovered_by_fuzzy_only(strict_buckets: dict[str, str], sections: Sections) -> int:
    fuzzy_found = {
        "summary":        bool(sections.summary),
        "experience":     bool(sections.experience),
        "education":      bool(sections.education),
        "skills":         bool(sections.skills.text),
        "projects":       bool(sections.projects),
        "certifications": bool(sections.certifications),
    }
    return sum(
        1 for name in _CONTENT_SECTIONS
        if fuzzy_found[name] and not strict_buckets[name]
    )
# -------------------- _sections_recovered_by_fuzzy_only ------------- END ----------------


# -------------------- _experience_boundary_failures ----------- START ----------
# -- Calls : count_date_ranges
# -- Called by: build_ats_redflags
def _experience_boundary_failures(sections: Sections) -> int:
    return sum(1 for e in sections.experience if count_date_ranges(e.description) >= 2)
# -------------------- _experience_boundary_failures ------------- END ----------------


# -------------------- _section_coherence ----------- START ----------
# -- Calls : section_coherence_score
# -- Called by: build_ats_redflags
def _section_coherence(sections: Sections) -> float:
    samples = (
        ("summary",        sections.summary),
        ("experience",     "\n".join(e.description for e in sections.experience)),
        ("education",      "\n".join(f"{e.degree or ''} {e.institution or ''}" for e in sections.education)),
        ("skills",         sections.skills.text),
        ("projects",       sections.projects),
        ("certifications", "\n".join(sections.certifications)),
    )
    scored = [section_coherence_score(name, content) for name, content in samples if content]
    return sum(scored) / len(scored) if scored else 0.0
# -------------------- _section_coherence ------------- END ----------------


# -------------------- _unclassified_ratio ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags
def _unclassified_ratio(sections: Sections, raw_text: str) -> float:
    if not raw_text:
        return 0.0
    return len(sections.other) / len(raw_text)
# -------------------- _unclassified_ratio ------------- END ----------------


# -------------------- _non_whitespace_count ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags
def _non_whitespace_count(text: str) -> int:
    return sum(1 for c in text if not c.isspace())
# -------------------- _non_whitespace_count ------------- END ----------------


# -------------------- build_ats_redflags ----------- START ----------
# -- Calls : stream_order_anomaly, text_density, encoding_anomaly_rate,
#            distinct_bullet_chars, line_length_bimodality, hyphenation_break_rate,
#            group_lines_by_heading, _heading_detection_rate,
#            _sections_recovered_by_fuzzy_only, _experience_boundary_failures,
#            _section_coherence, _unclassified_ratio, _non_whitespace_count
# -- Called by: parse_cv (parser.py)
def build_ats_redflags(
    raw: RawExtraction,
    cleaned: CleanedText,
    sections: Sections,
) -> AtsRedFlags:
    nwc = _non_whitespace_count(cleaned.text)
    strict_buckets = group_lines_by_heading(cleaned.lines, STRICT_SECTION_ALIASES_V1)
    return AtsRedFlags(
        stream_order_anomaly=stream_order_anomaly(raw.chars),
        text_density=text_density(nwc, raw.total_page_area),
        # measured on raw (pre-clean) text: an ATS signal about the document
        # itself, independent of parser-side encoding repair
        encoding_anomaly_rate=encoding_anomaly_rate(raw.text),
        extraction_method=raw.method,
        distinct_bullet_chars=distinct_bullet_chars(cleaned.text),
        line_length_bimodality=line_length_bimodality(cleaned.lines),
        hyphenation_break_rate=hyphenation_break_rate(cleaned.lines),
        heading_detection_rate=_heading_detection_rate(strict_buckets),
        section_coherence=_section_coherence(sections),
        unclassified_ratio=_unclassified_ratio(sections, cleaned.text),
        sections_recovered_by_fuzzy_only=_sections_recovered_by_fuzzy_only(strict_buckets, sections),
        experience_boundary_failures=_experience_boundary_failures(sections),
    )
# -------------------- build_ats_redflags ------------- END ----------------
