from cv_jd_scorer.engine_base import ScorerEngine
from cv_jd_scorer.engines.v1_tfidf import scorer
from cv_jd_scorer.models import ScoreResult


class V1TfidfEngine(ScorerEngine):
    engine_version = "v1_tfidf"

    def compute(self, parsed_cv: dict, jd_text: str) -> ScoreResult:
        return scorer.compute(parsed_cv, jd_text)


engine = V1TfidfEngine()
