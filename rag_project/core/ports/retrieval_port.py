# File: rag_project/core/ports/retrieval_port.py

from abc import ABC, abstractmethod
from typing import List
from rag_project.core.domain.chunk import Chunk

class RetrievalPort(ABC):
    """
    Interface for retrieval operations.
    """
    @abstractmethod
    def  retrieve(self, query: str, top_k: int) -> List[Chunk]:
        """
        Retrieve relevant chunks based on the query.

        Args:
            query (str): The search query text.
            top_k (int): Number of top chunks to retrieve.

        Returns:
            List[Chunk]: List of relevant chunks.
        """
        pass
