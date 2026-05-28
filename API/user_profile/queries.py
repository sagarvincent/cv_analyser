from datetime import date

from asyncpg import Connection, Record


# -------------------- fetch_user_by_username ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.get_profile, service.create_profile
async def fetch_user_by_username(conn: Connection, username: str) -> Record | None:
    return await conn.fetchrow(
        "SELECT id, username, email, full_name, date_of_birth, location FROM users WHERE username = $1",
        username,
    )
# -------------------- fetch_user_by_username ------------- END ----------------


# -------------------- fetch_qualifications ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.get_profile
async def fetch_qualifications(conn: Connection, user_id: int) -> list[Record]:
    return await conn.fetch(
        """
        SELECT type, institution_name, degree_name, course_name,
               start_date, end_date, marks
        FROM qualifications
        WHERE user_id = $1
        ORDER BY start_date DESC
        """,
        user_id,
    )
# -------------------- fetch_qualifications ------------- END ----------------


# -------------------- fetch_experience ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.get_profile
async def fetch_experience(conn: Connection, user_id: int) -> list[Record]:
    return await conn.fetch(
        """
        SELECT job_title, company, salary, joining_date, leaving_date
        FROM experience
        WHERE user_id = $1
        ORDER BY joining_date DESC
        """,
        user_id,
    )
# -------------------- fetch_experience ------------- END ----------------


# -------------------- fetch_aspirations ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.get_profile
async def fetch_aspirations(conn: Connection, user_id: int) -> list[Record]:
    return await conn.fetch(
        """
        SELECT desired_role, desired_salary, active
        FROM aspirations
        WHERE user_id = $1
        ORDER BY created_at DESC
        """,
        user_id,
    )
# -------------------- fetch_aspirations ------------- END ----------------


# -------------------- fetch_projects ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.get_profile
async def fetch_projects(conn: Connection, user_id: int) -> list[Record]:
    return await conn.fetch(
        """
        SELECT name, domain, fun_description, techstack_description,
               start_date, end_date, deployed, source_type
        FROM projects
        WHERE user_id = $1
        ORDER BY start_date DESC NULLS LAST
        """,
        user_id,
    )
# -------------------- fetch_projects ------------- END ----------------


# -------------------- insert_user ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.create_profile
async def insert_user(
    conn: Connection,
    username: str,
    email: str,
    password_hash: str,
    full_name: str,
    date_of_birth: date,
    location: str | None,
) -> int:
    return await conn.fetchval(
        """
        INSERT INTO users (username, email, password_hash, full_name, date_of_birth, location)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id
        """,
        username,
        email,
        password_hash,
        full_name,
        date_of_birth,
        location,
    )
# -------------------- insert_user ------------- END ----------------


# -------------------- insert_cv_upload ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: service.create_profile
async def insert_cv_upload(
    conn: Connection,
    user_id: int,
    storage_path: str,
    original_filename: str,
    file_size_bytes: int,
    mime_type: str,
) -> int:
    return await conn.fetchval(
        """
        INSERT INTO cv_uploads (user_id, storage_path, original_filename, file_size_bytes, mime_type, status)
        VALUES ($1, $2, $3, $4, $5, 'pending')
        RETURNING id
        """,
        user_id,
        storage_path,
        original_filename,
        file_size_bytes,
        mime_type,
    )
# -------------------- insert_cv_upload ------------- END ----------------
