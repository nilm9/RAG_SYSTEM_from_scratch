# File: ./rag_project/core/domain/document.py

from typing import Dict, Any
from pydantic import BaseModel, Field

class Document(BaseModel):
    """
    Represents a full document loaded into the system, including metadata.
    """
    filename: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_metadata(self, key: str, value: str):
        """
        Add or update metadata for the document.
        """
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        """
        Retrieve specific metadata by key.

        Args:
            key (str): Metadata key.

        Returns:
            Any: Metadata value or None.
        """
        return self.metadata.get(key)
