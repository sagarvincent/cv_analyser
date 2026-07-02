import re

# Pure text helpers — no embeddings, no I/O. Tokenisation + phrase extraction for
# both the JD (demand signal) and the CV (evidence signal).

# Split on bullets and list separators only — NOT hyphens, so compound skills
# like "hands-on" and "end-to-end" stay intact instead of fragmenting.
_SPLIT_RE = re.compile(r"[•·▪;,/|]+|\s{2,}|\n")
_LEAD_BULLET_RE = re.compile(r"^\s*(?:[•·▪\-–—*]|\d+[.)])\s*")
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z+#.]*")

# Low-signal header/filler lines to drop from JD phrase extraction.
_DROP_PHRASES = {
    "requirements", "responsibilities", "about the role", "about the company",
    "about us", "what you'll do", "what we offer", "qualifications", "preferred",
    "benefits", "overview", "the role", "nice to have", "must have",
}


# -------------------- clamp_unit ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: score_leaves, scorer, jd_categories
def clamp_unit(v: float) -> float:
    return max(0.0, min(1.0, v))
# -------------------- clamp_unit ------------- END ----------------


# -------------------- _clean_phrase ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: jd_phrases, resume_phrases
def _clean_phrase(raw: str) -> str:
    return _LEAD_BULLET_RE.sub("", raw).strip()
# -------------------- _clean_phrase ------------- END ----------------


# -------------------- jd_phrases ----------- START ----------
# -- Calls : _clean_phrase
# -- Called by: builder.build_skill_matrix
def jd_phrases(jd_text: str, cap: int = 40) -> list[str]:
    """Break a job description into candidate demand phrases (skills, clauses),
    dropping bullets, headers, and noise. Order-preserving, de-duplicated."""
    if not jd_text or not jd_text.strip():
        return []

    phrases: list[str] = []
    seen: set[str] = set()
    for line in jd_text.splitlines():
        for chunk in _SPLIT_RE.split(line):
            phrase = _clean_phrase(chunk)
            if len(phrase) < 3:
                continue
            low = phrase.lower()
            if low in _DROP_PHRASES or low in seen:
                continue
            if not _WORD_RE.search(phrase):  # purely numeric / symbols
                continue
            seen.add(low)
            phrases.append(phrase)
            if len(phrases) >= cap:
                return phrases
    return phrases
# -------------------- jd_phrases ------------- END ----------------


# -------------------- resume_phrases ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: builder.build_skill_matrix
def resume_phrases(sections: dict, cap: int = 40, words_per_exp: int = 50) -> list[str]:
    """Collect the resume's evidence phrases: each skills item, plus the first
    *words_per_exp* words of each experience description."""
    phrases: list[str] = []

    skills_block = sections.get("skills", {})
    if isinstance(skills_block, dict):
        for item in skills_block.get("items", []):
            item = str(item).strip()
            if item:
                phrases.append(item)
    elif isinstance(skills_block, str) and skills_block.strip():
        phrases.append(skills_block.strip())

    for exp in sections.get("experience", []) or []:
        if not isinstance(exp, dict):
            continue
        desc = str(exp.get("description", "")).strip()
        if desc:
            phrases.append(" ".join(desc.split()[:words_per_exp]))

    summary = sections.get("summary", "")
    if isinstance(summary, str) and summary.strip():
        phrases.append(" ".join(summary.split()[:words_per_exp]))

    return phrases[:cap]
# -------------------- resume_phrases ------------- END ----------------
