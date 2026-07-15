from google import genai
from app.config.settings import settings

def _get_client() -> genai.Client:
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is required to run text analysis")

    return genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate(prompt: str):
    response = _get_client().models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text
