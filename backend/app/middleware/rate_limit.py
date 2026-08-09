from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.redis_service import RedisService

class RateLimitMiddleware:
    """Middleware for rate limiting API requests."""
    
    def __init__(self, app, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.app = app
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
    
    async def __call__(self, request: Request, call_next):
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check minute rate limit
        minute_key = f"rate_limit:minute:{client_ip}"
        minute_allowed, minute_remaining = RedisService.increment_rate_limit(
            minute_key, 
            self.requests_per_minute, 
            60  # 60 seconds
        )
        
        # Check hour rate limit
        hour_key = f"rate_limit:hour:{client_ip}"
        hour_allowed, hour_remaining = RedisService.increment_rate_limit(
            hour_key,
            self.requests_per_hour,
            3600  # 1 hour
        )
        
        # Check if limits exceeded before processing
        if not minute_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Minute rate limit of {self.requests_per_minute} requests exceeded",
                    "retry_after": 60
                },
                headers={"Retry-After": "60"}
            )
        
        if not hour_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Hourly rate limit of {self.requests_per_hour} requests exceeded",
                    "retry_after": 3600
                },
                headers={"Retry-After": "3600"}
            )
        
        # Process request
        response = await call_next(request)
        
        # Set rate limit headers
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(minute_remaining)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(hour_remaining)
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check for forwarded headers (proxy/load balancer)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct connection
        if request.client:
            return request.client.host
        
        return "unknown"