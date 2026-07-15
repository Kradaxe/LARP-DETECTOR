from pydantic import BaseModel
from typing import List


class GithubAnalysisResponse(BaseModel):
    credibility_score: int
    verdict: str

    repo_count: int
    stars: int
    forks: int

    languages: List[str]

    strengths: List[str]
    weaknesses: List[str]

    reasoning: str