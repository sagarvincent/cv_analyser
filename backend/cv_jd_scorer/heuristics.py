import math

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from cv_jd_scorer.data.role_profiles import ROLES
from cv_jd_scorer.data.salary_bands import BANDS, MARKET_WEIGHTS
from cv_jd_scorer.leaves.cv_leaves import calc_exp_years, detect_seniority
from cv_jd_scorer.leaves.score_leaves import clamp_100, clamp_unit


_N_BUCKETS = 16
_ALIGN_AXES = [
    "Technical Depth",
    "Leadership",
    "Domain Expertise",
    "Collaboration",
    "Execution",
    "Seniority Match",
]


# -------------------- _bell_histogram ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: compute_peer
def _bell_histogram(you_bucket: int, n: int = _N_BUCKETS) -> list[int]:
    centre = n // 2
    return [max(1, int(40 * math.exp(-0.5 * ((i - centre) / 3.5) ** 2))) for i in range(n)]
# -------------------- _bell_histogram ------------- END ----------------


# -------------------- compute_peer ----------- START ----------
# -- Calls : calc_exp_years, clamp_100, _bell_histogram
# -- Called by: scorer.compute
def compute_peer(sections: dict) -> dict:
    exp_years = calc_exp_years(sections.get("experience", []))
    skills_block = sections.get("skills", {})
    n_skills = len(skills_block.get("items", [])) if isinstance(skills_block, dict) else 0
    n_certs = len(sections.get("certifications", []))

    strength = clamp_100(exp_years * 5 + n_skills * 1.5 + n_certs * 5)
    percentile = max(1, min(99, strength))

    you_bucket = int(percentile / 100 * (_N_BUCKETS - 1))
    p50_bucket = _N_BUCKETS // 2

    sections_filled = sum(
        1 for k in ("summary", "experience", "education", "skills", "projects", "certifications", "other")
        if sections.get(k)
    )

    dimensions = [
        {"dim": "Experience Depth", "you": round(clamp_unit(exp_years / 15), 2), "p50": 0.5},
        {"dim": "Skill Breadth",    "you": round(clamp_unit(n_skills / 40), 2),  "p50": 0.5},
        {"dim": "Certifications",   "you": round(clamp_unit(n_certs / 8), 2),    "p50": 0.3},
        {"dim": "Profile Completeness", "you": round(sections_filled / 7, 2),    "p50": 0.6},
    ]

    return {
        "peerSummary": {
            "eyebrow": "PEER BENCHMARK",
            "titlePercentile": f"{percentile}th percentile",
            "sub": f"Scored against {n_skills} skills · {round(exp_years, 1)} yrs exp · {n_certs} certs",
        },
        "peerBuckets": _bell_histogram(you_bucket),
        "peerYouBucket": you_bucket,
        "peerP50Bucket": p50_bucket,
        "peerDimensions": dimensions,
    }
# -------------------- compute_peer ------------- END ----------------


# -------------------- compute_comp ----------- START ----------
# -- Calls : detect_seniority, calc_exp_years, clamp_unit
# -- Called by: scorer.compute
def compute_comp(jd_text: str, sections: dict) -> dict:
    seniority = detect_seniority(jd_text)
    band = BANDS[seniority]
    min_, p25, p50, p75, max_ = band

    exp_years = calc_exp_years(sections.get("experience", []))
    you = int(p25 + clamp_unit(exp_years / 15) * (p75 - p25))

    gap = you - p50
    gap_str = f"${abs(gap) // 1000}k {'above' if gap >= 0 else 'below'} median"

    ref_cards = [
        {"label": "Market Median", "value": f"${p50 // 1000}k", "sub": f"{seniority.title()} role", "tone": "accent"},
        {"label": "Role p75",      "value": f"${p75 // 1000}k", "sub": "Top quartile",             "tone": "good"},
        {"label": "Your Estimate", "value": f"${you // 1000}k", "sub": gap_str,                    "tone": "warn" if gap < 0 else "good"},
    ]

    return {
        "compSummary": {
            "eyebrow": "COMPENSATION",
            "titleUnderpaid": gap_str,
            "sub": f"Estimated from {round(exp_years, 1)} yrs exp · {seniority} band",
            "bandTitle": f"{seniority.title()} salary band",
        },
        "compBandData": {"min": min_, "p25": p25, "p50": p50, "p75": p75, "max": max_, "you": you},
        "compRefCards": ref_cards,
    }
# -------------------- compute_comp ------------- END ----------------


