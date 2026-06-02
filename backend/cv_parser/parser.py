from cv_parser import cleaner, extractors, redflags, segmenter
from cv_parser.models import ParsedCV


# -------------------- parse_cv ----------- START ----------
# -- Calls : extractors.dispatch_by_extension, cleaner.clean_text,
#            segmenter.segment, redflags.build_ats_redflags
# -- Called by: parse_endpoint (interface.py)
def parse_cv(file_bytes: bytes, filename: str) -> ParsedCV:
    raw = extractors.dispatch_by_extension(file_bytes, filename)
    cleaned = cleaner.clean_text(raw)
    sections = segmenter.segment(cleaned)
    flags = redflags.build_ats_redflags(raw, cleaned, sections)
    return ParsedCV(
        raw_text=cleaned.text,
        sections=sections,
        extraction_method=raw.method,
        ats_redflags=flags,
    )
# -------------------- parse_cv ------------- END ----------------
