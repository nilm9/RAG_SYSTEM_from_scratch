from abc import ABC, abstractmethod
from typing import List
from rag_project.core.domain.document import Document

class FileLoaderPort(ABC):
    """
    Interface for file loading operations.
    """
    @abstractmethod
    def load_files(self, directory: str) -> List[Document]:
        """
        Load files from a directory and return them as Document objects.

        Args:
            directory (str): Path to the directory containing raw files.

        Returns:
            List[Document]: List of loaded documents.
        """
        pass
