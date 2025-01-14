from sqlalchemy.orm import Session
from sqlalchemy import text
from rag_project.adapters.database.models import Metadata
from typing import Dict
from rag_project.core.ports.metadata_repository_port import MetadataRepositoryPort


class MetadataPG(MetadataRepositoryPort):
    """
    Handles metadata storage and querying in PostgreSQL.
    """
    def __init__(self, session: Session):
        self.session = session

    def insert_metadata(self, filename: str, source: str, ingestion_timestamp: str):
        """
        Insert metadata into the database.
        """
        metadata_entry = Metadata(
            filename=filename,
            source=source,
            ingestion_timestamp=ingestion_timestamp
        )
        self.session.add(metadata_entry)
        self.session.commit()

    def fetch_metadata(self):
        """
        Retrieve all metadata.
        """
        return self.session.query(Metadata).all()

    def close(self):
        """
        Close the session.
        """
        self.session.close()
