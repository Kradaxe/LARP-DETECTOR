from fastapi import APIRouter, HTTPException
from app.processors.github_processor import process_github
from app.schemas.response_schema import GitHubAnalysisResponse

router = APIRouter()


@router.get("/{username}", response_model=GitHubAnalysisResponse)
async def analyze_github(username: str):
    """
    Analyze GitHub profile for technical credibility.
    
    This endpoint:
    1. Fetches profile metadata from GitHub API
    2. Fetches repositories
    3. Calculates comprehensive metrics (stars, forks, language diversity, etc.)
    4. Generates credibility signals from repository quality
    5. Returns recruiter-facing analysis with scores and reasoning
    """
    try:
        result = await process_github(username)
        return GitHubAnalysisResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during GitHub analysis: {str(e)}")