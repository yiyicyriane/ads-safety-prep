import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src"))

from llm_client import LLMClient
from agents.price_agent import PriceAgent


def test_price_agent():
    client = LLMClient()
    agent = PriceAgent(client)

    test_cases = [
        {"title": "iPhone 15 Pro", "price": 9.99,   "expect": True},
        {"title": "Yoga Mat",       "price": 18.00,  "expect": False},
        {"title": "Gucci Handbag",  "price": 5.00,   "expect": True},
        {"title": "Coffee Maker",   "price": 25.00,  "expect": False},
    ]

    for case in test_cases:
        result = agent.analyze(case["title"], case["price"])
        status = "✅" if result["price_suspicious"] == case["expect"] else "❌"
        
        print(f"{status} {case['title']} with price ${case['price']:.2f}")
        print(f"- price_suspicious: {result['price_suspicious']}")
        print(f"- reason: {result['reason']}")
        print()
        time.sleep(15)

if __name__ == "__main__":
    test_price_agent()