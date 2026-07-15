from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.recruiter_report_service import RecruiterReportService
from app.schemas.response_schema import RecruiterReportResponse

router = APIRouter()


class ReportRequest(BaseModel):
    resume_analysis: Optional[dict] = None
    github_analysis: Optional[dict] = None


@router.post("/generate", response_model=RecruiterReportResponse)
async def generate_recruiter_report(request: ReportRequest):
    """
    Generate a comprehensive recruiter report combining resume and GitHub analysis.
    
    This endpoint:
    1. Accepts resume analysis and GitHub analysis outputs
    2. Combines both analyses into a weighted overall score
    3. Aggregates suspicious claims, strengths, and weaknesses
    4. Generates recruiter-friendly summary and recommendations
    5. Returns actionable insights for hiring decisions
    """
    try:
        # Validate that at least one analysis is provided
        if not request.resume_analysis and not request.github_analysis:
            raise HTTPException(
                status_code=400,
                detail="At least one of resume_analysis or github_analysis must be provided"
            )
        
        # Generate the report
        report = RecruiterReportService.generate_report(
            resume_analysis=request.resume_analysis,
            github_analysis=request.github_analysis
        )
        
        return RecruiterReportResponse(**report)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during report generation: {str(e)}"
        )
