from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReasoningStep(BaseModel):
    stage: str
    text: str


class JdFitMatch(BaseModel):
    topic: str
    evidence: str
    strength: float


class JdFitGap(BaseModel):
    topic: str
    impact: Literal["HIGH", "MED", "LOW"]
    note: str


class JdFitSummary(BaseModel):
    eyebrow: str
    titleReach: str
    titleRest: str
    sub: str
    score: int
    evidencedMatches: int
    totalRequirements: int
    gapsFlagged: int
    gapBreakdown: str
    keywordDensity: int


class AtsCheck(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    label: str
    pass_: bool = Field(serialization_alias="pass")
    note: str


class AtsSummary(BaseModel):
    eyebrow: str
    titleScore: str
    titleRest: str
    sub: str
    score: int


class ScoreRequest(BaseModel):
    parsed_cv: dict
    jd_text: str


class ScoreResult(BaseModel):
    reasoningTrace: list[ReasoningStep]
    jdFitSummary: JdFitSummary
    jdFitMatches: list[JdFitMatch]
    jdFitGaps: list[JdFitGap]
    atsSummary: AtsSummary
    atsChecks: list[AtsCheck]
