# File: rag_project/adapters/vector_store_adapter.py

from sqlalchemy.orm import Session
from sqlalchemy import text
from rag_project.core.ports.vector_store_port import VectorStorePort
from rag_project.core.domain.chunk import Chunk
from rag_project.adapters.database.models import Embedding
from typing import List, Dict


class PgVectorStore(VectorStorePort):
    """
    Adapter for PostgreSQL with pgvector extension.
    """
    def __init__(self, session: Session):
        self.session = session

    def insert(self, chunks: List[Chunk]) -> None:
        for chunk in chunks:
            embedding = chunk.embedding
            if embedding is None:
                raise ValueError("Chunk embedding cannot be None")

            embedding_entry = Embedding(
                filename=chunk.filename,
                chunk_id=chunk.chunk_id,
                content=chunk.content,
                embedding=embedding,
            )
            self.session.add(embedding_entry)
        self.session.commit()

    def query(self, embedding: List[float], top_k: int) -> List[Dict]:
        embedding_str = f"[{','.join(map(str, embedding))}]"
        query = text(f"""
            SELECT id, filename, chunk_id, content, doc_metadata, embedding <-> '{embedding_str}' AS distance
            FROM embeddings
            ORDER BY distance ASC
            LIMIT :top_k
        """)
        result = self.session.execute(query, {'top_k': top_k}).fetchall()

        return [
            {
                'id': row.id,
                'filename': row.filename,
                'chunk_id': row.chunk_id,
                'content': row.content,
                'metadata': row.doc_metadata
            }
            for row in result
        ]
