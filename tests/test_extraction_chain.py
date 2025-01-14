import pytest
from tests.utils import TestHelper

# Basic queries validation
@pytest.mark.parametrize(
    "question, expected_response",
    [
        (
            "Which library do we install for the extraction chain tutorial?",
            "langchain-core",
        ),
        (
            "Which environment variables do we set for LangSmith logging in the extraction tutorial?",
            "LANGCHAIN_TRACING_V2 and LANGCHAIN_API_KEY",
        ),
        (
            "What is the minimum version of langchain-core required?",
            "0.3.20",
        ),
        (
            "Which model is recommended for structured output in the tutorial?",
            "gpt-4o-mini",
        ),
    ],
)
def test_pipeline_queries(question, expected_response):
    """
    Test pipeline with parametrized Q&A pairs.
    """
    assert TestHelper.run_test_query(
        question=question,
        expected_response=expected_response,
    ), f"Test failed for question: {question}"


# Test with ambiguous or malformed questions
@pytest.mark.parametrize(
    "question, expected_response",
    [
        (
            "Do we use LangSmith in this tutorial?",
            "Yes",
        ),
        (
            "What environment variable starts with LANGCHAIN_TRACING?",
            "LANGCHAIN_TRACING_V2",
        ),
        (
            "Is the example code block valid Python?",
            "Yes",
        ),
    ],
)
def test_pipeline_edge_cases(question, expected_response):
    """
    Test pipeline with ambiguous and edge-case Q&A pairs.
    """
    assert TestHelper.run_test_query(
        question=question,
        expected_response=expected_response,
    ), f"Edge case failed for question: {question}"


# Test extraction with multi-entity responses
@pytest.mark.parametrize(
    "text_input, expected_response",
    [
        (
            "Alan Smith is 6 feet tall and has blond hair.",
            {
                "name": "Alan Smith",
                "height_in_meters": "1.83",  # Approximation of 6 feet
                "hair_color": "blond"
            },
        ),
        (
            "Anna has red hair and is 5.5 feet tall.",
            {
                "name": "Anna",
                "height_in_meters": "1.68",  # Approximation of 5.5 feet
                "hair_color": "red"
            },
        ),
    ],
)
def test_entity_extraction(text_input, expected_response):
    """
    Test entity extraction from text using the pipeline.
    """
    assert TestHelper.run_extraction_test(
        text=text_input,
        expected_response=expected_response,
    ), f"Entity extraction failed for text: {text_input}"


# Test failure scenarios
@pytest.mark.parametrize(
    "question, expected_error",
    [
        (
            "What is the latest unsupported feature?",
            "Feature not supported",
        ),
        (
            "Extract from a non-existing tutorial.",
            "Tutorial not found",
        ),
    ],
)
def test_pipeline_errors(question, expected_error):
    """
    Test pipeline with questions expected to raise specific errors.
    """
    with pytest.raises(ValueError, match=expected_error):
        TestHelper.run_test_query(
            question=question,
            expected_response=None,
        )


# Test pipeline with schema validation
def test_pipeline_with_invalid_schema():
    """
    Test pipeline behavior with invalid schema input.
    """
    invalid_input = {
        "name": 123,  # Invalid type
        "height_in_meters": "unknown",  # Invalid format
        "hair_color": None,
    }
    with pytest.raises(TypeError, match="Invalid schema"):
        TestHelper.run_extraction_test(
            text="Random person with invalid schema.",
            expected_response=invalid_input,
        )


# Test multi-entity extraction edge cases
def test_pipeline_multiple_entities():
    """
    Test pipeline handles multiple entities in the same input text.
    """
    text_input = "John is 5.9 feet tall with brown hair, and Lisa is 5.7 feet with blonde hair."
    expected_response = [
        {
            "name": "John",
            "height_in_meters": "1.80",
            "hair_color": "brown",
        },
        {
            "name": "Lisa",
            "height_in_meters": "1.73",
            "hair_color": "blonde",
        },
    ]
    assert TestHelper.run_extraction_test(
        text=text_input,
        expected_response=expected_response,
    ), f"Multiple entity extraction failed for text: {text_input}"


# Test empty or null inputs
@pytest.mark.parametrize(
    "question",
    [
        "",
        None,
        "   ",
    ],
)
def test_empty_or_null_inputs(question):
    """
    Test pipeline with empty or null inputs.
    """
    with pytest.raises(ValueError, match="Input cannot be empty or null"):
        TestHelper.run_test_query(question=question, expected_response=None)


# Test edge cases for tool usage
def test_pipeline_tool_usage():
    """
    Test pipeline with improper tool invocation.
    """
    question = "Invoke an unsupported tool."
    with pytest.raises(RuntimeError, match="Unsupported tool invoked"):
        TestHelper.run_test_query(question=question, expected_response=None)
