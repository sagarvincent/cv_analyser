from dataclasses import dataclass

from cv_parser.extractors import RawExtraction
from cv_parser.leaves.cleaning_leaves import normalise_whitespace


@dataclass
class CleanedText:
    text: str
    lines: list[str]


# -------------------- clean_text ----------- START ----------
# -- Calls : normalise_whitespace
# -- Called by: parse_cv (parser.py)
def clean_text(raw: RawExtraction) -> CleanedText:
    normalised = normalise_whitespace(raw.text)
    lines = normalised.split("\n")
    return CleanedText(text=normalised, lines=lines)
# -------------------- clean_text ------------- END ----------------
