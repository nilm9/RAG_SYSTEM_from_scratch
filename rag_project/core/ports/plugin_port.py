from abc import ABC, abstractmethod
from typing import List
from rag_project.core.domain.document import Document


class Plugin(ABC):
    """
    Base class for all plugins.
    """
    @abstractmethod
    def supports(self, filename: str) -> bool:
        """
        Check if the plugin supports processing the given file type.

        Args:
            filename (str): The file name.

        Returns:
            bool: True if supported, False otherwise.
        """
        pass

    @abstractmethod
    def load(self, filepath: str) -> Document:
        """
        Load and process a single file.

        Args:
            filepath (str): Path to the file.

        Returns:
            Document: Processed document object.
        """
        pass
