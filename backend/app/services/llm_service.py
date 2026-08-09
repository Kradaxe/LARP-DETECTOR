from google import genai
from app.config.settings import settings
from app.services.redis_service import RedisService

_client = None

def _get_client() -> genai.Client:
    global _client
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is required to run text analysis")
    
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    return _client


async def generate(prompt: str):
    # Check cache first
    cache_key = f"llm_response:{RedisService.hash_text(prompt)}"
    cached_result = RedisService.cache_get(cache_key)
    
    if cached_result is not None:
        print("Cache hit for LLM prompt")
        return cached_result
    
    # Cache miss - call the API
    client = _get_client()
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    result = response.text
    
    # Cache the result with 24 hour TTL
    RedisService.cache_set(cache_key, result, ttl=86400)
    
    return result
