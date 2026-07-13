from app.services.llm_service import evaluate_text
from app.services.signal_extractor import extract_signals
from app.services.scoring_service import calculate_score
from app.services.verdict_service import get_verdict

from app.utils.json_parser import parse_llm_json


async def analyze_text(text: str):
    signals = extract_signals(text)

    llm_result = await evaluate_text(
        text=text,
        signals=signals
    )

    parsed = parse_llm_json(llm_result)

    score = calculate_score(
        specificity=parsed["specificity"],
        technical_depth=parsed["technical_depth"],
        evidence=parsed["evidence"],
        implementation_detail=parsed["implementation_detail"],
        signals=signals
    )

    verdict = get_verdict(score)

    return {
        "credibility_score": score,
        "verdict": verdict,

        "specificity": parsed["specificity"],
        "technical_depth": parsed["technical_depth"],
        "evidence": parsed["evidence"],
        "implementation_detail": parsed["implementation_detail"],

        "technologies_found": signals["technologies_found"],

        "reasoning": parsed["reasoning"]
    }