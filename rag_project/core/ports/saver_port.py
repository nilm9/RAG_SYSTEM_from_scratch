from abc import ABC, abstractmethod
from typing import List
from rag_project.core.domain.chunk import Chunk

class SaverPort(ABC):
    """
    Interface for saving chunks.
    """
    @abstractmethod
    def save_chunks(self, chunks: List[Chunk]) -> None:
        """
        Save chunks to a storage system.

        Args:
            chunks (List[Chunk]): List of chunks to be saved.
        """
        pass
