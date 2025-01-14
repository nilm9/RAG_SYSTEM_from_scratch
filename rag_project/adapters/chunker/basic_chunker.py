# File: rag_project/adapters/chunker/basic_chunker.py

from typing import List
from rag_project.core.domain.chunk import Chunk
from rag_project.core.domain.document import Document
from rag_project.core.ports.chunker_port import ChunkerPort

class BasicChunker(ChunkerPort):
    """
    Adapter for splitting a document into smaller chunks.
    """
    def __init__(self, chunk_size: int = 512, overlap: int = 128):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document: Document) -> List[Chunk]:
        content = document.content
        chunks = []
        for index, i in enumerate(range(0, len(content), self.chunk_size - self.overlap)):
            chunk_content = content[i:i + self.chunk_size]
            chunks.append(Chunk(
                filename=document.filename,
                chunk_id=index,  # Use the loop index directly
                content=chunk_content
            ))

        return chunks
