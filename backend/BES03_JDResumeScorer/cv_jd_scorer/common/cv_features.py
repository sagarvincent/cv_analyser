import re
from datetime import date

from BES01_cv_parser.leaves.segmentation_leaves import find_date_range


_SENIORITY_PATTERNS = [
    (r"\bc[\-\s]?level\b|chief\b|cto\b|cpo\b|coo\b|ceo\b", "c-level"),
    (r"\bvice\s+president\b|\bvp\b", "vp"),
    (r"\bdirector\b", "director"),
    (r"\bprincipal\b", "principal"),
    (r"\blead\b|\bstaff\b", "lead"),
    (r"\bmanager\b", "manager"),
    (r"\bsenior\b|\bsr\b", "senior"),
    (r"\bassociate\b|\bjunior\b|\bjr\b", "junior"),
    (r"\bintern\b|\btrainee\b", "intern"),
]


# -------------------- _parse_year ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: calc_exp_years
def _parse_year(token: str) -> int | None:
    m = re.search(r"\d{4}", token)
    return int(m.group()) if m else None
# -------------------- _parse_year ------------- END ----------------


# -------------------- calc_exp_years ----------- START ----------
# -- Calls : find_date_range, _parse_year
# -- Called by: engines that need experience duration
def calc_exp_years(experience_list: list[dict]) -> float:
    current_year = date.today().year
    total_months = 0.0
    for entry in experience_list:
        text = (entry.get("dates") or "") + " " + (entry.get("description") or "")
        date_str = find_date_range(text.strip())
        if not date_str:
            continue
        parts = re.split(r"\s*(?:-|–|—|to)\s*", date_str, maxsplit=1)
        if len(parts) != 2:
            continue
        start_year = _parse_year(parts[0])
        end_raw = parts[1].strip().lower()
        if re.match(r"present|current", end_raw):
            end_year = current_year
        else:
            end_year = _parse_year(parts[1])
        if start_year and end_year and end_year >= start_year:
            total_months += (end_year - start_year) * 12
    return round(total_months / 12, 1)
# -------------------- calc_exp_years ------------- END ----------------


# -------------------- detect_seniority ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: engines that need seniority classification
def detect_seniority(text: str) -> str:
    lower = text.lower()
    for pattern, label in _SENIORITY_PATTERNS:
        if re.search(pattern, lower):
            return label
    return "mid"
# -------------------- detect_seniority ------------- END ----------------


# -------------------- extract_skill_tokens ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: engines that need skill token extraction
def extract_skill_tokens(sections: dict) -> list[str]:
    tokens: list[str] = []
    skills_block = sections.get("skills", {})
    if isinstance(skills_block, dict):
        tokens.extend(item.lower() for item in skills_block.get("items", []))
    for exp in sections.get("experience", []):
        desc = exp.get("description", "")
        tokens.extend(desc.lower().split()[:50])
    return tokens
# -------------------- extract_skill_tokens ------------- END ----------------
