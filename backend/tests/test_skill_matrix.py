"""
Tests for BES04_SkillMatrix.

Coverage:
  - text_leaves: jd_phrases (header filtering, dedup), resume_phrases
  - score_leaves: aggregate_sim, format_delta, build_delta_cards (distinct topics)
  - classifier: classify_bucket (argmax + per-category norms)
  - jd_categories: build_rows (base rows, emergent rows, empty-JD fallback, cap)
  - scorer: score_rows (matrix shape, PEER P50, empty-resume → YOU 0)
  - builder: end-to-end (marked `integration` — loads the embedding model)

The pure-logic tests inject numpy vectors and never load the model, so they run
fast and need no sentence-transformers download.
"""
import numpy as np
import pytest

from BES04_SkillMatrix.classifier import classify_bucket
from BES04_SkillMatrix.jd_categories import _is_skill_like, _short_label, build_rows
from BES04_SkillMatrix.leaves.score_leaves import (
    aggregate_sim,
    build_delta_cards,
    format_delta,
)
from BES04_SkillMatrix.leaves.text_leaves import jd_phrases, resume_phrases
from BES04_SkillMatrix.scorer import COHORTS, score_rows


# ── text_leaves ──────────────────────────────────────────────────────────────

def test_jd_phrases_filters_headers_and_dedups():
    jd = "Responsibilities\n• Build React apps, Node.js\nRequirements\n5+ years React"
    phrases = jd_phrases(jd)
    low = [p.lower() for p in phrases]
    assert "responsibilities" not in low
    assert "requirements" not in low
    assert any("react" in p for p in low)
    assert len(low) == len(set(low))  # de-duplicated


def test_jd_phrases_empty():
    assert jd_phrases("") == []
    assert jd_phrases("   \n  ") == []


def test_jd_phrases_keeps_hyphenated_terms():
    joined = " ".join(jd_phrases("React, Node-based tooling, end-to-end testing")).lower()
    assert "node-based tooling" in joined     # not fragmented at the hyphen
    assert "end-to-end testing" in joined


def test_resume_phrases_collects_skills_and_experience():
    sections = {
        "skills": {"items": ["Python", "SQL"]},
        "experience": [{"description": "Led a team " * 30}],
    }
    phrases = resume_phrases(sections)
    assert "Python" in phrases and "SQL" in phrases
    assert any("Led a team" in p for p in phrases)


# ── score_leaves ─────────────────────────────────────────────────────────────

def test_aggregate_sim_bounds():
    assert aggregate_sim([]) == 0.0
    assert aggregate_sim([1.0, 1.0]) == 1.0
    assert 0.0 <= aggregate_sim([-0.5, 0.4, 0.9]) <= 1.0


def test_format_delta_signs():
    assert format_delta(0.27) == "+27"
    assert format_delta(-0.42) == "−42"   # U+2212 minus sign
    assert format_delta(0.0) == "+0"


def test_build_delta_cards_distinct_topics():
    names = ["A", "B", "C"]
    you = [0.9, 0.2, 0.55]
    ask = [0.5, 0.8, 0.50]
    cards = build_delta_cards(names, you, ask)
    assert [c["label"] for c in cards] == ["OVER-INDEX", "BIGGEST GAP", "CLOSEST MATCH"]
    assert cards[0]["topic"] == "A"          # delta +0.40 → biggest over
    assert cards[1]["topic"] == "B"          # delta -0.60 → biggest gap
    assert cards[2]["topic"] == "C"          # closest, drawn from the remainder
    assert cards[0]["delta"] == "+40"
    assert cards[1]["delta"].startswith("−")
    assert len({c["topic"] for c in cards}) == 3


def test_build_delta_cards_empty():
    assert build_delta_cards([], [], []) == []


def test_build_delta_cards_all_negative_is_not_over_index():
    # Every category sits under the JD's ask — the top card must not claim an over-index.
    names = ["A", "B", "C"]
    you = [0.36, 0.24, 0.22]
    ask = [0.49, 0.70, 0.36]          # deltas: A -0.13, B -0.46, C -0.14
    cards = build_delta_cards(names, you, ask)
    assert cards[0]["label"] == "SMALLEST GAP"
    assert "exceed" not in cards[0]["note"].lower()
    assert cards[1]["label"] == "BIGGEST GAP" and cards[1]["topic"] == "B"


# ── jd_categories: emergent gating ───────────────────────────────────────────

def test_is_skill_like_rejects_prose_fragments():
    assert not _is_skill_like("9 years of hands")     # leading number
    assert not _is_skill_like("And maintaining end")  # leading connector
    assert not _is_skill_like("Developing")           # leading action verb
    assert not _is_skill_like("5 years experience")   # requirement boilerplate
    assert not _is_skill_like("Job Title: Design Engineer")  # header line
    assert _is_skill_like("Python")
    assert _is_skill_like("machine learning")
    assert _is_skill_like("Kubernetes")


