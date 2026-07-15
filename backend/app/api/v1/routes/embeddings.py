from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.qdrant_service import QdrantService

router = APIRouter()


class StoreClaimRequest(BaseModel):
    claim: str
    candidate_id: str
    metadata: Optional[Dict[str, Any]] = None


class StoreClaimsBatchRequest(BaseModel):
    claims: List[str]
    candidate_id: str
    metadata: Optional[Dict[str, Any]] = None


class SimilaritySearchRequest(BaseModel):
    query_claim: str
    limit: int = 10
    score_threshold: float = 0.7
    candidate_filter: Optional[str] = None


class DuplicateCheckRequest(BaseModel):
    claim: str
    threshold: float = 0.9


class CandidateComparisonRequest(BaseModel):
    candidate_id_1: str
    candidate_id_2: str


@router.post("/store")
async def store_claim(request: StoreClaimRequest):
    """
    Store a single claim with its embedding in Qdrant.
    
    Args:
        claim: The claim text to store
        candidate_id: Unique identifier for the candidate
        metadata: Optional additional metadata
    
    Returns:
        Point ID of the stored claim
    """
    try:
        qdrant_service = QdrantService()
        point_id = qdrant_service.store_claim(
            claim=request.claim,
            candidate_id=request.candidate_id,
            metadata=request.metadata
        )
        return {"point_id": point_id, "status": "stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store claim: {str(e)}")


@router.post("/store-batch")
async def store_claims_batch(request: StoreClaimsBatchRequest):
    """
    Store multiple claims for a candidate in batch.
    
    Args:
        claims: List of claim texts to store
        candidate_id: Unique identifier for the candidate
        metadata: Optional additional metadata for all claims
    
    Returns:
        List of point IDs for the stored claims
    """
    try:
        qdrant_service = QdrantService()
        point_ids = qdrant_service.store_claims_batch(
            claims=request.claims,
            candidate_id=request.candidate_id,
            metadata=request.metadata
        )
        return {
            "point_ids": point_ids,
            "count": len(point_ids),
            "status": "stored"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store claims: {str(e)}")


@router.post("/search")
async def search_similar_claims(request: SimilaritySearchRequest):
    """
    Search for similar claims using vector similarity.
    
    Args:
        query_claim: The claim to find similar claims for
        limit: Maximum number of results to return
        score_threshold: Minimum similarity score (0-1)
        candidate_filter: Optional candidate ID to filter by
    
    Returns:
        List of similar claims with scores and metadata
    """
    try:
        qdrant_service = QdrantService()
        results = qdrant_service.search_similar_claims(
            query_claim=request.query_claim,
            limit=request.limit,
            score_threshold=request.score_threshold,
            candidate_filter=request.candidate_filter
        )
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/check-duplicates")
async def check_duplicates(request: DuplicateCheckRequest):
    """
    Find potential duplicate claims with high similarity.
    
    Args:
        claim: The claim to check for duplicates
        threshold: Similarity threshold for considering as duplicate
    
    Returns:
        List of potential duplicate claims
    """
    try:
        qdrant_service = QdrantService()
        duplicates = qdrant_service.find_duplicate_claims(
            claim=request.claim,
            threshold=request.threshold
        )
        return {
            "duplicates": duplicates,
            "count": len(duplicates),
            "is_duplicate": len(duplicates) > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Duplicate check failed: {str(e)}")


@router.get("/candidate/{candidate_id}")
async def get_candidate_claims(candidate_id: str, limit: int = 100):
    """
    Retrieve all claims for a specific candidate.
    
    Args:
        candidate_id: The candidate ID to retrieve claims for
        limit: Maximum number of claims to retrieve
    
    Returns:
        List of claims with metadata
    """
    try:
        qdrant_service = QdrantService()
        claims = qdrant_service.get_candidate_claims(
            candidate_id=candidate_id,
            limit=limit
        )
        return {"candidate_id": candidate_id, "claims": claims, "count": len(claims)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve claims: {str(e)}")


@router.post("/compare")
async def compare_candidates(request: CandidateComparisonRequest):
    """
    Compare two candidates based on their claim embeddings.
    
    Args:
        candidate_id_1: First candidate ID
        candidate_id_2: Second candidate ID
    
    Returns:
        Comparison results with similarity metrics
    """
    try:
        qdrant_service = QdrantService()
        comparison = qdrant_service.compare_candidates(
            candidate_id_1=request.candidate_id_1,
            candidate_id_2=request.candidate_id_2
        )
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.delete("/candidate/{candidate_id}")
async def delete_candidate_claims(candidate_id: str):
    """
    Delete all claims for a specific candidate.
    
    Args:
        candidate_id: The candidate ID to delete claims for
    
    Returns:
        Number of points deleted
    """
    try:
        qdrant_service = QdrantService()
        deleted_count = qdrant_service.delete_candidate_claims(candidate_id)
        return {
            "candidate_id": candidate_id,
            "deleted_count": deleted_count,
            "status": "deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")
