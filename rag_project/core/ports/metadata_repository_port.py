from abc import ABC, abstractmethod
from typing import Dict


class MetadataRepositoryPort(ABC):
    """
    Interface for metadata repository.
    """

    @abstractmethod
    def insert_metadata(self, filename: str, source: str, ingestion_timestamp: str):
        """
        Insert metadata into the storage system.

        Args:
            filename (str): The name of the file.
            source (str): Source of metadata.
            ingestion_timestamp (str): Timestamp of ingestion.
        """
        pass

    @abstractmethod
    def fetch_metadata(self):
        """
        Retrieve all metadata from storage.
        """
        pass
