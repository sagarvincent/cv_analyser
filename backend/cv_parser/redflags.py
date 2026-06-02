from cv_parser.cleaner import CleanedText
from cv_parser.extractors import RawExtraction
from cv_parser.leaves.cleaning_leaves import (
    distinct_bullet_chars,
    hyphenation_break_rate,
    line_length_bimodality,
)
from cv_parser.leaves.extraction_leaves import (
    encoding_anomaly_rate,
    stream_order_anomaly,
    text_density,
)
from cv_parser.leaves.segmentation_leaves import (
    CANONICAL_SECTIONS,
    section_coherence_score,
)
from cv_parser.models import AtsRedFlags, Sections


_EXPECTED_HEADINGS = 7


# -------------------- _heading_detection_rate ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags
def _heading_detection_rate(sections: Sections) -> float:
    found = 0
    if sections.summary:        found += 1
    if sections.experience:     found += 1
    if sections.education:      found += 1
    if sections.skills.text:    found += 1
    if sections.projects:       found += 1
    if sections.certifications: found += 1
    if sections.other:          found += 1
    return found / _EXPECTED_HEADINGS
# -------------------- _heading_detection_rate ------------- END ----------------


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
#            _heading_detection_rate, _section_coherence, _unclassified_ratio,
#            _non_whitespace_count
# -- Called by: parse_cv (parser.py)
def build_ats_redflags(
    raw: RawExtraction,
    cleaned: CleanedText,
    sections: Sections,
) -> AtsRedFlags:
    nwc = _non_whitespace_count(cleaned.text)
    return AtsRedFlags(
        stream_order_anomaly=stream_order_anomaly(raw.chars),
        text_density=text_density(nwc, raw.total_page_area),
        encoding_anomaly_rate=encoding_anomaly_rate(cleaned.text),
        extraction_method=raw.method,
        distinct_bullet_chars=distinct_bullet_chars(cleaned.text),
        line_length_bimodality=line_length_bimodality(cleaned.lines),
        hyphenation_break_rate=hyphenation_break_rate(cleaned.lines),
        heading_detection_rate=_heading_detection_rate(sections),
        section_coherence=_section_coherence(sections),
        unclassified_ratio=_unclassified_ratio(sections, cleaned.text),
    )
# -------------------- build_ats_redflags ------------- END ----------------
