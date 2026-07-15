from app.services.llm_service import generate


async def generate_questions(
    claim: str,
    technologies: list[str]
):
    prompt = f"""
Generate 5 technical interview questions.

Claim:
{claim}

Technologies:
{technologies}

Return JSON array only.
"""

    return await generate(prompt)