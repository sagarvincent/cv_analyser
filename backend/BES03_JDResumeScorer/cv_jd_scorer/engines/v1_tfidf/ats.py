from cv_jd_scorer.engines.v1_tfidf.leaves.score_leaves import clamp_100
from cv_jd_scorer.models import AtsCheck, AtsSummary


_CHECKS = [
    {
        "label": "Section headings detected",
        "field": "heading_detection_rate",
        "pass_fn": lambda v: v >= 0.7,
        "weight": 20,
        "pass_note": "Clear section structure helps ATS parse your CV.",
        "fail_note": "Few or no section headings found — ATS may misclassify content.",
    },
    {
        "label": "Low unclassified content",
        "field": "unclassified_ratio",
        "pass_fn": lambda v: v <= 0.25,
        "weight": 15,
        "pass_note": "Most content maps to recognised sections.",
        "fail_note": "High proportion of text outside recognised sections.",
    },
    {
        "label": "Clean character encoding",
        "field": "encoding_anomaly_rate",
        "pass_fn": lambda v: v <= 0.01,
        "weight": 15,
        "pass_note": "No encoding issues detected.",
        "fail_note": "Non-standard characters may be stripped by ATS parsers.",
    },
    {
        "label": "No broken hyphenation",
        "field": "hyphenation_break_rate",
        "pass_fn": lambda v: v <= 0.05,
        "weight": 15,
        "pass_note": "Words appear intact across line breaks.",
        "fail_note": "Hyphenation breaks detected — words may be split mid-token.",
    },
    {
        "label": "Consistent bullet style",
        "field": "distinct_bullet_chars",
        "pass_fn": lambda v: v <= 3,
        "weight": 10,
        "pass_note": "Bullet characters are consistent throughout.",
        "fail_note": "Multiple bullet styles used — can confuse list parsing.",
    },
    {
        "label": "Uniform line lengths",
        "field": "line_length_bimodality",
        "pass_fn": lambda v: v <= 0.6,
        "weight": 10,
        "pass_note": "Line lengths are reasonably uniform.",
        "fail_note": "High variance in line lengths suggests multi-column layout.",
    },
    {
        "label": "Normal reading order",
        "field": "stream_order_anomaly",
        "pass_fn": lambda v: v <= 0.1,
        "weight": 10,
        "pass_note": "Text stream order looks correct.",
        "fail_note": "Unusual character ordering — possible multi-column or table artefact.",
    },
    {
        "label": "Strong section coherence",
        "field": "section_coherence",
        "pass_fn": lambda v: v >= 0.5,
        "weight": 5,
        "pass_note": "Section content matches expected headings.",
        "fail_note": "Section content does not strongly match its heading label.",
    },
]


# -------------------- score ----------- START ----------
# -- Calls : clamp_100
# -- Called by: scorer.compute
def score(ats_redflags: dict) -> tuple[AtsSummary, list[AtsCheck]]:
    checks: list[AtsCheck] = []
    total_weight = 0

    for spec in _CHECKS:
        raw = ats_redflags.get(spec["field"], 0)
        passed = bool(spec["pass_fn"](raw))
        note = spec["pass_note"] if passed else spec["fail_note"]
        checks.append(AtsCheck(label=spec["label"], pass_=passed, note=note))
        if passed:
            total_weight += spec["weight"]

    ats_score = clamp_100(total_weight)
    n_pass = sum(1 for c in checks if c.pass_)
    n_total = len(checks)

    summary = AtsSummary(
        eyebrow="ATS READABILITY",
        titleScore=f"{ats_score}/100",
        titleRest=" — structural scan complete",
        sub=f"{n_pass} of {n_total} checks passed",
        score=ats_score,
    )
    return summary, checks
# -------------------- score ------------- END ----------------
