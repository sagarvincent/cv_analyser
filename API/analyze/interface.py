from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from analyze.service import run_analysis

router = APIRouter(prefix="/analyze", tags=["analyze"])

_ALLOWED_MIME = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}
_MAX_BYTES = 16 * 1024 * 1024


# -------------------- analyze_endpoint ----------- START ----------
# -- Calls : run_analysis
# -- Called by: FastAPI POST /analyze
@router.post("")
async def analyze_endpoint(
    cv: UploadFile = File(...),
    jd: str = Form(default=""),
) -> dict:
    if cv.content_type not in _ALLOWED_MIME:
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {cv.content_type}")

    file_bytes = await cv.read()
    if len(file_bytes) > _MAX_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 16 MB limit.")

    return await run_analysis(file_bytes, cv.filename or "upload", cv.content_type or "", jd)
# -------------------- analyze_endpoint ------------- END ----------------
