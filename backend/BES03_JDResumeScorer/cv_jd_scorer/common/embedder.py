from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

_MODEL_NAME = "all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


# -------------------- _get_model ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: embed
def _get_model() -> SentenceTransformer:
    """Lazy singleton — the model (and torch) only load on first embed() call,
    keeping v1_tfidf deployments free of the heavy ML dependency."""
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model
# -------------------- _get_model ------------- END ----------------


# -------------------- build_cv_text ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: v2_ml jd_fit.score
def build_cv_text(parsed_cv: dict) -> str:
    """Assemble a focused CV representation for embedding.

    Prefers structured sections (summary + skills + recent experience) over the
    full raw_text so the 256-token model window sees signal, not boilerplate.
    Falls back to truncated raw_text when sections are empty.
    """
    sections = parsed_cv.get("sections", {})
    parts: list[str] = []

    summary = sections.get("summary", "")
    if isinstance(summary, str) and summary.strip():
        parts.append(summary.strip())

    skills = sections.get("skills", {})
    if isinstance(skills, dict):
        items = skills.get("items", [])
        if items:
            parts.append(" ".join(str(i) for i in items))
    elif isinstance(skills, str) and skills.strip():
        parts.append(skills.strip())

    for exp in (sections.get("experience") or [])[:4]:
        role = exp.get("role", "")
        desc = exp.get("description", "")
        if role:
            parts.append(str(role))
        if desc:
            parts.append(str(desc)[:300])

    if not parts:
        parts.append(parsed_cv.get("raw_text", "")[:1500])

    return " ".join(parts)
# -------------------- build_cv_text ------------- END ----------------


# -------------------- embed ----------- START ----------
# -- Calls : _get_model
# -- Called by: v2_ml jd_fit.score
def embed(text: str) -> np.ndarray:
    """Return a unit-normalised embedding vector for *text*."""
    return _get_model().encode(text, normalize_embeddings=True)
# -------------------- embed ------------- END ----------------


# -------------------- cosine_sim ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: v2_ml jd_fit.score
def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Dot product of two unit-normalised vectors equals cosine similarity."""
    return float(np.dot(a, b))
# -------------------- cosine_sim ------------- END ----------------
