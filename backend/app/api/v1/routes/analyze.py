from fastapi import APIRouter

from app.schemas.request_schema import AnalyzeRequest
from app.schemas.response_schema import AnalyzeResponse
from app.services.analysis_service import analyze_text

router = APIRouter()

@router.post(
    "/analyze/",
    response_model=AnalyzeResponse
)
async def analyze(
    request: AnalyzeRequest
):
    result = await analyze_text(request.text)

    return result