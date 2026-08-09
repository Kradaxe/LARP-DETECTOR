try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("Redis module not available - caching and rate limiting will be disabled")

import json
import hashlib
from typing import Optional, Any, Tuple
from app.config.settings import settings

class RedisService:
    """Service for Redis operations including caching and rate limiting."""
    
    _client = None
    
    @classmethod
    def get_client(cls) -> redis.Redis:
        """Get or create Redis client singleton."""
        if not REDIS_AVAILABLE:
            return None
        if cls._client is None:
            cls._client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5
            )
        return cls._client
    
    @classmethod
    def cache_get(cls, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not REDIS_AVAILABLE:
            return None
        try:
            client = cls.get_client()
            if client is None:
                return None
            value = client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis cache get error: {e}")
            return None
    
    @classmethod
    def cache_set(cls, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL in seconds."""
        if not REDIS_AVAILABLE:
            return False
        try:
            client = cls.get_client()
            if client is None:
                return False
            serialized = json.dumps(value)
            return client.setex(key, ttl, serialized)
        except Exception as e:
            print(f"Redis cache set error: {e}")
            return False
    
    @classmethod
    def cache_delete(cls, key: str) -> bool:
        """Delete key from cache."""
        if not REDIS_AVAILABLE:
            return False
        try:
            client = cls.get_client()
            if client is None:
                return False
            return client.delete(key) > 0
        except Exception as e:
            print(f"Redis cache delete error: {e}")
            return False
    
    @classmethod
    def increment_rate_limit(cls, key: str, limit: int, window: int) -> Tuple[bool, int]:
        """
        Check and increment rate limit.
        
        Args:
            key: Rate limit key (e.g., "ip:127.0.0.1" or "user:123")
            limit: Maximum requests allowed
            window: Time window in seconds
            
        Returns:
            Tuple of (allowed: bool, remaining: int)
        """
        if not REDIS_AVAILABLE:
            # Fail open - allow request if Redis is not available
            return True, limit
        try:
            client = cls.get_client()
            if client is None:
                return True, limit
            current = client.incr(key)
            
            if current == 1:
                # First request, set expiration
                client.expire(key, window)
            
            allowed = current <= limit
            remaining = max(0, limit - current)
            
            return allowed, remaining
        except Exception as e:
            print(f"Redis rate limit error: {e}")
            # Fail open - allow request if Redis is down
            return True, limit
    
    @classmethod
    def get_rate_limit_info(cls, key: str) -> dict:
        """Get current rate limit info for a key."""
        if not REDIS_AVAILABLE:
            return {"current": 0, "ttl": 0}
        try:
            client = cls.get_client()
            if client is None:
                return {"current": 0, "ttl": 0}
            current = int(client.get(key) or 0)
            ttl = client.ttl(key)
            return {
                "current": current,
                "ttl": ttl if ttl > 0 else 0
            }
        except Exception as e:
            print(f"Redis get rate limit info error: {e}")
            return {"current": 0, "ttl": 0}
    
    @staticmethod
    def hash_text(text: str) -> str:
        """Generate hash for text to use as cache key."""
        return hashlib.sha256(text.encode()).hexdigest()
