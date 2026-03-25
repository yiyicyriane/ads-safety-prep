# Smoke test for Gemini API connectivity.
# Run this file to verify that the API Key is configured correctly.
from llm_client import LLMClient

def test_api():
    """
    Smoke test for the LLM API connectivity.
    """
    client = LLMClient()
    prompt = "Please use one sentence to answer: What is ad safety?"
    response = client.generate(prompt)
    print(response)


if __name__ == "__main__":
    test_api()