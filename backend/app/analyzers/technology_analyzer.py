# app/analyzers/technology_analyzer.py

from typing import Dict, List


TECHNOLOGIES = {
    "redis",
    "kafka",
    "postgresql",
    "mongodb",
    "docker",
    "kubernetes",
    "react",
    "nextjs",
    "next.js",
    "node",
    "nodejs",
    "express",
    "typescript",
    "python",
    "fastapi",
    "pytorch",
    "tensorflow",
    "qdrant",
    "aws",
    "gcp"
}


def analyze_technologies(text: str) -> Dict:
    text_lower = text.lower()

    found: List[str] = []

    for tech in TECHNOLOGIES:
        if tech in text_lower:
            found.append(tech)

    return {
        "technology_count": len(found),
        "technologies_found": found
    }