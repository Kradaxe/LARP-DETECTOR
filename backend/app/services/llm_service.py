from google import genai

from app.core.config import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


async def evaluate_text(
    text: str,
    signals: dict
):
    prompt = f"""
    You are a senior staff engineer interviewing a candidate.
    
    Your task is to determine whether a technical claim sounds genuine,
    experienced, and implementation-backed or whether it sounds vague,
    buzzword-heavy, or superficial.
    
    Claim:
    {text}
    
    Objective Signals:
    {signals}
    
    Score the following from 0-10:
    
    1. Specificity
    2. Technical Depth
    3. Evidence
    4. Implementation Detail
    
    Definitions:
    
    Specificity:
    How concrete is the statement?
    
    Technical Depth:
    Does the author appear to understand the underlying systems?
    
    Evidence:
    Are numbers, measurements, tradeoffs, or outcomes provided?
    
    Implementation Detail:
    Does the author explain HOW they built something?
    
    Return ONLY valid JSON:
    
    {{
        "specificity": 0,
        "technical_depth": 0,
        "evidence": 0,
        "implementation_detail": 0,
        "reasoning": ""
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text