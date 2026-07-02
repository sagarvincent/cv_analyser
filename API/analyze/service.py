import asyncio
import logging

import httpx

from clients import analyser_client, scorer_client, skill_matrix_client

logger = logging.getLogger(__name__)


# -------------------- _safe_score ----------- START ----------
# -- Calls : scorer_client.score_cv_jd
# -- Called by: run_analysis
async def _safe_score(parsed_cv: dict, jd_text: str) -> dict:
    try:
        return await scorer_client.score_cv_jd(parsed_cv, jd_text)
    except httpx.HTTPError as exc:
        logger.warning("scorer failed: %s", exc)
        return {}
# -------------------- _safe_score ------------- END ----------------


# -------------------- _safe_skill_matrix ----------- START ----------
# -- Calls : skill_matrix_client.score_skill_matrix
# -- Called by: run_analysis
async def _safe_skill_matrix(parsed_cv: dict, jd_text: str) -> dict:
    try:
        return await skill_matrix_client.score_skill_matrix(parsed_cv, jd_text)
    except httpx.HTTPError as exc:
        logger.warning("skill matrix failed: %s", exc)
        return {}
# -------------------- _safe_skill_matrix ------------- END ----------------


# -------------------- run_analysis ----------- START ----------
# -- Calls : analyser_client.parse_cv, _safe_score, _safe_skill_matrix
# -- Called by: interface.analyze_endpoint
async def run_analysis(
    file_bytes: bytes,
    filename: str,
    content_type: str,
    jd_text: str,
) -> dict:
    parsed_cv = await analyser_client.parse_cv(file_bytes, filename, content_type)
    logger.info(
        "CV parsed: method=%s sections=%s",
        parsed_cv.get("extraction_method"),
        list((parsed_cv.get("sections") or {}).keys()),
    )

    # BES03 scorer (7 lenses) and BES04 skill matrix run concurrently; either may
    # degrade to {} without sinking the whole analysis.
    score_result, skill_matrix_result = await asyncio.gather(
        _safe_score(parsed_cv, jd_text),
        _safe_skill_matrix(parsed_cv, jd_text),
    )

    return {**parsed_cv, **score_result, **skill_matrix_result}
# -------------------- run_analysis ------------- END ----------------
