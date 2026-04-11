import os
import logging

from dotenv import load_dotenv
from google import genai

logger = logging.getLogger(__name__)

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
                model="gemini-3.1-flash-lite-preview",
                contents=prompt
            )

            return response.text
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise