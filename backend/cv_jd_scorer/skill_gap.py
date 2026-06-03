from cv_jd_scorer.data.skill_tracks import TRACKS
from cv_jd_scorer.leaves.cv_leaves import extract_skill_tokens
from cv_jd_scorer.leaves.score_leaves import clamp_unit


_MAX_SKILLS = 10
_DELTA_COLORS = {
    "over": "var(--good)",
    "under": "var(--warn)",
    "neutral": "var(--text-2)",
}


# -------------------- _overlap_score ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: score
def _overlap_score(skill_tokens: set[str], track_keywords: list[str]) -> float:
    if not track_keywords:
        return 0.0
    hits = sum(1 for kw in track_keywords if any(kw in token for token in skill_tokens))
    return clamp_unit(hits / len(track_keywords))
# -------------------- _overlap_score ------------- END ----------------


# -------------------- score ----------- START ----------
# -- Calls : extract_skill_tokens, _overlap_score, clamp_unit
# -- Called by: scorer.compute
def score(sections: dict, jd_text: str) -> dict:
    skills_block = sections.get("skills", {})
    if isinstance(skills_block, dict):
        skill_items = skills_block.get("items", [])
    else:
        skill_items = []

    skill_items = skill_items[:_MAX_SKILLS] if skill_items else ["General Skills"]
    track_names = list(TRACKS.keys())

    # Build 2D matrix: skill × track
    matrix: list[list[float]] = []
    for skill in skill_items:
        skill_tokens = set(skill.lower().split())
        row = [_overlap_score(skill_tokens, TRACKS[t]) for t in track_names]
        matrix.append(row)

    # Track-level averages (your CV coverage per track)
    track_avgs = [
        sum(matrix[i][j] for i in range(len(skill_items))) / len(skill_items)
        for j in range(len(track_names))
    ]

    # JD expected demand per track (uniform 0.5 baseline; boost tracks matched by JD keywords)
    jd_lower = jd_text.lower()
    jd_demand = [
        min(1.0, 0.5 + 0.5 * any(kw in jd_lower for kw in TRACKS[t]))
        for t in track_names
    ]

    # Delta cards: track avg vs JD demand
    deltas = [track_avgs[j] - jd_demand[j] for j in range(len(track_names))]
    sorted_idx = sorted(range(len(track_names)), key=lambda j: deltas[j])

    under_track = track_names[sorted_idx[0]]
    over_track = track_names[sorted_idx[-1]]

    delta_cards = []
    for label, idx, sign in [("BIGGEST GAP", sorted_idx[0], -1), ("OVER-INDEX", sorted_idx[-1], 1)]:
        delta_val = deltas[idx]
        delta_str = f"+{abs(int(delta_val*100))}" if delta_val >= 0 else f"−{abs(int(delta_val*100))}"
        color = _DELTA_COLORS["over"] if delta_val >= 0 else _DELTA_COLORS["under"]
        note = (
            "You exceed JD demand in this area." if delta_val >= 0
            else "JD requires more than your CV signals here."
        )
        delta_cards.append({
            "label": label,
            "topic": track_names[idx],
            "delta": delta_str,
            "color": color,
            "note": note,
        })

    # Third delta card: most balanced track
    mid_idx = sorted_idx[len(sorted_idx) // 2]
    delta_cards.append({
        "label": "CLOSEST MATCH",
        "topic": track_names[mid_idx],
        "delta": f"+{abs(int(deltas[mid_idx]*100))}" if deltas[mid_idx] >= 0 else f"−{abs(int(deltas[mid_idx]*100))}",
        "color": _DELTA_COLORS["neutral"],
        "note": "Your coverage aligns closely with JD expectations.",
    })

    return {
        "skillGapSummary": {
            "eyebrow": "SKILL MATRIX",
            "overIndexTopic": over_track,
            "underIndexTopic": under_track,
            "sub": f"Strongest in {over_track.split(' &')[0]} · biggest gap in {under_track.split(' &')[0]}",
        },
        "skillGapSkills": skill_items,
        "skillGapTracks": track_names,
        "skillGapData": [[round(v, 2) for v in row] for row in matrix],
        "skillGapDeltaCards": delta_cards,
    }
# -------------------- score ------------- END ----------------
