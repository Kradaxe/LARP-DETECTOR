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

# Add rate limiting middleware (60 requests/minute, 1000 requests/hour)
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    from app.services.redis_service import RedisService
    from fastapi.responses import JSONResponse
    
    # Get client IP
    client_ip = request.headers.get("X-Forwarded-For", 
                  request.headers.get("X-Real-IP", 
                  request.client.host if request.client else "unknown"))
    
    if isinstance(client_ip, list):
        client_ip = client_ip[0]
    
    # Check minute rate limit
    minute_key = f"rate_limit:minute:{client_ip}"
    minute_allowed, minute_remaining = RedisService.increment_rate_limit(
        minute_key, 60, 60
    )
    
    # Check hour rate limit
    hour_key = f"rate_limit:hour:{client_ip}"
    hour_allowed, hour_remaining = RedisService.increment_rate_limit(
        hour_key, 1000, 3600
    )
    
    # Check if limits exceeded
    if not minute_allowed:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "message": "Minute rate limit exceeded"},
            headers={"Retry-After": "60"}
        )
    
    if not hour_allowed:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "message": "Hourly rate limit exceeded"},
            headers={"Retry-After": "3600"}
        )
    
    # Process request
    response = await call_next(request)
    
    # Set rate limit headers
    response.headers["X-RateLimit-Limit-Minute"] = "60"
    response.headers["X-RateLimit-Remaining-Minute"] = str(minute_remaining)
    response.headers["X-RateLimit-Limit-Hour"] = "1000"
    response.headers["X-RateLimit-Remaining-Hour"] = str(hour_remaining)
    
    return response

# Add CORS middleware
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
