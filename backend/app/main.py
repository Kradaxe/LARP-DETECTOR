from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes.analyze import router as analyze_router
from app.api.v1.routes.github import router as github_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.resume import router as resume_router
from app.api.v1.routes.report import router as report_router
from app.api.v1.routes.embeddings import router as embeddings_router
from app.api.v1.routes.feedback import router as feedback_router
from app.api.v1.routes.linkedin_post import router as linkedin_post_router

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
    feedback_router,
    prefix="/api/v1/feedback",
    tags=["feedback"]
)

app.include_router(
    resume_router,
    prefix="/api/v1/resume",
    tags=["resume"]
)

app.include_router(
    report_router,
    prefix="/api/v1/report",
    tags=["report"]
)

app.include_router(
    embeddings_router,
    prefix="/api/v1/embeddings",
    tags=["embeddings"]
)

app.include_router(
    analyze_router,
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

app.include_router(
    linkedin_post_router,
    prefix="/api/v1/linkedin-post",
    tags=["linkedin-post"]
)

@app.get("/")
async def root():
    return {
        "message": "LARP Detector API running"
    }
