from __future__ import annotations

import numpy as np

from BES04_SkillMatrix import classifier, embedder, jd_categories, scorer
from BES04_SkillMatrix.data.taxonomy import BUCKETS, CATEGORIES
from BES04_SkillMatrix.leaves import score_leaves, text_leaves
from BES04_SkillMatrix.models import SkillMatrix, SkillMatrixDeltaCard, SkillMatrixSummary

# Static taxonomy/bucket vectors never change → embed once, cache for the process.
_cat_vecs: dict[str, np.ndarray] | None = None
_bucket_vecs: dict[str, np.ndarray] | None = None


# -------------------- _category_vectors ----------- START ----------
# -- Calls : embedder.embed_many
# -- Called by: build_skill_matrix
def _category_vectors() -> dict[str, np.ndarray]:
    global _cat_vecs
    if _cat_vecs is None:
        names = list(CATEGORIES)
        protos = [" ".join(CATEGORIES[n]) for n in names]
        vecs = embedder.embed_many(protos)
        _cat_vecs = {n: vecs[i] for i, n in enumerate(names)}
    return _cat_vecs
# -------------------- _category_vectors ------------- END ----------------


# -------------------- _bucket_vectors ----------- START ----------
# -- Calls : embedder.embed_many
# -- Called by: build_skill_matrix
def _bucket_vectors() -> dict[str, np.ndarray]:
    global _bucket_vecs
    if _bucket_vecs is None:
        names = list(BUCKETS)
        vecs = embedder.embed_many([BUCKETS[n] for n in names])
        _bucket_vecs = {n: vecs[i] for i, n in enumerate(names)}
    return _bucket_vecs
# -------------------- _bucket_vectors ------------- END ----------------


# -------------------- build_skill_matrix ----------- START ----------
# -- Calls : embedder.*, classifier.classify_bucket, text_leaves.*, jd_categories.build_rows,
#            scorer.score_rows, score_leaves.build_delta_cards
# -- Called by: interface.score_endpoint
def build_skill_matrix(parsed_cv: dict, jd_text: str) -> SkillMatrix:
    """Run the three-step Skill Matrix: classify the resume's bucket, derive the
    JD's demanded categories, then score the resume's evidence against them."""
    sections = parsed_cv.get("sections", {}) or {}
    cat_vecs = _category_vectors()
    bucket_vecs = _bucket_vectors()

    # Step 1 — bucket
    cv_vec = embedder.embed(embedder.build_cv_text(parsed_cv))
    bucket, bucket_norms = classifier.classify_bucket(cv_vec, bucket_vecs, cat_vecs)

    # Step 2 — JD categories (rows)
    phrases = text_leaves.jd_phrases(jd_text)
    phrase_vecs = embedder.embed_many(phrases)
    rows = jd_categories.build_rows(phrases, phrase_vecs, cat_vecs, bucket_norms)

    # Step 3 — score the resume against each row
    resume_vecs = embedder.embed_many(text_leaves.resume_phrases(sections))
    matrix, you_vals, jd_ask_vals = scorer.score_rows(rows, resume_vecs)

    names = [r["name"] for r in rows]
    delta_cards = score_leaves.build_delta_cards(names, you_vals, jd_ask_vals)

    deltas = [you_vals[i] - jd_ask_vals[i] for i in range(len(names))]
    over_topic = names[max(range(len(names)), key=lambda i: deltas[i])] if names else "—"
    under_topic = names[min(range(len(names)), key=lambda i: deltas[i])] if names else "—"
    noun = "category" if len(names) == 1 else "categories"

    summary = SkillMatrixSummary(
        eyebrow="SKILL MATRIX",
        bucket=bucket,
        overIndexTopic=over_topic,
        underIndexTopic=under_topic,
        sub=f"Profile: {bucket} · {len(names)} JD {noun} scored",
    )

    return SkillMatrix(
        skillMatrixSummary=summary,
        skillMatrixCategories=names,
        skillMatrixCohorts=scorer.COHORTS,
        skillMatrixData=matrix,
        skillMatrixDeltaCards=[SkillMatrixDeltaCard(**c) for c in delta_cards],
    )
# -------------------- build_skill_matrix ------------- END ----------------
