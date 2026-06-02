from fastapi import APIRouter, HTTPException

from cv_jd_scorer.models import ScoreRequest, ScoreResult
from cv_jd_scorer.scorer import compute

router = APIRouter(prefix="/cv", tags=["cv_jd_scorer"])


# -------------------- score_endpoint ----------- START ----------
# -- Calls : compute
# -- Called by: FastAPI POST /cv/score
@router.post("/score")
async def score_endpoint(body: ScoreRequest) -> dict:
    if not body.parsed_cv:
        raise HTTPException(status_code=422, detail="parsed_cv must not be empty.")
    result: ScoreResult = compute(body.parsed_cv, body.jd_text)
    # Serialize by alias so AtsCheck.pass_ → "pass" in JSON output
    return result.model_dump(by_alias=True, mode="json")
# -------------------- score_endpoint ------------- END ----------------
