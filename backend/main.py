from fastapi import FastAPI

from cv_jd_scorer.interface import router as cv_jd_scorer_router
from BES01_cv_parser.interface import router as cv_parser_router
from BES02_jd_parser.interface import router as jd_parser_router

app = FastAPI(title="CV Analyser — Analyser Service")
app.include_router(cv_parser_router)
app.include_router(cv_jd_scorer_router)
app.include_router(jd_parser_router)
