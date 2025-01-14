from datetime import datetime
from typing import List
from rag_project.core.domain.chunk import Chunk
from rag_project.core.ports.chunker_port import ChunkerPort
from rag_project.core.ports.cleaner_port import CleanerPort
from rag_project.core.ports.plugin_port import Plugin
from rag_project.core.ports.saver_port import SaverPort
from rag_project.core.ports.metadata_repository_port import MetadataRepositoryPort
import os


class DataService:
    """
    Handles data processing workflows.
    """
    def __init__(
        self,
        plugins: List[Plugin],
        cleaner: CleanerPort,
        chunker: ChunkerPort,
        saver: SaverPort,
        metadata_repo: MetadataRepositoryPort
    ):
        self.plugins = plugins
        self.cleaner = cleaner
        self.chunker = chunker
        self.saver = saver
        self.metadata_repo = metadata_repo

    def process_files(self, directory: str) -> List[Chunk]:
        all_chunks = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            for plugin in self.plugins:
                if plugin.supports(filename):
                    document = plugin.load(filepath)
                    document.content = self.cleaner.clean(document.content)

                    document.add_metadata('source', filename.split('.')[-1].upper())
                    document.add_metadata('ingestion_timestamp', datetime.now().isoformat())

                    self.metadata_repo.insert_metadata(
                        filename=document.filename,
                        source=document.get_metadata('source'),
                        ingestion_timestamp=document.get_metadata('ingestion_timestamp'),
                    )

                    chunks = self.chunker.chunk(document)
                    self.saver.save_chunks(chunks)
                    all_chunks.extend(chunks)
                    break
        return all_chunks
