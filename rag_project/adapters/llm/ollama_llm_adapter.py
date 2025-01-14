# File: rag_project/adapters/ollama_llm_adapter.py
from typing import Optional
from rag_project.core.ports.llm_port import LLMPort
import os
from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama

load_dotenv()  # Load environment variables from a .env file

class OllamaLLMAdapter(LLMPort):
    """
    Adapter for interacting with a local Ollama model via LangChain.
    """

    def __init__(self, model_name: str = "mistral", system_prompt: Optional[str] = None):
        """
        :param model_name: Name of the local model installed in Ollama (e.g. 'mistral', 'llama2-7b', etc).
        :param system_prompt: Optional system prompt or initial instructions.
        """
        # If you have a "test_mode" concept, you can also pass that in or detect env var.
        # For now we keep it simple.
        self.model_name = model_name
        self.system_prompt = system_prompt or "You are a helpful local model using Ollama."

        # Create a LangChain Ollama instance
        #  * You can pass other parameters (like 'cfg', 'temperature', etc) if desired.

        self.client = Ollama(
            model=model_name,
            base_url="http://localhost:11434",  # default is usually http://localhost:11411
        )


    def generate_response(self, context: str, query: str) -> str:
        """
        Generate a response from the local Ollama model by combining
        the context (retrieved chunks) and the user query into a single prompt.
        """
        # Build the prompt
        # (You can also incorporate system_prompt or other instruction tokens if you like)
        prompt = f"""
        {self.system_prompt}

        Context provided is below:
        ----------------
        {context}
        ----------------

        User's question: {query}

        Answer:
        """

        # Actually call Ollama. `.invoke()` returns text.
        response_text = self.client.invoke(prompt)
        # Or if you prefer: self.client(prompt) => which uses __call__
        # But typically you want to read .invoke()

        return response_text.strip()
