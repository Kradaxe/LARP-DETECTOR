from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class AnalyzeResponse(BaseModel):
    analysis_id: Optional[int] = None
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


class ClaimAnalysis(BaseModel):
    claim: str
    credibility_score: int
    verdict: str
    reasoning: str


class ResumeAnalysisResponse(BaseModel):
    overall_credibility_score: int
    overall_verdict: str
    claim_analyses: List[ClaimAnalysis]
    suspicious_claims: List[str]
    strongest_claims: List[str]
    total_claims_analyzed: int


class GitHubAnalysisResponse(BaseModel):
    username: str
    credibility_score: int
    verdict: str
    
    basic_metrics: Dict[str, Any]
    engagement_metrics: Dict[str, Any]
    language_metrics: Dict[str, Any]
    repository_metrics: Dict[str, Any]
    
    signal_scores: Dict[str, int]
    strengths: List[str]
    weaknesses: List[str]
    reasoning: str


class CredibilityBreakdown(BaseModel):
    resume_score: int
    github_score: int
    weighted_overall: int
    score_distribution: Dict[str, int]


class RecruiterReportResponse(BaseModel):
    overall_score: int
    verdict: str
    credibility_breakdown: CredibilityBreakdown
    suspicious_claims: List[str]
    strengths: List[str]
    weaknesses: List[str]
    recruiter_summary: str
    recommendations: List[str]
