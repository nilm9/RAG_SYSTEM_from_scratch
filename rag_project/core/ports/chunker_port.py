from abc import ABC, abstractmethod
from typing import List

from rag_project.core.domain.chunk import Chunk
from rag_project.core.domain.document import Document

class ChunkerPort(ABC):
    """
    Interface for text chunking operations.
    """
    @abstractmethod
    def chunk(self, document: Document) -> List[Chunk]:
        """
        Split a document into smaller chunks.

        Args:
            document (Document): The document to be chunked.

        Returns:
            List[Chunk]: List of text chunks.
        """
        pass
