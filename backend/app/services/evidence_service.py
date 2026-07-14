from app.services.llm_service import generate_json


async def expected_evidence(claim: str):
    prompt = f"""
What evidence would support this claim?

Claim:
{claim}

Return JSON.
"""

    return await generate_json(prompt)