def test_short_label_strips_leading_qualifiers():
    assert _short_label("Strong React") == "React"
    assert _short_label("Proven TypeScript") == "TypeScript"
    assert _short_label("React") == "React"


# ── classifier ───────────────────────────────────────────────────────────────

def test_classify_bucket_picks_argmax_and_norms():
    cat_vecs = {"A": np.array([1.0, 0.0, 0.0]), "B": np.array([0.0, 1.0, 0.0])}
    bucket_vecs = {"X": np.array([1.0, 0.0, 0.0]), "Y": np.array([0.0, 1.0, 0.0])}
    cv = np.array([0.9, 0.1, 0.0])           # closest to X
    bucket, norms = classify_bucket(cv, bucket_vecs, cat_vecs)
    assert bucket == "X"
    assert norms["A"] == 1.0                  # cosine(X, A)
    assert norms["B"] == 0.0                  # cosine(X, B)


# ── jd_categories ────────────────────────────────────────────────────────────

def test_build_rows_base_and_emergent():
    cat_vecs = {"Cat1": np.array([1.0, 0.0, 0.0, 0.0]),
                "Cat2": np.array([0.0, 1.0, 0.0, 0.0])}
    bucket_norms = {"Cat1": 0.6, "Cat2": 0.4}
    phrases = ["cat1 thing", "weird skill"]
    phrase_vecs = np.array([[1.0, 0.0, 0.0, 0.0],   # → Cat1 (base)
                            [0.0, 0.0, 1.0, 0.0]])  # → no category (emergent)
    rows = build_rows(phrases, phrase_vecs, cat_vecs, bucket_norms)
    names = [r["name"] for r in rows]
    assert "Cat1" in names
    assert "Cat2" not in names                # no JD signal → below base threshold
    assert any(n.lower().startswith("weird skill") for n in names)


def test_build_rows_empty_jd_uses_bucket_top():
    cat_vecs = {"Cat1": np.array([1.0, 0.0]), "Cat2": np.array([0.0, 1.0])}
    bucket_norms = {"Cat1": 0.8, "Cat2": 0.3}
    rows = build_rows([], np.empty((0, 0)), cat_vecs, bucket_norms)
    assert rows[0]["name"] == "Cat1"          # highest bucket norm first
    assert rows[0]["jd_ask"] == 0.8


def test_build_rows_caps_total():
    cat_vecs = {f"C{i}": np.eye(12)[i] for i in range(12)}
    bucket_norms = {k: 0.5 for k in cat_vecs}
    # every phrase aligns with its own category → many base rows
    phrases = [f"c{i}" for i in range(12)]
    phrase_vecs = np.eye(12)
    rows = build_rows(phrases, phrase_vecs, cat_vecs, bucket_norms)
    assert len(rows) <= 8


# ── scorer ───────────────────────────────────────────────────────────────────

def test_score_rows_shape_and_peer():
    rows = [{"name": "A", "jd_ask": 0.7, "bucket_norm": 0.6, "vec": np.array([1.0, 0.0, 0.0])}]
    resume = np.array([[1.0, 0.0, 0.0]])
    matrix, you, ask = score_rows(rows, resume)
    assert COHORTS == ["YOU", "JD ASK", "BUCKET NORM", "PEER P50"]
    assert len(matrix) == 1 and len(matrix[0]) == 4
    assert matrix[0][3] == 0.5                # PEER P50
    assert matrix[0][1] == 0.7 and matrix[0][2] == 0.6
    assert you[0] > 0.0                       # resume aligns with the row


def test_score_rows_empty_resume_zero_you():
    rows = [{"name": "A", "jd_ask": 0.7, "bucket_norm": 0.6, "vec": np.array([1.0, 0.0, 0.0])}]
    matrix, you, ask = score_rows(rows, np.empty((0, 0)))
    assert matrix[0][0] == 0.0 and you[0] == 0.0


# ── builder (end-to-end, real model) ─────────────────────────────────────────

@pytest.mark.integration
def test_build_skill_matrix_end_to_end():
    from BES04_SkillMatrix.builder import build_skill_matrix

    parsed_cv = {
        "raw_text": "Senior product designer with design systems and prototyping experience.",
        "sections": {
            "summary": "Senior product designer",
            "skills": {"items": ["Figma", "Prototyping", "User research", "Design systems"]},
            "experience": [{"title": "Product Designer",
                            "description": "Led design system and prototyping for a fintech app"}],
        },
    }
    jd = ("Job Title: Product Designer\nRequirements\n"
          "Figma, prototyping, design systems, user research, stakeholder management")

    result = build_skill_matrix(parsed_cv, jd).model_dump()
    assert result["skillMatrixCohorts"] == ["YOU", "JD ASK", "BUCKET NORM", "PEER P50"]
    assert len(result["skillMatrixData"]) == len(result["skillMatrixCategories"]) > 0
    assert all(len(row) == 4 for row in result["skillMatrixData"])
    assert len(result["skillMatrixDeltaCards"]) == 3
    assert result["skillMatrixSummary"]["bucket"]
