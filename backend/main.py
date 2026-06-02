from fastapi import FastAPI

from cv_parser.interface import router as cv_parser_router

app = FastAPI(title="CV Analyser — Analyser Service")
app.include_router(cv_parser_router)
