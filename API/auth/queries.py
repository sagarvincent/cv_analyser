from asyncpg import Connection, Record


# -------------------- fetch_user_for_auth ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.verify_user
async def fetch_user_for_auth(conn: Connection, username: str) -> Record | None:
    return await conn.fetchrow(
        "SELECT id, username, password_hash FROM users WHERE username = $1",
        username,
    )
# -------------------- fetch_user_for_auth ------------- END ----------------
