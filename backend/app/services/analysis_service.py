from app.services.llm_service import generate
from app.services.signal_extractor import extract_signals
from app.services.scoring_service import calculate_score
from app.services.verdict_service import verdict as get_verdict
from app.services.interview_service import generate_questions
from app.services.persistence_service import save_analysis

from app.utils.json_parser import parse_llm_json


async def analyze_text(text: str):
    signals = extract_signals(text)

    prompt = f"""Analyze this text for technical credibility and return ONLY a JSON object with the following keys:
- specificity (number 1-10)
- technical_depth (number 1-10)
- evidence (number 1-10)
- implementation_detail (number 1-10)
- reasoning (string)

Text: {text}
Signals: {signals}

Return ONLY the JSON, no other text."""

    llm_result = await generate(prompt)
    parsed = parse_llm_json(llm_result)

    score = calculate_score(
        specificity=parsed["specificity"],
        technical_depth=parsed["technical_depth"],
        evidence=parsed["evidence"],
        implementation_detail=parsed["implementation_detail"],
        technology_count=len(signals["technologies"]["technologies_found"]),
        metrics_count=signals["metrics"]["metrics_count"],
        architecture_count=signals["architecture"]["count"]
    )

    questions = await generate_questions(
        text,
        signals["technologies"]["technologies_found"]
    )

    verdict = get_verdict(score)

    result = {
        "credibility_score": score,
        "verdict": verdict,

        "specificity": parsed["specificity"],
        "technical_depth": parsed["technical_depth"],
        "evidence": parsed["evidence"],
        "implementation_detail": parsed["implementation_detail"],

        "technologies_found": signals["technologies"]["technologies_found"],

        "reasoning": parsed["reasoning"],
        "interview_questions": parse_llm_json(questions),
        "strengths": [],
        "weaknesses": []
    }

    analysis_id = save_analysis(
        text=text,
        score=score,
        verdict=verdict,
        technologies=signals["technologies"]["technologies_found"],
        reasoning=parsed["reasoning"],
    )
    
    result["analysis_id"] = analysis_id

    return result
