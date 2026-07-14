from app.services.llm_service import generate_json


async def consistency_check(text: str):
    prompt = f"""
Find contradictions or inconsistencies.

Return JSON.

Text:
{text}
"""

    return await generate_json(prompt)