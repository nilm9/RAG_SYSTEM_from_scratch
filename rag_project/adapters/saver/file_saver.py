# File: rag_project/adapters/saver/file_saver.py

import os
from typing import List
from rag_project.core.domain.chunk import Chunk
from rag_project.core.ports.saver_port import SaverPort

class FileSaver(SaverPort):
    """
    Adapter for saving chunks to disk.
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_chunks(self, chunks: List[Chunk]) -> None:
        for chunk in chunks:
            file_path = os.path.join(self.output_dir, f"{chunk.filename}_chunk_{chunk.chunk_id}.txt")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(chunk.content)
