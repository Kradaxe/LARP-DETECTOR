from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Optional, Any
from app.config.settings import settings
from app.services.embedding_service import EmbeddingService


class QdrantService:
    """Service for storing and searching candidate embeddings in Qdrant."""
    
    COLLECTION_NAME = "candidate_claims"
    EMBEDDING_DIMENSION = 768  # Gemini embedding dimension
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None
        )
        self.embedding_service = EmbeddingService()
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Ensure the collection exists, create if it doesn't."""
        collections = self.client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if self.COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )
    
    def store_claim(
        self,
        claim: str,
        candidate_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a claim with its embedding in Qdrant.
        
        Args:
            claim: The claim text
            candidate_id: Unique identifier for the candidate
            metadata: Additional metadata to store
        
        Returns:
            Point ID of the stored claim
        """
        # Generate embedding
        embedding = self.embedding_service.generate_embedding(claim)
        
        # Create point ID (use timestamp + candidate_id for uniqueness)
        import time
        point_id = f"{candidate_id}_{int(time.time() * 1000)}"
        
        # Prepare payload
        payload = {
            "claim": claim,
            "candidate_id": candidate_id,
            "timestamp": int(time.time())
        }
        
        if metadata:
            payload.update(metadata)
        
        # Store in Qdrant
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )
        
        return point_id
    
    def store_claims_batch(
        self,
        claims: List[str],
        candidate_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Store multiple claims for a candidate.
        
        Args:
            claims: List of claim texts
            candidate_id: Unique identifier for the candidate
            metadata: Additional metadata to store for all claims
        
        Returns:
            List of point IDs
        """
        import time
        point_ids = []
        
        # Generate embeddings for all claims
        embeddings = self.embedding_service.generate_embeddings_batch(claims)
        
        # Create points
        points = []
        for i, (claim, embedding) in enumerate(zip(claims, embeddings)):
            point_id = f"{candidate_id}_{int(time.time() * 1000)}_{i}"
            point_ids.append(point_id)
            
            payload = {
                "claim": claim,
                "candidate_id": candidate_id,
                "timestamp": int(time.time())
            }
            
            if metadata:
                payload.update(metadata)
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            )
        
        # Batch upsert
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )
        
        return point_ids
    
    def search_similar_claims(
        self,
        query_claim: str,
        limit: int = 10,
        score_threshold: float = 0.7,
        candidate_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
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
        # Generate embedding for query
        query_embedding = self.embedding_service.generate_embedding(query_claim)
        
        # Build filter if candidate_id is provided
        query_filter = None
        if candidate_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="candidate_id",
                        match=MatchValue(value=candidate_filter)
                    )
                ]
            )
        
        # Search
        results = self.client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "claim": result.payload.get("claim"),
                "candidate_id": result.payload.get("candidate_id"),
                "similarity_score": result.score,
                "point_id": result.id,
                "metadata": {k: v for k, v in result.payload.items() 
                           if k not in ["claim", "candidate_id"]}
            })
        
        return formatted_results
    
    def find_duplicate_claims(
        self,
        claim: str,
        threshold: float = 0.9
    ) -> List[Dict[str, Any]]:
        """
        Find potential duplicate claims with high similarity.
        
        Args:
            claim: The claim to check for duplicates
            threshold: Similarity threshold for considering as duplicate
        
        Returns:
            List of potential duplicate claims
        """
        return self.search_similar_claims(
            query_claim=claim,
            limit=10,
            score_threshold=threshold
        )
    
    def get_candidate_claims(
        self,
        candidate_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all claims for a specific candidate.
        
        Args:
            candidate_id: The candidate ID to retrieve claims for
            limit: Maximum number of claims to retrieve
        
        Returns:
            List of claims with metadata
        """
        # Scroll through collection with filter
        results, _ = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="candidate_id",
                        match=MatchValue(value=candidate_id)
                    )
                ]
            ),
            limit=limit
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "claim": result.payload.get("claim"),
                "candidate_id": result.payload.get("candidate_id"),
                "point_id": result.id,
                "metadata": {k: v for k, v in result.payload.items() 
                           if k not in ["claim", "candidate_id"]}
            })
        
        return formatted_results
    
    def compare_candidates(
        self,
        candidate_id_1: str,
        candidate_id_2: str
    ) -> Dict[str, Any]:
        """
        Compare two candidates based on their claim embeddings.
        
        Args:
            candidate_id_1: First candidate ID
            candidate_id_2: Second candidate ID
        
        Returns:
            Comparison results with similarity metrics
        """
        # Get claims for both candidates
        claims_1 = self.get_candidate_claims(candidate_id_1)
        claims_2 = self.get_candidate_claims(candidate_id_2)
        
        if not claims_1 or not claims_2:
            return {
                "candidate_id_1": candidate_id_1,
                "candidate_id_2": candidate_id_2,
                "error": "One or both candidates have no stored claims"
            }
        
        # Find similar claims between candidates
        similar_claims = []
        for claim_1 in claims_1:
            similar = self.search_similar_claims(
                query_claim=claim_1["claim"],
                limit=5,
                score_threshold=0.75,
                candidate_filter=candidate_id_2
            )
            if similar:
                similar_claims.append({
                    "claim_1": claim_1["claim"],
                    "similar_claims_2": similar
                })
        
        # Calculate overall similarity
        total_similarities = sum([
            len(sc["similar_claims_2"]) for sc in similar_claims
        ])
        max_possible = len(claims_1) * 5  # Assuming max 5 similar per claim
        overall_similarity = total_similarities / max_possible if max_possible > 0 else 0
        
        return {
            "candidate_id_1": candidate_id_1,
            "candidate_id_2": candidate_id_2,
            "claims_count_1": len(claims_1),
            "claims_count_2": len(claims_2),
            "similar_claim_pairs": len(similar_claims),
            "overall_similarity": round(overall_similarity, 3),
            "similar_claims_detail": similar_claims
        }
    
    def delete_candidate_claims(self, candidate_id: str) -> int:
        """
        Delete all claims for a specific candidate.
        
        Args:
            candidate_id: The candidate ID to delete claims for
        
        Returns:
            Number of points deleted
        """
        # Get all points for the candidate
        points = self.get_candidate_claims(candidate_id)
        point_ids = [p["point_id"] for p in points]
        
        if point_ids:
            self.client.delete(
                collection_name=self.COLLECTION_NAME,
                points_selector=point_ids
            )
        
        return len(point_ids)
