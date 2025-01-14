# File: rag_project/adapters/llm_adapter.py
from typing import Optional
from rag_project.core.ports.llm_port import LLMPort
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv()  # Load environment variables from a .env file


class OpenAILLMAdapter(LLMPort):
    """
    Adapter for interacting with OpenAI's LLM API.
    """
    def __init__(self, api_key: Optional[str] = None) :
        """
        Initialize the ChatGPT client. The API key can be passed directly or loaded from environment variables.

        :param api_key: Optional API key for the OpenAI API.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")  # Use the provided key or fall back to environment variable
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or in environment variables.")

        if os.getenv("TEST_MODE") == "True":
            print("Running in TEST MODE. API calls are mocked.")
            self.test_mode = True
        else:
            self.test_mode = False
            self.client = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                openai_api_key=self.api_key
            )

    def generate_response(self, context: str, query: str):
        """
        Generate a response from the OpenAI API by combining the context (retrieved chunks)
        and the user query into a single prompt.

        :param context: The retrieved chunks or relevant context.
        :param query: The user's query.
        :return: The LLM's generated response, as a string.
        """
        if self.test_mode:
            return f"Test mode: Simulated response for '{query[:50]}...' with context: '{context[:50]}...'"

        # Combine context + query into a single prompt
        prompt = f"""
        You are an AI that answers questions helpfully and accurately.
        Context provided is below:
        ----------------
        {context}
        ----------------
        User's question: {query}

        Answer:
        """

        # Use the LangChain ChatOpenAI .predict() method to get a response
        response = self.client.predict(prompt)
        return response.strip()