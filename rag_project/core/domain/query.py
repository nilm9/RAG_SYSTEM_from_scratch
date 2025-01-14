# File: ./rag_project/core/domain/query.py

from typing import Dict, Any
from pydantic import BaseModel, Field

class Query(BaseModel):
    """
    Represents a query to retrieve relevant chunks with optional metadata filters.
    """
    text: str
    metadata_filters: Dict[str, Any] = Field(default_factory=dict)

    def add_filter(self, key: str, value: str):
        """
        Add or update metadata filter.
        """
        self.metadata_filters[key] = value

    def get_filter(self, key: str):
        """
        Retrieve a specific metadata filter by key.
        """
        return self.metadata_filters.get(key)
