# File: ./rag_project/core/domain/chunk.py

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator

class Chunk(BaseModel):
    """
    Represents a chunk of text from a document, including metadata.
    """
    filename: str
    chunk_id: int
    content: str
    # embedding can be List[float] or None. If you want it always as List[float], remove Optional.
    embedding: Optional[List[float]] = None

    @validator('chunk_id')
    def check_chunk_id(cls, v):
        if v < 0:
            raise ValueError("chunk_id must be non-negative")
        return v

