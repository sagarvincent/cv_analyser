from fastapi import APIRouter, HTTPException

from BES04_SkillMatrix.builder import build_skill_matrix
from BES04_SkillMatrix.models import ScoreRequest, SkillMatrix

router = APIRouter(prefix="/skill-matrix", tags=["skill_matrix"])


# -------------------- score_endpoint ----------- START ----------
# -- Calls : build_skill_matrix
# -- Called by: FastAPI POST /skill-matrix/score
@router.post("/score")
async def score_endpoint(body: ScoreRequest) -> dict:
    if not body.parsed_cv:
        raise HTTPException(status_code=422, detail="parsed_cv must not be empty.")
    result: SkillMatrix = build_skill_matrix(body.parsed_cv, body.jd_text)
    return result.model_dump(mode="json")
# -------------------- score_endpoint ------------- END ----------------
