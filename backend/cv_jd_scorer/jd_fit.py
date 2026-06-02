from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from cv_jd_scorer.leaves.score_leaves import clamp_100, clamp_unit
from cv_jd_scorer.leaves.text_leaves import extract_top_keywords, remove_stopwords, tokenize
from cv_jd_scorer.models import JdFitGap, JdFitMatch, JdFitSummary


_JD_KEYWORDS_N = 30


# -------------------- _find_evidence_section ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: score
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
def _impact_for_rank(rank: int, total: int) -> str:
    thirds = total / 3
    if rank < thirds:
        return "HIGH"
    if rank < 2 * thirds:
        return "MED"
    return "LOW"
# -------------------- _impact_for_rank ------------- END ----------------


# -------------------- score ----------- START ----------
# -- Calls : extract_top_keywords, tokenize, remove_stopwords,
#            _find_evidence_section, _impact_for_rank,
#            clamp_100, clamp_unit
# -- Called by: scorer.compute
def score(
    cv_raw_text: str,
    jd_text: str,
    sections: dict,
) -> tuple[JdFitSummary, list[JdFitMatch], list[JdFitGap]]:
    # TF-IDF cosine similarity
    cv_clean = " ".join(remove_stopwords(tokenize(cv_raw_text)))
    jd_clean = " ".join(remove_stopwords(tokenize(jd_text)))

    if not jd_clean.strip():
        similarity = 0.0
    else:
        vec = TfidfVectorizer()
        matrix = vec.fit_transform([cv_clean, jd_clean])
        similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

    # Keyword extraction from JD
    jd_keywords = extract_top_keywords(jd_text, n=_JD_KEYWORDS_N)
    cv_text_lower = cv_raw_text.lower()

    matches: list[JdFitMatch] = []
    gaps: list[JdFitGap] = []

    for rank, kw in enumerate(jd_keywords):
        if kw in cv_text_lower:
            section = _find_evidence_section(kw, sections)
            # Strength: top-ranked keywords contribute more; normalise rank to 0.5–1.0
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
    fit_score = clamp_100(similarity * 60 + keyword_density * 0.4)

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
