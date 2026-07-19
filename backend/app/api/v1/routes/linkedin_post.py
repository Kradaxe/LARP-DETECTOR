from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.linkedin_post_service import analyze_linkedin_post

router = APIRouter()

class LinkedInPostRequest(BaseModel):
    post_url: str

@router.post("/analyze-linkedin-post")
async def analyze_linkedin_post_endpoint(request: LinkedInPostRequest):
    """
    Analyze a LinkedIn post for technical credibility and potential LARPing.
    """
    try:
        print("Received LinkedIn post URL:", request.post_url)
        result = await analyze_linkedin_post(request.post_url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
