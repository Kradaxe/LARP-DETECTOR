from google import genai
from app.config.settings import settings
from typing import List


class EmbeddingService:
    """Generate embeddings using Google Gemini API."""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using Gemini.
        
        Args:
            text: Text to generate embedding for
        
        Returns:
            List of float values representing the embedding
        """
        try:
            response = self.client.models.embed_content(
                model="models/text-embedding-004",
                contents=text,
                config=genai.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
            )
            return response.embeddings[0].values
        except Exception as e:
            raise ValueError(f"Failed to generate embedding: {str(e)}")
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to generate embeddings for
        
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
