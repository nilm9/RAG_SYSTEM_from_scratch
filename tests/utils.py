# tests/utils.py

from langchain_community.llms.ollama import Ollama
from rag_project.core.pipeline import PipelineSingleton

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response?
"""


class TestHelper:
    """
    Helper class for running standardized tests and evaluations.
    """
    _ollama_instance = None

    @classmethod
    def get_ollama_instance(cls):
        if cls._ollama_instance is None:
            cls._ollama_instance = Ollama(model="mistral")
        return cls._ollama_instance

    @classmethod
    def run_test_query(cls, question: str, expected_response: str) -> bool:
        """
        Run a query and validate using the LLM.
        """
        pipeline = PipelineSingleton()
        response_text = pipeline.query_service.generate_response(question, [])

        prompt = EVAL_PROMPT.format(
            expected_response=expected_response, actual_response=response_text
        )

        model = cls.get_ollama_instance()
        evaluation_results_str = model.invoke(prompt)
        evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

        if "true" in evaluation_results_str_cleaned:
            print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
            return True
        elif "false" in evaluation_results_str_cleaned:
            print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
            return False
        else:
            raise ValueError("Invalid evaluation result. Expected 'true' or 'false'.")
