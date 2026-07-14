from fastapi import APIRouter
from app.processors.github_processor import process_github

router = APIRouter()


@router.get("/{username}")
async def analyze_github(username: str):

    return await process_github(username)