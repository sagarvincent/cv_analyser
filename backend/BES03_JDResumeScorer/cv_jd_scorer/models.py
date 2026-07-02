from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ── Shared ─────────────────────────────────────────────────────────────────

class ReasoningStep(BaseModel):
    stage: str
    text: str


# ── JD Fit ─────────────────────────────────────────────────────────────────

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


# ── ATS ────────────────────────────────────────────────────────────────────

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


# ── Request / Response ─────────────────────────────────────────────────────

class ScoreRequest(BaseModel):
    parsed_cv: dict
    jd_text: str


class ScoreResult(BaseModel):
    engine_version: str = "unknown"

    # Reasoning trace
    reasoningTrace: list[ReasoningStep]

    # JD Fit
    jdFitSummary: JdFitSummary
    jdFitMatches: list[JdFitMatch]
    jdFitGaps: list[JdFitGap]

    # ATS
    atsSummary: AtsSummary
    atsChecks: list[AtsCheck]

    # Peer Benchmark
    peerSummary: dict
    peerBuckets: list[int]
    peerYouBucket: int
    peerP50Bucket: int
    peerDimensions: list[dict]

    # Compensation
    compSummary: dict
    compBandData: dict
    compRefCards: list[dict]

    # Alternative Paths
    altPathsSummary: dict
    altPathsCenter: dict
    altPathsNodes: list[dict]
    altPathsLinks: list[dict]
    altPathsInsight: dict

    # Market Trends (disabled — static not-available response)
    trendsSummary: dict
    trendRising: list[dict]
    trendFalling: list[dict]
    trendsInsight: dict

    # Market Alignment
    alignSummary: dict
    alignAxes: list[str]
    alignYou: list[float]
    alignMarket: list[float]

    # Overview (assembled last)
    overviewCards: list[dict]
    overviewSummary: dict
    overviewRecommendations: list[dict]
    overviewInsight: dict
    overviewMarketData: dict
    overviewVectorSignature: dict
