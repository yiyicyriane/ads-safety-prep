# Smoke test for Gemini API connectivity.
# Run this file to verify that the API Key is configured correctly.
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def test_gemini_call():
    """
    Smoke test: verify that the Gemini API key is set and a basic generate_content call succeeds.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY is not set in the environment variables")
        return
    
    client = genai.Client(api_key=api_key)

    prompt = "Please use one sentence to answer: What is ad safety?"
    print(f"[Test] Sending the request...")
    print(f"[Test] Prompt: {prompt}\n")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print("[Gemini Response]")
        print(response.text)
    except Exception as e:
        print(f"[Error] API call failed: {e}")


if __name__ == "__main__":
    test_gemini_call()

