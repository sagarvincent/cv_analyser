from fastapi import APIRouter, File, HTTPException, UploadFile

from BES01_cv_parser.extractors import supported_extensions
from BES01_cv_parser.models import ParsedCV
from BES01_cv_parser.parser import parse_cv

router = APIRouter(prefix="/cv", tags=["cv_parser"])


# -------------------- _extension_of ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: parse_endpoint
def _extension_of(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
# -------------------- _extension_of ------------- END ----------------


# -------------------- parse_endpoint ----------- START ----------
# -- Calls : _extension_of, supported_extensions, parse_cv
# -- Called by: FastAPI POST /cv/parse
@router.post("/parse", response_model=ParsedCV)
async def parse_endpoint(file: UploadFile = File(...)):
    filename = file.filename or ""
    ext = _extension_of(filename)
    if ext not in supported_extensions():
        allowed = ", ".join(supported_extensions())
        raise HTTPException(status_code=415, detail=f"Unsupported file type '.{ext or '?'}'. Allowed: {allowed}.")

    file_bytes = await file.read()
    parsed = parse_cv(file_bytes, filename)
    if parsed.extraction_method == "failed":
        raise HTTPException(status_code=422, detail="Could not extract any text from the file.")
    return parsed
# -------------------- parse_endpoint ------------- END ----------------
