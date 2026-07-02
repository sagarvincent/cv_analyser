from __future__ import annotations

import numpy as np

from BES04_SkillMatrix.leaves.score_leaves import aggregate_sim
from BES04_SkillMatrix.leaves.vector_leaves import cosine_sim

# Row-selection thresholds (tunable). A category is a "base" row when the JD
# demands it past _BASE_THRESHOLD; a JD phrase becomes an "emergent" row when it
# maps to no known category (best cosine below _EMERGENT_THRESHOLD).
_BASE_THRESHOLD = 0.25
_EMERGENT_THRESHOLD = 0.35
_EMERGENT_FALLBACK_ASK = 0.5  # demand for an emergent skill when there are no base rows to calibrate against
_EMERGENT_NEUTRAL_NORM = 0.5  # outside the taxonomy → no bucket expectation
_MAX_ROWS = 8
_MIN_ROWS = 2
_MAX_EMERGENT = 3
_EMERGENT_MAX_WORDS = 4       # keep emergent rows skill-like, not prose clauses
_FALLBACK_ROWS = 4            # empty-JD: show this many of the bucket's top categories

# An emergent row must look like a skill, not a sentence fragment. Reject phrases
# that lead with a connector/boilerplate noun/action verb, that start with a number
# ("9 years of …"), or that read as a requirement clause ("… years experience").
_EMERGENT_REJECT_LEAD = {
    "and", "or", "the", "a", "an", "with", "of", "to", "for", "in", "on", "at",
    "by", "as", "is", "are", "be", "we", "you", "our", "your", "this", "that",
    "etc", "including", "ability", "experience",
    "developing", "maintaining", "building", "designing", "working", "using",
    "ensuring", "creating", "managing", "leading", "supporting", "delivering",
    "driving", "defining", "implementing", "collaborating", "partnering",
    "owning", "conducting", "performing",
}
_EMERGENT_REJECT_ANY = {"years", "year", "yrs", "experience"}

# Leading qualifier words stripped from an emergent label ("Strong React" → "React").
_LEAD_QUALIFIERS = {
    "strong", "excellent", "proven", "solid", "deep", "extensive", "advanced",
    "expert", "experienced", "good", "great", "proficient", "skilled", "robust",
    "hands-on", "demonstrated", "thorough",
}


# -------------------- _is_skill_like ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_rows
def _is_skill_like(phrase: str) -> bool:
    """True when *phrase* reads like a discrete skill rather than a prose fragment
    or a header line ('Job Title: …')."""
    if ":" in phrase:                     # header/label line, not a skill
        return False
    tokens = phrase.lower().split()
    if not tokens or len(tokens) > _EMERGENT_MAX_WORDS:
        return False
    if tokens[0][:1].isdigit():
        return False
    if tokens[0] in _EMERGENT_REJECT_LEAD:
        return False
    if any(t in _EMERGENT_REJECT_ANY for t in tokens):
        return False
    return any(t.isalpha() and len(t) >= 3 for t in tokens)
# -------------------- _is_skill_like ------------- END ----------------


# -------------------- _short_label ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_rows
def _short_label(phrase: str, limit: int = 28) -> str:
    tokens = phrase.strip().split()
    while len(tokens) > 1 and tokens[0].lower().strip(",.;:") in _LEAD_QUALIFIERS:
        tokens = tokens[1:]
    label = " ".join(tokens)
    if len(label) > limit:
        label = label[:limit].rstrip() + "…"
    return label[:1].upper() + label[1:]
# -------------------- _short_label ------------- END ----------------


# -------------------- build_rows ----------- START ----------
# -- Calls : cosine_sim, aggregate_sim, _short_label
# -- Called by: builder.build_skill_matrix
def build_rows(
    phrases: list[str],
    phrase_vecs: np.ndarray,
    cat_vecs: dict[str, np.ndarray],
    bucket_norms: dict[str, float],
) -> list[dict]:
    """Step 2 (hybrid) — turn the JD into matrix rows. Base rows are taxonomy
    categories the JD demands; emergent rows are strong JD skills with no taxonomy
    home. Each row carries its JD-ASK weight, BUCKET-NORM, and target vector."""
    cat_names = list(cat_vecs)

    # No JD signal → fall back to the bucket's strongest categories.
    if len(phrase_vecs) == 0:
        ranked = sorted(cat_names, key=lambda c: bucket_norms.get(c, 0.0), reverse=True)
        return [
            {"name": c, "jd_ask": bucket_norms.get(c, 0.5),
             "bucket_norm": bucket_norms.get(c, 0.5), "vec": cat_vecs[c]}
            for c in ranked[:_FALLBACK_ROWS]
        ]

    # Assign each JD phrase to its nearest category; collect emergent leftovers.
    cat_sims: dict[str, list[float]] = {c: [] for c in cat_names}
    emergent: list[tuple[str, np.ndarray]] = []
    for i in range(len(phrase_vecs)):
        vec = phrase_vecs[i]
        best_c = max(cat_names, key=lambda c: cosine_sim(vec, cat_vecs[c]))
        best_sim = cosine_sim(vec, cat_vecs[best_c])
        if best_sim < _EMERGENT_THRESHOLD:
            if _is_skill_like(phrases[i]):
                emergent.append((phrases[i], vec))
        else:
            cat_sims[best_c].append(best_sim)

    jd_ask = {c: aggregate_sim(cat_sims[c]) for c in cat_names}
    base = [c for c in cat_names if jd_ask[c] >= _BASE_THRESHOLD]
    if not base:  # JD had signal but nothing cleared the bar — keep the top demands
        base = sorted(cat_names, key=lambda c: jd_ask[c], reverse=True)[:_MIN_ROWS]
    else:  # strongest demand first, capped so the heatmap stays readable
        base = sorted(base, key=lambda c: jd_ask[c], reverse=True)[:_MAX_ROWS]

    rows = [
        {"name": c, "jd_ask": jd_ask[c], "bucket_norm": bucket_norms.get(c, 0.5), "vec": cat_vecs[c]}
        for c in base
    ]

    # Emergent rows fill the remaining slots (deduped, capped). Their demand is
    # calibrated to the base categories' median so a genuine off-taxonomy skill sits
    # in line with real demand instead of automatically dominating the gap ranking.
    base_asks = sorted(jd_ask[c] for c in base)
    emergent_ask = base_asks[len(base_asks) // 2] if base_asks else _EMERGENT_FALLBACK_ASK
    slots = min(_MAX_ROWS - len(rows), _MAX_EMERGENT)
    if slots > 0 and emergent:
        seen: set[str] = set()
        existing = {r["name"].lower() for r in rows}
        for phrase, vec in emergent:
            key = phrase.lower()
            if key in seen or key in existing:
                continue
            seen.add(key)
            rows.append({
                "name": _short_label(phrase),
                "jd_ask": emergent_ask,
                "bucket_norm": _EMERGENT_NEUTRAL_NORM,
                "vec": vec,
            })
            slots -= 1
            if slots <= 0:
                break

    return rows
# -------------------- build_rows ------------- END ----------------
