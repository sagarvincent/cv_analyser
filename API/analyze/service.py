import logging

import httpx

from clients import analyser_client, scorer_client

logger = logging.getLogger(__name__)


# -------------------- run_analysis ----------- START ----------
# -- Calls : analyser_client.parse_cv, scorer_client.score_cv_jd
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

    try:
        score_result = await scorer_client.score_cv_jd(parsed_cv, jd_text)
    except httpx.HTTPError as exc:
        logger.warning("scorer failed: %s", exc)
        score_result = {}

    return {**parsed_cv, **score_result}
# -------------------- run_analysis ------------- END ----------------
