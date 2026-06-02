from cv_jd_scorer import ats as ats_scorer
from cv_jd_scorer import jd_fit as jd_fit_scorer
from cv_jd_scorer.models import ReasoningStep, ScoreResult


# -------------------- _build_trace ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: compute
def _build_trace(
    parsed_cv: dict,
    jd_text: str,
    jd_score: int,
    ats_score: int,
    n_matches: int,
    n_gaps: int,
    n_skills: int,
) -> list[ReasoningStep]:
    sections = parsed_cv.get("sections", {})
    n_exp = len(sections.get("experience", []))
    n_certs = len(sections.get("certifications", []))
    jd_preview = jd_text[:60].replace("\n", " ").strip() + ("…" if len(jd_text) > 60 else "")

    return [
        ReasoningStep(stage="INGEST", text=f"Parsed CV · {n_exp} employers · {n_skills} skills · {n_certs} certs detected"),
        ReasoningStep(stage="INGEST", text=f"Extracted JD signal · '{jd_preview}'"),
        ReasoningStep(stage="FIT",    text=f"TF-IDF alignment · {n_matches} keyword matches · {n_gaps} gaps · score={jd_score}"),
        ReasoningStep(stage="ATS",    text=f"ATS structural scan · score={ats_score}/100"),
        ReasoningStep(stage="SYNTHESIS", text="Report assembled · JD Fit and ATS modules complete"),
    ]
# -------------------- _build_trace ------------- END ----------------


# -------------------- compute ----------- START ----------
# -- Calls : jd_fit_scorer.score, ats_scorer.score, _build_trace
# -- Called by: interface.score_endpoint
def compute(parsed_cv: dict, jd_text: str) -> ScoreResult:
    raw_text = parsed_cv.get("raw_text", "")
    sections = parsed_cv.get("sections", {})
    ats_redflags = parsed_cv.get("ats_redflags", {})

    skills_block = sections.get("skills", {})
    if isinstance(skills_block, dict):
        n_skills = len(skills_block.get("items", []))
    else:
        n_skills = 0

    jd_summary, jd_matches, jd_gaps = jd_fit_scorer.score(raw_text, jd_text, sections)
    ats_summary, ats_checks = ats_scorer.score(ats_redflags)

    trace = _build_trace(
        parsed_cv=parsed_cv,
        jd_text=jd_text,
        jd_score=jd_summary.score,
        ats_score=ats_summary.score,
        n_matches=len(jd_matches),
        n_gaps=len(jd_gaps),
        n_skills=n_skills,
    )

    return ScoreResult(
        reasoningTrace=trace,
        jdFitSummary=jd_summary,
        jdFitMatches=jd_matches,
        jdFitGaps=jd_gaps,
        atsSummary=ats_summary,
        atsChecks=ats_checks,
    )
# -------------------- compute ------------- END ----------------
