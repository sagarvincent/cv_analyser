import os

import httpx


_DEFAULT_TIMEOUT = 30.0


# -------------------- _analyser_url ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: parse_cv
def _analyser_url() -> str:
    return os.environ.get("ANALYSER_URL", "http://analyser:8002").rstrip("/")
# -------------------- _analyser_url ------------- END ----------------


# -------------------- parse_cv ----------- START ----------
# -- Calls : _analyser_url
# -- Called by: user_profile.service.create_profile
async def parse_cv(file_bytes: bytes, filename: str, content_type: str) -> dict:
    files = {"file": (filename, file_bytes, content_type)}
    async with httpx.AsyncClient(timeout=_DEFAULT_TIMEOUT) as client:
        response = await client.post(f"{_analyser_url()}/cv/parse", files=files)
        response.raise_for_status()
        return response.json()
# -------------------- parse_cv ------------- END ----------------
