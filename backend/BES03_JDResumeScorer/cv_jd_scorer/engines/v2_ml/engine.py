from cv_jd_scorer.engine_base import ScorerEngine
from cv_jd_scorer.engines.v2_ml import scorer
from cv_jd_scorer.models import ScoreResult


class V2MlEngine(ScorerEngine):
    engine_version = "v2_ml"

    def compute(self, parsed_cv: dict, jd_text: str) -> ScoreResult:
        return scorer.compute(parsed_cv, jd_text)


engine = V2MlEngine()
