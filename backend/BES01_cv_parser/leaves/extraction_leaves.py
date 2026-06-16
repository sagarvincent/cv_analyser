import re


_ALLOWED_CHAR_RE = re.compile(r"[A-Za-z0-9\s\.\,\;\:\!\?\(\)\[\]\{\}\-\_\'\"\/\\@#\$%&\*\+=<>\|~`\^]")
_MOJIBAKE_RE = re.compile(r"[�ÂÃ]")


# -------------------- stream_order_anomaly ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def stream_order_anomaly(chars: list[dict]) -> float:
    if len(chars) < 2:
        return 0.0
    backwards = 0
    pairs = 0
    for prev, curr in zip(chars, chars[1:]):
        if prev.get("page_number") != curr.get("page_number"):
            continue
        pairs += 1
        same_line = abs(curr["top"] - prev["top"]) < 2.0
        if same_line:
            if curr["x0"] < prev["x0"]:
                backwards += 1
        else:
            if curr["top"] < prev["top"]:
                backwards += 1
    return backwards / pairs if pairs else 0.0
# -------------------- stream_order_anomaly ------------- END ----------------


# -------------------- text_density ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def text_density(non_whitespace_char_count: int, total_page_area: float) -> float:
    if total_page_area <= 0:
        return 0.0
    return non_whitespace_char_count / total_page_area
# -------------------- text_density ------------- END ----------------


# -------------------- encoding_anomaly_rate ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_ats_redflags (redflags.py)
def encoding_anomaly_rate(text: str) -> float:
    if not text:
        return 0.0
    weighted_anomalies = 0.0
    for ch in text:
        if _MOJIBAKE_RE.match(ch):
            weighted_anomalies += 2.0
        elif not _ALLOWED_CHAR_RE.match(ch):
            weighted_anomalies += 1.0
    return weighted_anomalies / len(text)
# -------------------- encoding_anomaly_rate ------------- END ----------------


# -------------------- page_area ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: extract_pdf (extractors.py)
def page_area(width: float, height: float) -> float:
    return max(width, 0.0) * max(height, 0.0)
# -------------------- page_area ------------- END ----------------
