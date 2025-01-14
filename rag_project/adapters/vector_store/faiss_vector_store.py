# File: rag_project/adapters/vector_store_adapter.py

import numpy as np
import faiss
from rag_project.core.ports.vector_store_port import VectorStorePort
from rag_project.core.domain.chunk import Chunk
from typing import List, Dict


class FaissVectorStore(VectorStorePort):
    """
    Adapter for FAISS vector store operations.
    """
    def __init__(self, vector_dim: int):
        self.vector_dim = vector_dim
        self.index = faiss.IndexFlatL2(self.vector_dim)
        self.chunk_data: List[Dict] = []

        print(f"Initialized FAISS Index with dimension: {self.vector_dim}")

    def insert(self, chunks: List[Chunk]):
        embeddings_to_add = []
        for chunk in chunks:
            if chunk.embedding is not None:
                embedding_np = np.array(chunk.embedding, dtype=np.float32)
                embeddings_to_add.append(embedding_np)
                self.chunk_data.append({
                    "chunk_id": chunk.chunk_id,
                    "filename": chunk.filename,
                    "content": chunk.content,
                    "embedding": chunk.embedding,
                })

        if embeddings_to_add:
            embeddings_matrix = np.vstack(embeddings_to_add)
            self.index.add(embeddings_matrix)

    def query(self, embedding: List[float], top_k: int) -> List[Dict]:
        if self.index.ntotal == 0:
            return []

        query_vector = np.array(embedding, dtype=np.float32).reshape(1, -1)
        distances, indices = self.index.search(query_vector, top_k)

        return [
            self.chunk_data[idx] for idx in indices[0] if idx != -1
        ]
