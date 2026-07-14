from pydantic import BaseModel
from typing import Optional


class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_text: Optional[str] = None