from app.services.llm_service import generate_json


async def extract_claims(text: str):
    prompt = f"""
Extract independent technical claims.

Return JSON:

[
    "claim1",
    "claim2"
]

Text:
{text}
"""

    return await generate_json(prompt)