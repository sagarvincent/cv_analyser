import logging
import os
import uuid
from datetime import date
from pathlib import Path

import asyncpg
import httpx
from asyncpg import Pool
from fastapi import UploadFile
from security import hash_password

from clients import analyser_client
from user_profile import queries
from user_profile.models import (
    AspirationOut,
    ExperienceOut,
    ProfileResponse,
    ProjectOut,
    QualificationOut,
)

logger = logging.getLogger(__name__)

_ALLOWED_MIME = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "text/plain": "txt",
}


# -------------------- _compute_age ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: _build_profile
def _compute_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
# -------------------- _compute_age ------------- END ----------------


# -------------------- _build_profile ----------- START ----------
# -- Calls : _compute_age
# -- Called by: get_profile, create_profile
def _build_profile(user_row, quals, exps, asps, projs) -> ProfileResponse:
    return ProfileResponse(
        username=user_row["username"],
        full_name=user_row["full_name"],
        email=user_row["email"],
        age=_compute_age(user_row["date_of_birth"]),
        location=user_row["location"],
        qualifications=[QualificationOut(**dict(r)) for r in quals],
        experience=[ExperienceOut(**dict(r)) for r in exps],
        aspirations=[AspirationOut(**dict(r)) for r in asps],
        projects=[ProjectOut(**dict(r)) for r in projs],
    )
# -------------------- _build_profile ------------- END ----------------


# -------------------- get_profile ----------- START ----------
# -- Calls : queries.fetch_user_by_username, queries.fetch_qualifications,
#            queries.fetch_experience, queries.fetch_aspirations,
#            queries.fetch_projects, _build_profile
# -- Called by: interface.get_profile_endpoint, service.create_profile
async def get_profile(pool: Pool, username: str) -> ProfileResponse | None:
    async with pool.acquire() as conn:
        user_row = await queries.fetch_user_by_username(conn, username)
        if user_row is None:
            return None
        uid = user_row["id"]
        quals = await queries.fetch_qualifications(conn, uid)
        exps  = await queries.fetch_experience(conn, uid)
        asps  = await queries.fetch_aspirations(conn, uid)
        projs = await queries.fetch_projects(conn, uid)
    return _build_profile(user_row, quals, exps, asps, projs)
# -------------------- get_profile ------------- END ----------------


# -------------------- _save_cv_to_disk ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: create_profile
def _save_cv_to_disk(cv: UploadFile, file_bytes: bytes, username: str) -> tuple[str, int, str]:
    upload_dir = Path(os.environ.get("CV_UPLOAD_DIR", "cv_uploads"))
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = _ALLOWED_MIME.get(cv.content_type or "", "bin")
    filename = f"{username}_{uuid.uuid4().hex}.{ext}"
    dest = upload_dir / filename
    dest.write_bytes(file_bytes)

    return str(dest), len(file_bytes), cv.content_type or "application/octet-stream"
# -------------------- _save_cv_to_disk ------------- END ----------------


# -------------------- _try_parse_cv ----------- START ----------
# -- Calls : analyser_client.parse_cv
# -- Called by: create_profile
async def _try_parse_cv(file_bytes: bytes, filename: str, content_type: str) -> dict | None:
    try:
        return await analyser_client.parse_cv(file_bytes, filename, content_type)
    except httpx.HTTPError as exc:
        logger.warning("analyser parse failed for %s: %s", filename, exc)
        return None
# -------------------- _try_parse_cv ------------- END ----------------


# -------------------- create_profile ----------- START ----------
# -- Calls : _save_cv_to_disk, _try_parse_cv, queries.insert_user,
#            queries.insert_cv_upload, get_profile
# -- Called by: interface.create_profile_endpoint
async def create_profile(
    pool: Pool,
    username: str,
    email: str,
    password: str,
    full_name: str,
    date_of_birth: str,
    location: str | None,
    cv: UploadFile,
) -> ProfileResponse:
    file_bytes = await cv.read()
    storage_path, file_size, mime_type = _save_cv_to_disk(cv, file_bytes, username)
    parsed = await _try_parse_cv(file_bytes, cv.filename or "upload", mime_type)
    if parsed is not None:
        logger.info(
            "parsed CV for %s: method=%s sections=%s",
            username,
            parsed.get("extraction_method"),
            list((parsed.get("sections") or {}).keys()),
        )
    bcrypt_hash = hash_password(password)
    dob = date.fromisoformat(date_of_birth)

    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                user_id = await queries.insert_user(
                    conn, username, email, bcrypt_hash, full_name, dob, location
                )
                await queries.insert_cv_upload(
                    conn,
                    user_id,
                    storage_path,
                    cv.filename or "upload",
                    file_size,
                    mime_type,
                )
    except asyncpg.UniqueViolationError:
        raise ValueError("duplicate")

    return await get_profile(pool, username)
# -------------------- create_profile ------------- END ----------------
