from cv_jd_scorer.common.cv_features import detect_seniority
from cv_jd_scorer.engines.v1_tfidf import ats as ats_scorer
from cv_jd_scorer.engines.v1_tfidf import heuristics
from cv_jd_scorer.engines.v1_tfidf import overview as overview_module
from cv_jd_scorer.engines.v1_tfidf import skill_gap as skill_gap_scorer
from cv_jd_scorer.engines.v2_ml import jd_fit as jd_fit_scorer
from cv_jd_scorer.models import ReasoningStep, ScoreResult


_TRENDS_DISABLED = {
    "trendsSummary": {
        "eyebrow": "MARKET TRENDS",
        "titleGrowing": "Not Available",
        "sub": "Market trend analysis is not enabled in this version.",
    },
    "trendRising": [],
    "trendFalling": [],
    "trendsInsight": {
        "text": "Market trend data is not enabled in this version.",
        "source": "—",
    },
}


# -------------------- _build_trace ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: compute
def _build_trace(
    sections: dict,
    jd_text: str,
    jd_score: int,
    ats_score: int,
    n_matches: int,
    n_gaps: int,
    n_skills: int,
    seniority: str,
    peer_pct: int,
) -> list[ReasoningStep]:
    n_exp = len(sections.get("experience", []))
    n_certs = len(sections.get("certifications", []))
    jd_preview = jd_text[:60].replace("\n", " ").strip() + ("…" if len(jd_text) > 60 else "")

    return [
        ReasoningStep(stage="INGEST",    text=f"Parsed CV · {n_exp} employers · {n_skills} skills · {n_certs} certs detected"),
        ReasoningStep(stage="INGEST",    text=f"Extracted JD signal · '{jd_preview}'"),
        ReasoningStep(stage="FIT",       text=f"Semantic embedding alignment · {n_matches} keyword matches · {n_gaps} gaps · score={jd_score}"),
        ReasoningStep(stage="ATS",       text=f"ATS structural scan · score={ats_score}/100"),
        ReasoningStep(stage="SKILLS",    text=f"Skill matrix · {n_skills} skills × 5 tracks scored"),
        ReasoningStep(stage="MARKET",    text=f"Heuristic benchmarks · peer={peer_pct}p · seniority={seniority}"),
        ReasoningStep(stage="PATHS",     text="Adjacent role mapping complete via TF-IDF cosine"),
        ReasoningStep(stage="SYNTHESIS", text="Report assembled · all modules complete"),
    ]
# -------------------- _build_trace ------------- END ----------------


# -------------------- compute ----------- START ----------
# -- Calls : jd_fit_scorer.score (v2 — semantic embeddings),
#            ats_scorer.score, skill_gap_scorer.score,
#            heuristics.compute_peer, heuristics.compute_comp,
#            heuristics.compute_alt_paths, heuristics.compute_alignment,
#            overview_module.compute, detect_seniority, _build_trace
# -- Called by: V2MlEngine.compute
def compute(parsed_cv: dict, jd_text: str) -> ScoreResult:
    raw_text = parsed_cv.get("raw_text", "")
    sections = parsed_cv.get("sections", {})
    ats_redflags = parsed_cv.get("ats_redflags", {})

    skills_block = sections.get("skills", {})
    n_skills = len(skills_block.get("items", [])) if isinstance(skills_block, dict) else 0

    seniority = detect_seniority(jd_text)

    # Layer 2 modules — jd_fit is v2 (semantic); the rest are reused from v1.
    jd_summary, jd_matches, jd_gaps = jd_fit_scorer.score(parsed_cv, jd_text, sections)
    ats_summary, ats_checks         = ats_scorer.score(ats_redflags)
    skill_gap_result                = skill_gap_scorer.score(sections, jd_text)
    peer_result                     = heuristics.compute_peer(sections)
    comp_result                     = heuristics.compute_comp(jd_text, sections)
    alt_paths_result                = heuristics.compute_alt_paths(raw_text, jd_text)
    alignment_result                = heuristics.compute_alignment(sections, jd_text)

    peer_pct = peer_result["peerSummary"]["titlePercentile"]
    peer_bucket_idx = peer_result["peerYouBucket"]
    comp_you = comp_result["compBandData"]["you"]
    comp_p50 = comp_result["compBandData"]["p50"]
    align_you = alignment_result["alignYou"]
    align_avg = sum(align_you) / len(align_you) if align_you else 0.5

    overview_result = overview_module.compute(
        jd_score=jd_summary.score,
        ats_score=ats_summary.score,
        peer_percentile=peer_bucket_idx * 7,
        comp_you=comp_you,
        comp_p50=comp_p50,
        align_avg=align_avg,
        jd_gaps=[g.model_dump() for g in jd_gaps],
        jd_text=jd_text,
        seniority=seniority,
    )

    trace = _build_trace(
        sections=sections,
        jd_text=jd_text,
        jd_score=jd_summary.score,
        ats_score=ats_summary.score,
        n_matches=len(jd_matches),
        n_gaps=len(jd_gaps),
        n_skills=n_skills,
        seniority=seniority,
        peer_pct=peer_bucket_idx * 7,
    )

    return ScoreResult(
        engine_version="v2_ml",
        reasoningTrace=trace,
        jdFitSummary=jd_summary,
        jdFitMatches=jd_matches,
        jdFitGaps=jd_gaps,
        atsSummary=ats_summary,
        atsChecks=ats_checks,
        **skill_gap_result,
        **peer_result,
        **comp_result,
        **alt_paths_result,
        **_TRENDS_DISABLED,
        **alignment_result,
        **overview_result,
    )
# -------------------- compute ------------- END ----------------
