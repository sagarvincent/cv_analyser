from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.upload_validation.file_validator import FileValidator

app = FastAPI()


@app.post("/api/validate")
async def validate_upload(file: UploadFile = File(...)):
    data = await file.read()
    valid, error = FileValidator().validate(file.filename or "", len(data))
    if not valid:
        return JSONResponse({"valid": False, "error": error}, status_code=422)
    return {"valid": True, "error": None}


# Serve the built React frontend — must be mounted last
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
