# File: ./rag_project/core/services/embedding_service.py

from typing import List
from sentence_transformers import SentenceTransformer
from rag_project.core.domain.chunk import Chunk


class EmbeddingService:
    """
    Generates embeddings for document chunks and queries using SentenceTransformer.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, chunks: List[Chunk]) -> List[Chunk]:
        """
        Generates embeddings for a list of chunks.

        Args:
            chunks (List[Chunk]): List of chunks to embed.

        Returns:
            List[Chunk]: List of chunks with embeddings.
        """
        contents = [chunk.content for chunk in chunks]
        embeddings = self.model.encode(contents, show_progress_bar=True)

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding.tolist()

        return chunks

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a text query.

        Args:
            query (str): The text query string.

        Returns:
            List[float]: Embedding vector for the query.
        """
        embedding = self.model.encode(query)
        return embedding.tolist()
