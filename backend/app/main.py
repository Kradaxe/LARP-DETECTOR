from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes.analyze import router as analyze_router
from app.api.v1.routes.github import router as github_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.github import router as github_router

app = FastAPI(
    title="LARP Detector API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    analyze_router,
    prefix="/api/v1"
)

app.include_router(
    github_router,
    prefix="/api/v1"
)

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    github_router,
    prefix="/api/v1/github",
    tags=["github"]
)

@app.get("/")
async def root():
    return {
        "message": "LARP Detector API running"
    }