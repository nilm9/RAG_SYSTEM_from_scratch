# rag_project/core/pipeline.py

from typing import Any
import yaml

from rag_project.adapters.loader.notebook_adapter import NotebookLoader
from rag_project.adapters.loader.text_loader import TextLoader
from rag_project.adapters.cleaner.simple_cleaner import SimpleCleaner
from rag_project.adapters.chunker.basic_chunker import BasicChunker
from rag_project.adapters.metadata.metadata_pg import MetadataPG
from rag_project.adapters.saver.file_saver import FileSaver
from rag_project.adapters.llm.ollama_llm_adapter import OllamaLLMAdapter
from rag_project.core.services.data_service import DataService
from rag_project.core.services.embedding_service import EmbeddingService
from rag_project.core.services.retrieval_service import RetrievalService
from rag_project.core.services.query_service import QueryService
from rag_project.adapters.vector_store.pg_vector_store import PgVectorStore
from rag_project.adapters.database.connection import SessionLocal
import os


class PipelineSingleton:
    """
    Singleton for centralizing pipeline initialization and sharing across code and tests.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PipelineSingleton, cls).__new__(cls)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, "../../rag_project/config/settings.yaml")
            config = cls._load_config(config_path)

            cls.raw_dir = config['pipeline']['data']['raw_directory']
            cls.processed_dir = config['pipeline']['data']['processed_directory']
            cls.chunk_size = config['pipeline']['chunker']['chunk_size']
            cls.overlap = config['pipeline']['chunker']['overlap']
            cls.vector_dim = config['pipeline']['vector_store']['vector_dim']
            cls.query_text = config['pipeline']['query']['text']
            cls.top_k = config['pipeline']['query']['top_k']


            session = SessionLocal()
            metadata_repo = MetadataPG(session=session)

            # Initialize pipeline components
            cls.plugins = [TextLoader(), NotebookLoader()]
            cls.cleaner = SimpleCleaner()
            cls.chunker = BasicChunker(chunk_size=cls.chunk_size, overlap=cls.overlap)
            cls.saver = FileSaver(output_dir=cls.processed_dir)
            cls.data_service = DataService(cls.plugins, cls.cleaner, cls.chunker, cls.saver, metadata_repo)

            cls.embedding_service = EmbeddingService(model_name="all-MiniLM-L6-v2")

            # Choose the vector store based on configuration
            # cls.vector_store = FaissVectorStore(vector_dim=384)
            cls.vector_store = PgVectorStore(session=SessionLocal())  # Uncomment for PgVectorStore

            cls.retrieval_service = RetrievalService(cls.vector_store, cls.embedding_service)
            cls.llm_adapter = OllamaLLMAdapter(model_name="mistral")
            cls.query_service = QueryService(cls.llm_adapter)

        return cls._instance

    @staticmethod
    def _load_config(config_path: str) -> Any:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def run_ingestion(self):
        """
        Run the ingestion pipeline: process files, generate embeddings, and store data.
        """
        print("🚀 Starting ingestion workflow...")
        documents = self.data_service.process_files(self.raw_dir)
        chunks = self.embedding_service.generate_embeddings(documents)
        self.vector_store.insert(chunks)
        print("✅ Data ingestion completed successfully!")

    def run_retrieval(self):
        """
        Run the retrieval pipeline: query embeddings and return results.
        """
        print("Starting retrieval workflow...")
        retrieved_chunks = self.retrieval_service.retrieve(self.query_text, top_k=self.top_k)
        response = self.query_service.generate_response(self.query_text, retrieved_chunks)

        print("✅ Retrieved Chunks:")
        for chunk in retrieved_chunks:
            print(f"- Filename: {chunk.filename}, Content: {chunk.content}")

        print(f"🔗 Query: {self.query_text}")
        print(f"💬 Response: {response}")

