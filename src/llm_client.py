import os
from dotenv import load_dotenv
from google import genai


class LLMClient:
    def __init__(self):
        """
        Load the api key from .env file.
        Initialize the LLM client.
        """
        load_dotenv()

        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in .env file")

        self.client = genai.Client(api_key=self.api_key)
    

    def generate(self, prompt: str) -> str:
        """
        Receive a prompt and return the response from the LLM.

        Args:
            prompt: the prompt to send to the LLM
        
        Returns:
            The response from the LLM
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text
        except Exception as e:
            print(f"[Error] API call failed: {e}")
            raise