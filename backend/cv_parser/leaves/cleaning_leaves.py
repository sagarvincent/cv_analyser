import re


BULLET_CHARS = "•●◦▪▫◆◇■□○-*–—»›"


# -------------------- normalise_whitespace ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: clean_text (cleaner.py)
def normalise_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
# -------------------- normalise_whitespace ------------- END ----------------


# -------------------- distinct_bullet_chars ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def distinct_bullet_chars(text: str) -> int:
    return len({c for c in text if c in BULLET_CHARS})
# -------------------- distinct_bullet_chars ------------- END ----------------


# -------------------- line_length_bimodality ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def line_length_bimodality(lines: list[str]) -> float:
    lengths = [len(ln) for ln in lines if ln.strip()]
    if len(lengths) < 4:
        return 0.0
    lengths_sorted = sorted(lengths)
    mid = len(lengths_sorted) // 2
    lower = lengths_sorted[:mid]
    upper = lengths_sorted[mid:]
    mean_lower = sum(lower) / len(lower)
    mean_upper = sum(upper) / len(upper)
    inter_gap = abs(mean_upper - mean_lower)
    spread_lower = (max(lower) - min(lower)) or 1
    spread_upper = (max(upper) - min(upper)) or 1
    intra_spread = (spread_lower + spread_upper) / 2
    score = inter_gap / (inter_gap + intra_spread)
    return min(max(score, 0.0), 1.0)
# -------------------- line_length_bimodality ------------- END ----------------


# -------------------- hyphenation_break_rate ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def hyphenation_break_rate(lines: list[str]) -> float:
    non_empty = [ln for ln in lines if ln.strip()]
    if len(non_empty) < 2:
        return 0.0
    breaks = 0
    for prev, curr in zip(non_empty, non_empty[1:]):
        if prev.rstrip().endswith("-") and curr.lstrip()[:1].islower():
            breaks += 1
    return breaks / len(non_empty)
# -------------------- hyphenation_break_rate ------------- END ----------------
