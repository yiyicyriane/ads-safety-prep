# Smoke test for LLM API connectivity.
# Test safety agent by sending a test ad.
from llm_client import LLMClient
from agents.safety_agent import SafetyAgent

def test_api():
    """
    Smoke test for the LLM API connectivity.
    """
    client = LLMClient()
    prompt = "Please use one sentence to answer: What is ad safety?"
    response = client.generate(prompt)
    print(response)


def test_safety_agent():
    """
    Test the safety agent by sending a test ad.
    """
    agent = SafetyAgent()
    result = agent.analyze(
        title="iPhone 15 PRO",
        price=9.99,
        description="Brand new sealed in box"
    )
    print(result)
    print(type(result))


if __name__ == "__main__":
    test_api()
    test_safety_agent()