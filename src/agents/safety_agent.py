# safety agent: Use title, price, description to use LLM to detect suspicious ads
import json
import logging
from llm_client import LLMClient

logger = logging.getLogger(__name__)

class SafetyAgent:
    def __init__(self):
        """
        Initialize the LLM client.
        """
        self.llm_client = LLMClient()

    def analyze(self, title: str, price: float, description: str) -> dict:
        """
        Use title, price, and description to detect suspicious ads.

        Args:
            title: the title of the ad
            price: the price of the ad
            description: the description of the ad
        
        Returns:
            JSON object containing the analysis results(dict)
        """
        try:
            prompt = (
                "You are an ad safety classifier.\n\n"
                "Ad details:\n"
                f"- Title: {title}\n"
                f"- Price: {price}\n"
                f"- Description: {description}\n\n"
                "Task:\n"
                "Determine whether the ad is suspicious.\n"
                "Output format (STRICT):\n"
                "{\n"
                "  \"label\": \"suspicious\" | \"safe\"\n"
                "  \"reason\": \"one sentence\"\n"
                "}\n\n"
                "Rules:\n"
                "- Output MUST be valid JSON\n"
                "- DO NOT include markdown or extra text\n"
            )
            response = self.llm_client.generate(prompt)
            
            cleaned_response = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(cleaned_response)
        except Exception as e:
            logger.error(f"[Safety Agent] Error: {e}")
            raise