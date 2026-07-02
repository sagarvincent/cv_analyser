from __future__ import annotations

import numpy as np

from BES04_SkillMatrix.leaves.score_leaves import aggregate_sim
from BES04_SkillMatrix.leaves.text_leaves import clamp_unit
from BES04_SkillMatrix.leaves.vector_leaves import cosine_sim

COHORTS = ["YOU", "JD ASK", "BUCKET NORM", "PEER P50"]
_PEER_P50 = 0.5


# -------------------- score_rows ----------- START ----------
# -- Calls : cosine_sim, aggregate_sim, clamp_unit
# -- Called by: builder.build_skill_matrix
def score_rows(
    rows: list[dict],
    resume_vecs: np.ndarray,
) -> tuple[list[list[float]], list[float], list[float]]:
    """Step 3 — score each row across the four cohorts. YOU is the resume's
    semantic coverage of the row; JD ASK / BUCKET NORM come from the row; PEER P50
    is a fixed median. Returns the rounded matrix plus the raw YOU / JD-ASK columns
    (unrounded) for delta-card computation."""
    n_res = len(resume_vecs)
    matrix: list[list[float]] = []
    you_vals: list[float] = []
    jd_ask_vals: list[float] = []

    for row in rows:
        if n_res:
            sims = [cosine_sim(resume_vecs[i], row["vec"]) for i in range(n_res)]
            you = aggregate_sim(sims)
        else:
            you = 0.0
        jd_ask = clamp_unit(row["jd_ask"])
        bucket_norm = clamp_unit(row["bucket_norm"])

        you_vals.append(you)
        jd_ask_vals.append(jd_ask)
        matrix.append([round(you, 2), round(jd_ask, 2), round(bucket_norm, 2), _PEER_P50])

    return matrix, you_vals, jd_ask_vals
# -------------------- score_rows ------------- END ----------------
