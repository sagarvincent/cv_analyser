from pydantic import BaseModel


# ── Request ────────────────────────────────────────────────────────────────

class ScoreRequest(BaseModel):
    parsed_cv: dict
    jd_text: str = ""


# ── Response ───────────────────────────────────────────────────────────────

class SkillMatrixSummary(BaseModel):
    eyebrow: str
    bucket: str
    overIndexTopic: str
    underIndexTopic: str
    sub: str


class SkillMatrixDeltaCard(BaseModel):
    label: str
    topic: str
    delta: str
    color: str
    note: str


class SkillMatrix(BaseModel):
    skillMatrixSummary: SkillMatrixSummary
    skillMatrixCategories: list[str]      # rows
    skillMatrixCohorts: list[str]         # columns
    skillMatrixData: list[list[float]]    # rows × cohorts, values in [0, 1]
    skillMatrixDeltaCards: list[SkillMatrixDeltaCard]
