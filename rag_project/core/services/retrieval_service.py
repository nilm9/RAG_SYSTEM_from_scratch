# File: rag_project/core/services/retriever_service.py

from rag_project.core.ports.retrieval_port import RetrievalPort
from rag_project.core.services.embedding_service import EmbeddingService
from rag_project.core.domain.chunk import Chunk
from typing import List


class RetrievalService(RetrievalPort):
    """
    Handles chunk retrieval using vector stores and embeddings.
    """
    def __init__(self, vector_store, embedding_service: EmbeddingService):
        self.vector_store = vector_store
        self.embedding_service = embedding_service

    def retrieve(self, query: str, top_k: int) -> List[Chunk]:
        """
        Retrieve chunks using the vector store.
        """
        embedding = self.embedding_service.generate_query_embedding(query)
        results = self.vector_store.query(embedding, top_k)
        return [
            Chunk(
                filename=result['filename'],
                chunk_id=result['chunk_id'],
                content=result['content'],
                embedding=result.get('embedding'),
            )
            for result in results
        ]
