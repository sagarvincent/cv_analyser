from __future__ import annotations

import numpy as np

from BES04_SkillMatrix.leaves.text_leaves import clamp_unit
from BES04_SkillMatrix.leaves.vector_leaves import cosine_sim


# -------------------- classify_bucket ----------- START ----------
# -- Calls : cosine_sim, clamp_unit
# -- Called by: builder.build_skill_matrix
def classify_bucket(
    cv_vec: np.ndarray,
    bucket_vecs: dict[str, np.ndarray],
    cat_vecs: dict[str, np.ndarray],
) -> tuple[str, dict[str, float]]:
    """Step 1 — pick the job-profile bucket the resume falls into (highest cosine
    of the CV against each bucket profile), then derive that bucket's expected
    emphasis per skill category (its 'BUCKET NORM' column)."""
    bucket = max(bucket_vecs, key=lambda b: cosine_sim(cv_vec, bucket_vecs[b]))
    norms = {
        cat: clamp_unit(cosine_sim(bucket_vecs[bucket], cat_vecs[cat]))
        for cat in cat_vecs
    }
    return bucket, norms
# -------------------- classify_bucket ------------- END ----------------
