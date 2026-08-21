from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware:
    """Middleware for rate limiting API requests (disabled without Redis)."""
    
    def __init__(self, app, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.app = app
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
    
    async def __call__(self, request: Request, call_next):
        # Rate limiting disabled - pass through all requests
        response = await call_next(request)
        return response