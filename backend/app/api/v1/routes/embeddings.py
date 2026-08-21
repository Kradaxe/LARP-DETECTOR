from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


@router.get("/")
async def embeddings_disabled():
    """
    Embeddings endpoint disabled - Qdrant not configured.
    """
    return {
        "message": "Embeddings functionality is disabled. Qdrant vector database is not configured.",
        "status": "disabled"
    }
