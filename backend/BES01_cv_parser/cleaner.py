from dataclasses import dataclass

from BES01_cv_parser.extractors import RawExtraction
from BES01_cv_parser.leaves.cleaning_leaves import fix_encoding, normalise_whitespace


@dataclass
class CleanedText:
    text: str
    lines: list[str]


# -------------------- clean_text ----------- START ----------
# -- Calls : fix_encoding, normalise_whitespace
# -- Called by: parse_cv (parser.py)
def clean_text(raw: RawExtraction) -> CleanedText:
    normalised = normalise_whitespace(fix_encoding(raw.text))
    lines = normalised.split("\n")
    return CleanedText(text=normalised, lines=lines)
# -------------------- clean_text ------------- END ----------------
