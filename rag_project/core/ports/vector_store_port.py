from abc import ABC, abstractmethod
from typing import List, Dict, Any

from rag_project.core.domain.chunk import Chunk


class VectorStorePort(ABC):
    @abstractmethod
    def insert(self, chunks: List[Chunk]) -> None:
        pass

    @abstractmethod
    def query(self, embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        pass
