from google import genai
from app.config.settings import settings

_client = None

def _get_client() -> genai.Client:
    global _client
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is required to run text analysis")
    
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    return _client


async def generate(prompt: str):
    client = _get_client()
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text
