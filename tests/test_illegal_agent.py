import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src"))

from llm_client import LLMClient
from agents.illegal_agent import IllegalAgent


def test_illegal_agent():
    client = LLMClient()
    agent = IllegalAgent(client)

    test_cases = [
        {"title": "MacBook Pro", "description": "Stolen goods quick sale no questions asked", "expect": True},
        {"title": "Gucci Handbag", "description": "Replica inspired luxury bag free shipping", "expect": True},
        {"title": "Running Shoes", "description": "Comfortable everyday running shoes size 10", "expect": False},
        {"title": "Coffee Maker", "description": "Gently used works perfectly", "expect": False},
    ]

    for case in test_cases:
        result = agent.analyze(case["title"], case["description"])

        status = "✅" if result["illegal_flag"] == case["expect"] else "❌"
        print(f"{status} {case['title']} with description {case['description']}")
        print(f"- illegal_flag: {result['illegal_flag']}")
        print(f"- reason: {result['reason']}")
        print()
        time.sleep(15)

if __name__ == "__main__":
    test_illegal_agent()