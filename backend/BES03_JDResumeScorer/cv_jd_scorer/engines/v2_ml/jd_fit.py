from cv_jd_scorer.common import embedder
from cv_jd_scorer.common.text import extract_top_keywords
from cv_jd_scorer.engines.v1_tfidf.leaves.score_leaves import clamp_100, clamp_unit
from cv_jd_scorer.models import JdFitGap, JdFitMatch, JdFitSummary


_JD_KEYWORDS_N = 30

# Final fit blend: semantic similarity dominates, keyword density fills in.
# Slope and keyword weight were calibrated against eval_data/labelled/pairs.jsonl
# (cv_jd_scorer.eval.bench): a gentler semantic slope compresses the high-cosine
# overshoot on genuine mismatches — MiniLM's cosine floor (~0.3 for any two
# English texts) means low-match pairs still score non-trivially, so an
# aggressive slope over-scores them. 70 / 0.20 minimises total MAE while keeping
# the low_match bucket close to the TF-IDF baseline.
_W_SEMANTIC = 70.0   # applied to raw cosine sim in [0, 1]
_W_KEYWORD  = 0.20   # applied to keyword density in [0, 100]


# -------------------- _find_evidence_section ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: score
# -- Copied from v1_tfidf.jd_fit to keep engines decoupled.
def _find_evidence_section(keyword: str, sections: dict) -> str:
    for name in ("experience", "skills", "summary", "projects", "certifications"):
        section = sections.get(name)
        if not section:
            continue
        text = ""
        if isinstance(section, str):
            text = section
        elif isinstance(section, list):
            text = " ".join(
                str(item) if isinstance(item, str)
                else " ".join(str(v) for v in item.values())
                for item in section
            )
        elif isinstance(section, dict):
            text = section.get("text", "") + " ".join(section.get("items", []))
        if keyword in text.lower():
            return name.capitalize()
    return "CV"
# -------------------- _find_evidence_section ------------- END ----------------


# -------------------- _impact_for_rank ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: score
# -- Copied from v1_tfidf.jd_fit to keep engines decoupled.
def _impact_for_rank(rank: int, total: int) -> str:
    thirds = total / 3
    if rank < thirds:
        return "HIGH"
    if rank < 2 * thirds:
        return "MED"
    return "LOW"
# -------------------- _impact_for_rank ------------- END ----------------


# -------------------- score ----------- START ----------
# -- Calls : embedder.build_cv_text, embedder.embed, embedder.cosine_sim,
#            extract_top_keywords, _find_evidence_section, _impact_for_rank,
#            clamp_100, clamp_unit
# -- Called by: scorer.compute
def score(
    parsed_cv: dict,
    jd_text: str,
    sections: dict,
) -> tuple[JdFitSummary, list[JdFitMatch], list[JdFitGap]]:
    # Semantic cosine similarity via sentence embeddings
    cv_text = embedder.build_cv_text(parsed_cv)
    if not jd_text.strip() or not cv_text.strip():
        semantic_sim = 0.0
    else:
        cv_vec = embedder.embed(cv_text)
        jd_vec = embedder.embed(jd_text)
        # Cosine of unit vectors is in [-1, 1]; clamp negatives to 0.
        semantic_sim = max(0.0, embedder.cosine_sim(cv_vec, jd_vec))

    # Keyword match / gap analysis (kept for ATS explainability — same as v1)
    jd_keywords    = extract_top_keywords(jd_text, n=_JD_KEYWORDS_N)
    cv_text_lower  = cv_text.lower()
    raw_text_lower = parsed_cv.get("raw_text", "").lower()

    matches: list[JdFitMatch] = []
    gaps:    list[JdFitGap]   = []

    for rank, kw in enumerate(jd_keywords):
        if kw in cv_text_lower or kw in raw_text_lower:
            section  = _find_evidence_section(kw, sections)
            strength = clamp_unit(1.0 - (rank / (_JD_KEYWORDS_N * 2)))
            matches.append(JdFitMatch(topic=kw, evidence=f"Found in {section}", strength=round(strength, 2)))
        else:
            impact = _impact_for_rank(rank, len(jd_keywords))
            gaps.append(JdFitGap(
                topic=kw,
                impact=impact,
                note=f"'{kw}' appears in the JD but not in your CV.",
            ))

    keyword_density = (len(matches) / len(jd_keywords) * 100) if jd_keywords else 0.0
    fit_score = clamp_100(semantic_sim * _W_SEMANTIC + keyword_density * _W_KEYWORD)

    # Gap breakdown string  e.g. "2 high · 3 med · 1 low"
    high = sum(1 for g in gaps if g.impact == "HIGH")
    med  = sum(1 for g in gaps if g.impact == "MED")
    low  = sum(1 for g in gaps if g.impact == "LOW")
    gap_breakdown = f"{high} high · {med} med · {low} low"

    summary = JdFitSummary(
        eyebrow="JD FIT",
        titleReach=f"{fit_score}/100",
        titleRest=" match score",
        sub=f"{len(matches)} keyword matches · {len(gaps)} gaps",
        score=fit_score,
        evidencedMatches=len(matches),
        totalRequirements=len(jd_keywords),
        gapsFlagged=len(gaps),
        gapBreakdown=gap_breakdown,
        keywordDensity=clamp_100(keyword_density),
    )
    return summary, matches, gaps
# -------------------- score ------------- END ----------------
