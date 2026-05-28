from fastapi import APIRouter, Depends, HTTPException, Request

from auth import service
from auth.models import VerifyRequest
from user_profile.models import ProfileResponse

router = APIRouter(prefix="/auth", tags=["auth"])


# -------------------- _get_pool ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: verify_endpoint
def _get_pool(request: Request):
    return request.app.state.pool
# -------------------- _get_pool ------------- END ----------------


# -------------------- verify_endpoint ----------- START ----------
# -- Calls : service.verify_user
# -- Called by: FastAPI POST /api/auth/verify
@router.post("/verify", response_model=ProfileResponse)
async def verify_endpoint(body: VerifyRequest, pool=Depends(_get_pool)):
    profile = await service.verify_user(pool, body.username, body.password_hash)
    if profile is None:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    return profile
# -------------------- verify_endpoint ------------- END ----------------
