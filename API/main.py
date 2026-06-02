import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI

from analyze.interface import router as analyze_router
from auth.interface import router as auth_router
from user_profile.interface import router as user_profile_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 5432)),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        min_size=2,
        max_size=10,
    )
    yield
    await app.state.pool.close()


app = FastAPI(title="CV Analyser — User Profile API", lifespan=lifespan)
app.include_router(auth_router, prefix="/api")
app.include_router(user_profile_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
