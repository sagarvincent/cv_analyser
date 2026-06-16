from abc import ABC, abstractmethod

from cv_jd_scorer.models import ScoreResult


class ScorerEngine(ABC):

    @property
    @abstractmethod
    def engine_version(self) -> str:
        """Stamped onto every ScoreResult so stored scores are traceable to their engine."""
        ...

    @abstractmethod
    def compute(self, parsed_cv: dict, jd_text: str) -> ScoreResult: ...
