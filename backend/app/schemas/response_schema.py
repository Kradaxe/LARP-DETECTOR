from pydantic import BaseModel
from typing import List


class AnalyzeResponse(BaseModel):
    credibility_score: int
    verdict: str

    specificity: int
    technical_depth: int
    evidence: int
    implementation_detail: int

    technologies_found: List[str]

    strengths: List[str]
    weaknesses: List[str]

    interview_questions: List[str]

    reasoning: str