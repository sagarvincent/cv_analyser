from cv_jd_scorer.engine_base import ScorerEngine
from cv_jd_scorer.models import ScoreResult


class V2MlEngine(ScorerEngine):
    engine_version = "v2_ml"

    def compute(self, parsed_cv: dict, jd_text: str) -> ScoreResult:
        raise NotImplementedError("v2_ml engine is not yet implemented")


engine = V2MlEngine()
