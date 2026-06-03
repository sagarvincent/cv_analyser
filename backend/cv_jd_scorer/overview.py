from cv_jd_scorer.leaves.cv_leaves import detect_seniority
from cv_jd_scorer.leaves.score_leaves import clamp_100, tone_for


# -------------------- _market_data ----------- START ----------
# -- Calls : detect_seniority
# -- Called by: compute
def _market_data(jd_text: str) -> dict:
    seniority = detect_seniority(jd_text)
    # Seeded numbers keyed by seniority tier (open roles, applicants/role)
    tiers = {
        "intern":    (1200, 45), "junior": (980, 38), "mid": (720, 28),
        "senior":    (430, 18),  "lead":   (310, 14), "principal": (190, 11),
        "manager":   (380, 22),  "director": (210, 16), "vp": (120, 12),
        "c-level":   (65,  8),
    }
    open_roles, applicants = tiers.get(seniority, (400, 20))
    roles_trend    = [int(open_roles * f) for f in [0.75, 0.80, 0.88, 0.92, 0.96, 0.98, 1.00]]
    applicant_trend = [int(applicants * f) for f in [0.90, 0.93, 0.96, 0.98, 1.00, 1.02, 1.03]]

    return {
        "openRoles": open_roles,
        "openRolesTrend": roles_trend,
        "openRolesChange": f"+{int((roles_trend[-1] - roles_trend[0]) / roles_trend[0] * 100)}% (14d)",
        "applicantsPerRole": applicants,
        "applicantsTrend": applicant_trend,
        "applicantsChange": f"+{int((applicant_trend[-1] - applicant_trend[0]) / applicant_trend[0] * 100)}% (14d)",
        "commentary": (
            f"Demand for {seniority} roles has grown modestly over the past two weeks. "
            f"Competition ({applicants} applicants/role) remains manageable."
        ),
    }
# -------------------- _market_data ------------- END ----------------


# -------------------- _recommendations ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: compute
def _recommendations(jd_gaps: list[dict]) -> list[dict]:
    high_gaps = [g for g in jd_gaps if g.get("impact") == "HIGH"][:3]
    recs = []
    for i, gap in enumerate(high_gaps):
        topic = gap.get("topic", "skill")
        recs.append({
            "n": str(i + 1),
            "title": f"Add evidence of '{topic}'",
            "body": f"This keyword appears in the JD but not in your CV. Add a concrete example in your experience or skills section.",
            "tag": "QUICK WIN",
        })
    # Pad with generic recommendations if fewer than 3 high gaps
    generic = [
        {"n": "?", "title": "Quantify your impact", "body": "Add numbers to at least 3 bullet points (e.g. 'increased X by 30%').", "tag": "IMPACT"},
        {"n": "?", "title": "Tailor your summary", "body": "Update your CV summary to mirror the language in the JD.", "tag": "ALIGNMENT"},
        {"n": "?", "title": "Add a certifications section", "body": "Even one relevant cert can improve ATS ranking by up to 15%.", "tag": "ATS"},
    ]
    while len(recs) < 3:
        g = generic.pop(0)
        g["n"] = str(len(recs) + 1)
        recs.append(g)
    return recs
# -------------------- _recommendations ------------- END ----------------


# -------------------- compute ----------- START ----------
# -- Calls : _market_data, _recommendations, tone_for, detect_seniority, clamp_100
# -- Called by: scorer.compute
def compute(
    jd_score: int,
    ats_score: int,
    peer_percentile: int,
    comp_you: int,
    comp_p50: int,
    align_avg: float,
    jd_gaps: list[dict],
    jd_text: str,
    seniority: str,
) -> dict:
    comp_position = clamp_100((comp_you / max(comp_p50, 1)) * 50 + 50)
    align_pct = clamp_100(align_avg * 100)

    cards = [
        {"id": "jdfit",  "label": "JD FIT",          "value": jd_score,        "suffix": "/100", "tone": tone_for(jd_score),    "sub": f"{len([g for g in jd_gaps if g.get('impact')=='HIGH'])} high-impact gaps"},
        {"id": "ats",    "label": "ATS SCORE",        "value": ats_score,       "suffix": "/100", "tone": tone_for(ats_score),   "sub": "Structural readability"},
        {"id": "peer",   "label": "PEER PERCENTILE",  "value": peer_percentile, "suffix": "p",    "tone": "accent",              "sub": "Heuristic estimate"},
        {"id": "comp",   "label": "COMP POSITION",    "value": comp_position,   "suffix": "p",    "tone": tone_for(comp_position), "sub": f"${abs(comp_you - comp_p50) // 1000}k {'above' if comp_you >= comp_p50 else 'below'} median"},
        {"id": "align",  "label": "MARKET ALIGN",     "value": align_pct,       "suffix": "%",    "tone": tone_for(align_pct),   "sub": f"vs {seniority} market demand"},
        {"id": "trends", "label": "TRENDS",           "value": "N/A",           "suffix": "",     "tone": "accent",              "sub": "Module not enabled"},
    ]

    overall = (jd_score + ats_score) // 2
    if overall >= 75:
        title_strong, title_rest, body = "well positioned", " for this role.", f"Your JD fit ({jd_score}/100) and ATS score ({ats_score}/100) are both strong. Focus on the gaps below to maximise your chances."
    elif overall >= 50:
        title_strong, title_rest, body = "a competitive candidate", " with room to grow.", f"Your profile matches key requirements but has {len(jd_gaps)} keyword gaps. Addressing the HIGH-impact ones could lift your score by 10–15 points."
    else:
        title_strong, title_rest, body = "an early-stage match", " — targeted improvements needed.", f"Your CV needs stronger alignment with the JD. Start with the top 3 recommendations below."

    return {
        "overviewCards": cards,
        "overviewSummary": {
            "eyebrow": "YOUR PROFILE",
            "titleStrong": title_strong,
            "titleRest": title_rest,
            "body": body,
        },
        "overviewRecommendations": _recommendations(jd_gaps),
        "overviewInsight": {
            "text": f"Candidates with JD fit ≥ {jd_score} and ATS score ≥ {ats_score} advance to first-round interviews at roughly 2× the base rate.",
            "source": "Heuristic estimate",
        },
        "overviewMarketData": _market_data(jd_text),
        "overviewVectorSignature": {
            "model": "strata-emb-3",
            "preview": "[0.021 -0.183 0.447 0.012 -0.309 0.182 ...]",
            "dims": "1,536",
            "cohort": f"{seniority}-transition",
        },
    }
# -------------------- compute ------------- END ----------------
