from pydantic import BaseModel
from typing import Optional


class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_text: Optional[str] = None


class FeedbackRequest(BaseModel):
    analysis_id: int
    recruiter_agreed: bool
    recruiter_comments: Optional[str] = None
    recruiter_id: Optional[str] = None