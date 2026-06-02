from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from user_profile import service
from user_profile.models import ProfileResponse

router = APIRouter(prefix="/profile", tags=["user_profile"])


# -------------------- _get_pool ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: get_profile_endpoint, create_profile_endpoint
def _get_pool(request: Request):
    return request.app.state.pool
# -------------------- _get_pool ------------- END ----------------


# -------------------- get_profile_endpoint ----------- START ----------
# -- Calls : service.get_profile
# -- Called by: FastAPI GET /api/profile/{username}
@router.get("/{username}", response_model=ProfileResponse)
async def get_profile_endpoint(username: str, pool=Depends(_get_pool)):
    profile = await service.get_profile(pool, username)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found.")
    return profile
# -------------------- get_profile_endpoint ------------- END ----------------


# -------------------- create_profile_endpoint ----------- START ----------
# -- Calls : service.create_profile
# -- Called by: FastAPI POST /api/profile
@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile_endpoint(
    pool=Depends(_get_pool),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    date_of_birth: str = Form(..., description="YYYY-MM-DD"),
    location: str | None = Form(default=None),
    cv: UploadFile = File(...),
):
    try:
        profile = await service.create_profile(
            pool, username, email, password, full_name, date_of_birth, location, cv
        )
    except ValueError as exc:
        if str(exc) == "duplicate":
            raise HTTPException(status_code=409, detail="Username or email already exists.")
        raise
    return profile
# -------------------- create_profile_endpoint ------------- END ----------------
