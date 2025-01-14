from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from pgvector.sqlalchemy import VECTOR
from datetime import datetime


# Define Base using DeclarativeBase
class Base(DeclarativeBase):
    pass
class Metadata(Base):
    """
    Represents the metadata for ingested documents.
    """
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    source = Column(String)
    ingestion_timestamp = Column(TIMESTAMP, default=datetime.utcnow)


class Embedding(Base):
    """
    Represents the embeddings for document chunks.
    """
    __tablename__ = 'embeddings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    chunk_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding: List[float]  # Python type annotation for mypy
    embedding = Column(VECTOR(384), nullable=False)  # SQLAlchemy column definition