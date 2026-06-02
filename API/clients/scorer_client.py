import os

import httpx


_DEFAULT_TIMEOUT = 120.0


# -------------------- _analyser_url ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: score_cv_jd
def _analyser_url() -> str:
    return os.environ.get("ANALYSER_URL", "http://analyser:8002").rstrip("/")
# -------------------- _analyser_url ------------- END ----------------


# -------------------- score_cv_jd ----------- START ----------
# -- Calls : _analyser_url
# -- Called by: analyze.service.run_analysis
async def score_cv_jd(parsed_cv: dict, jd_text: str) -> dict:
    payload = {"parsed_cv": parsed_cv, "jd_text": jd_text}
    async with httpx.AsyncClient(timeout=_DEFAULT_TIMEOUT) as client:
        response = await client.post(f"{_analyser_url()}/cv/score", json=payload)
        response.raise_for_status()
        return response.json()
# -------------------- score_cv_jd ------------- END ----------------
