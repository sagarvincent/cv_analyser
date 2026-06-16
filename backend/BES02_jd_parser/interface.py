from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from BES02_jd_parser.extractor import dispatch_file
from BES02_jd_parser.models import ParsedJD
from BES02_jd_parser.parser import parse_jd

router = APIRouter(prefix="/jd", tags=["jd_parser"])


# -------------------- parse_jd_endpoint ----------- START ----------
# -- Calls : dispatch_file, parse_jd
# -- Called by: FastAPI POST /jd/parse
@router.post("/parse")
async def parse_jd_endpoint(
    jd: str | None = Form(None),
    jd_file: UploadFile | None = File(None),
) -> dict:
    if jd_file is not None:
        file_bytes = await jd_file.read()
        text = dispatch_file(file_bytes, jd_file.filename or "")
        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail=f"Could not extract text from '{jd_file.filename}'. Supported formats: PDF, DOC, DOCX, JSON, CSV.",
            )
    elif jd and jd.strip():
        text = jd
    else:
        raise HTTPException(
            status_code=422,
            detail="Either jd (text) or jd_file must be provided.",
        )

    result: ParsedJD = parse_jd(text)
    return result.model_dump(mode="json")
# -------------------- parse_jd_endpoint ------------- END ----------------
