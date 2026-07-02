from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

# Self-contained embedder for BES04 — a standalone copy of the all-MiniLM wrapper
# so the Skill Matrix service depends on nothing in BES03.
_MODEL_NAME = "all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


# -------------------- _get_model ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: embed, embed_many
def _get_model() -> SentenceTransformer:
    """Lazy singleton — the model (and torch) only load on first use, keeping
    import of this service cheap until a score is actually requested."""
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model
# -------------------- _get_model ------------- END ----------------


# -------------------- build_cv_text ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: builder.build_skill_matrix
def build_cv_text(parsed_cv: dict) -> str:
    """Assemble a focused CV representation for embedding — summary + skills +
    recent experience — so the model window sees signal, not boilerplate.
    Falls back to truncated raw_text when sections are empty."""
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
        if not isinstance(exp, dict):
            continue
        role = exp.get("role") or exp.get("title") or ""
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
# -- Called by: builder.build_skill_matrix
def embed(text: str) -> np.ndarray:
    """Return a unit-normalised embedding vector for *text*."""
    return _get_model().encode(text, normalize_embeddings=True)
# -------------------- embed ------------- END ----------------


# -------------------- embed_many ----------- START ----------
# -- Calls : _get_model
# -- Called by: builder.build_skill_matrix
def embed_many(texts: list[str]) -> np.ndarray:
    """Batch-embed *texts* in a single model call → array of shape (len, dim).
    Returns an empty (0, 0) array for an empty input so callers can branch on it."""
    if not texts:
        return np.empty((0, 0), dtype=np.float32)
    return _get_model().encode(texts, normalize_embeddings=True)
# -------------------- embed_many ------------- END ----------------
