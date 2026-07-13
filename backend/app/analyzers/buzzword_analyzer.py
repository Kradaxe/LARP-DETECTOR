# app/analyzers/buzzword_analyzer.py

from typing import Dict, List


BUZZWORDS = {
    "scalable",
    "cutting-edge",
    "innovative",
    "robust",
    "enterprise-grade",
    "synergy",
    "synergistic",
    "ai-powered",
    "disruptive",
    "next-generation",
    "state-of-the-art",
    "modern",
    "high-performance",
    "world-class",
    "industry-leading",
    "transformative"
}


def analyze_buzzwords(text: str) -> Dict:
    """
    Analyze text for generic buzzword usage.
    """

    text_lower = text.lower()

    found_buzzwords: List[str] = []

    for buzzword in BUZZWORDS:
        if buzzword in text_lower:
            found_buzzwords.append(buzzword)

    score = min(len(found_buzzwords) * 2, 10)

    return {
        "buzzword_score": score,
        "buzzwords_found": found_buzzwords
    }