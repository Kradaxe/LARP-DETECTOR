from fastapi import APIRouter, HTTPException, Query
from app.schemas.request_schema import FeedbackRequest
from app.services.feedback_service import FeedbackService

router = APIRouter()


@router.post("")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit recruiter feedback for an analysis.
    
    Recruiters can agree or disagree with the credibility score,
    optionally providing comments and their identifier.
    
    Args:
        request: Feedback request containing analysis_id, agreement status, and optional comments
    
    Returns:
        Confirmation of feedback submission
    """
    try:
        feedback = FeedbackService.create_feedback(
            analysis_id=request.analysis_id,
            recruiter_agreed=request.recruiter_agreed,
            recruiter_comments=request.recruiter_comments,
            recruiter_id=request.recruiter_id
        )
        
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": feedback.id,
            "analysis_id": feedback.analysis_id,
            "recruiter_agreed": feedback.recruiter_agreed
        }
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")


@router.get("/stats")
async def get_feedback_stats(days: int = Query(30, ge=1, le=365)):
    """
    Get feedback statistics for a specified time period.
    
    Args:
        days: Number of days to look back (default: 30, max: 365)
    
    Returns:
        Statistics including total feedback, agreement rate, and recruiter breakdown
    """
    try:
        stats = FeedbackService.get_feedback_stats(days=days)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feedback stats: {str(e)}")
