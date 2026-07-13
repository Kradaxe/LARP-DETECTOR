from fastapi import APIRouter

from app.models.request_models import AnalyzeRequest
from app.models.response_models import AnalyzeResponse
from app.services.analysis_service import analyze_text

router = APIRouter()

@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
async def analyze(
    request: AnalyzeRequest
):
    result = await analyze_text(request.text)

    return result