# -------------------- compute_alt_paths ----------- START ----------
# -- Calls : clamp_unit
# -- Called by: scorer.compute
def compute_alt_paths(cv_raw_text: str, jd_text: str) -> dict:
    role_names = list(ROLES.keys())
    role_texts = list(ROLES.values())

    if cv_raw_text.strip():
        vec = TfidfVectorizer()
        all_texts = [cv_raw_text] + role_texts
        matrix = vec.fit_transform(all_texts)
        sims = cosine_similarity(matrix[0:1], matrix[1:])[0]
        fits = [round(clamp_unit(float(s)), 2) for s in sims]
    else:
        fits = [0.5] * len(role_names)

    paired = sorted(zip(fits, role_names), reverse=True)
    top6 = paired[:6]

    seniority = detect_seniority(jd_text)
    band = BANDS[seniority]
    center_title = _extract_center_role(jd_text) or "Your Profile"

    nodes = []
    for i, (fit, title) in enumerate(top6):
        ring = 1 if i < 3 else 2
        salary_p50 = band[2]
        nodes.append({
            "id": f"role_{i}",
            "title": title,
            "fit": fit,
            "salary": f"${salary_p50 // 1000}k",
            "ring": ring,
        })

    links = [{"from": "center", "to": f"role_{i}", "fit": top6[i][0]} for i in range(len(top6))]
    # Add a couple cross-links between ring-1 nodes
    if len(top6) >= 3:
        links.append({"from": "role_0", "to": "role_1", "fit": round((top6[0][0] + top6[1][0]) / 2, 2)})
        links.append({"from": "role_1", "to": "role_2", "fit": round((top6[1][0] + top6[2][0]) / 2, 2)})

    top_role = top6[0][1] if top6 else "adjacent roles"

    return {
        "altPathsSummary": {
            "eyebrow": "ALTERNATIVE PATHS",
            "titleWarn": f"{len(top6)} adjacent roles",
            "titleRest": " identified from your profile",
            "sub": f"Closest match: {top_role}",
        },
        "altPathsCenter": {"title": center_title},
        "altPathsNodes": nodes,
        "altPathsLinks": links,
        "altPathsInsight": {
            "text": f"Your profile most closely aligns with {top_role}. Skill overlap with adjacent roles suggests strong lateral mobility.",
            "source": "Heuristic role similarity",
        },
    }
# -------------------- compute_alt_paths ------------- END ----------------


# -------------------- _extract_center_role ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: compute_alt_paths
def _extract_center_role(jd_text: str) -> str | None:
    for role in ROLES:
        if role.lower() in jd_text.lower():
            return role
    return None
# -------------------- _extract_center_role ------------- END ----------------


# -------------------- compute_alignment ----------- START ----------
# -- Calls : detect_seniority, calc_exp_years, clamp_unit
# -- Called by: scorer.compute
def compute_alignment(sections: dict, jd_text: str) -> dict:
    seniority = detect_seniority(jd_text)
    exp_years = calc_exp_years(sections.get("experience", []))
    skills_block = sections.get("skills", {})
    n_skills = len(skills_block.get("items", [])) if isinstance(skills_block, dict) else 0
    n_certs = len(sections.get("certifications", []))

    cv_text = " ".join(
        str(v) for exp in sections.get("experience", []) for v in exp.values()
    ).lower()

    leadership_kws = ["led", "managed", "directed", "mentored", "headed", "oversaw"]
    collab_kws = ["cross-functional", "stakeholder", "collaborated", "partnered", "aligned"]

    you_scores = [
        clamp_unit(n_skills / 40),
        0.8 if any(kw in cv_text for kw in leadership_kws) else 0.3,
        clamp_unit(exp_years / 12),
        0.8 if any(kw in cv_text for kw in collab_kws) else 0.5,
        clamp_unit((n_certs + (1 if sections.get("projects") else 0)) / 6),
        clamp_unit(min(exp_years, 15) / 15),
    ]
    you_scores = [round(v, 2) for v in you_scores]

    market_scores = [round(v, 2) for v in MARKET_WEIGHTS.get(seniority, MARKET_WEIGHTS["mid"])]

    you_avg = sum(you_scores) / len(you_scores)
    market_avg = sum(market_scores) / len(market_scores)
    gap_pct = abs(you_avg - market_avg)

    return {
        "alignSummary": {
            "eyebrow": "MARKET ALIGNMENT",
            "titleAccent": f"{int(you_avg * 100)}% profile match",
            "titleWarn": f" · {int(gap_pct * 100)}pt gap vs market",
            "sub": f"Benchmarked against {seniority} demand profile",
        },
        "alignAxes": _ALIGN_AXES,
        "alignYou": you_scores,
        "alignMarket": market_scores,
    }
# -------------------- compute_alignment ------------- END ----------------
