# File: rag_project/core/services/query_service.py

from typing import List
from rag_project.core.ports.llm_port import LLMPort
from rag_project.core.domain.chunk import Chunk

class QueryService:
    """
    Handles query refinement and synthesis with the help of an LLM.
    """
    def __init__(self, llm_port: LLMPort):
        self.llm_port = llm_port

    def generate_response(self, query: str, context_chunks: List[Chunk]) -> str:
        """
        Generate a response for the query using the retrieved context chunks.

        Args:
            query (str): User query.
            context_chunks (List[Chunk]): Relevant chunks to provide context.

        Returns:
            str: Generated response.
        """
        context = "\n".join(chunk.content for chunk in context_chunks)
        return self.llm_port.generate_response(context, query)
