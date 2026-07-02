from __future__ import annotations

import numpy as np


# -------------------- cosine_sim ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: classifier.classify_bucket, scorer.score_rows, jd_categories.build_rows
def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Dot product of two unit-normalised vectors equals cosine similarity.
    Pure numpy — kept out of embedder.py so the scoring logic carries no
    sentence-transformers import."""
    return float(np.dot(a, b))
# -------------------- cosine_sim ------------- END ----------------
