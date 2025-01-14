# File: rag_project/core/ports/llm_port.py

from abc import ABC, abstractmethod

class LLMPort(ABC):
    """
    Interface for Large Language Model (LLM) interactions.
    """
    @abstractmethod
    def generate_response(self, context: str, query: str) -> str:
        """
        Generate a response from the LLM based on context and query.

        Args:
            context (str): Context or retrieved information.
            query (str): User query.

        Returns:
            str: Generated response.
        """
        pass
