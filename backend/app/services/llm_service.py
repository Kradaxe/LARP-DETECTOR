from google import genai
from app.config.settings import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


async def generate(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text