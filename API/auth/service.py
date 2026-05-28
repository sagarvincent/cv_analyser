from asyncpg import Pool

from auth import queries
from security import verify_password
from user_profile.models import ProfileResponse
from user_profile.service import get_profile


# -------------------- verify_user ----------- START ----------
# -- Calls : queries.fetch_user_for_auth, user_profile.service.get_profile
# -- Called by: interface.verify_endpoint
async def verify_user(pool: Pool, username: str, password_hash: str) -> ProfileResponse | None:
    async with pool.acquire() as conn:
        row = await queries.fetch_user_for_auth(conn, username)
    if row is None:
        return None
    if not verify_password(password_hash, row["password_hash"]):
        return None
    return await get_profile(pool, username)
# -------------------- verify_user ------------- END ----------------
