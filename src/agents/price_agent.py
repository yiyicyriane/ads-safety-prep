import logging
import json

logger = logging.getLogger(__name__)

class PriceAgent:
    """
    Responsible for detecting suspicious prices in ads.
    Just focus on the price and title of the ad.
    """


    def __init__(self, llm_client):
        """
        Args: 
        - llm_client: the instance of LLMClient, used to call Gemini API.
        """
        self.llm_client = llm_client
    

    def analyze(self, title: str, price: float) -> dict:
        """
        Use title and price to detect suspicious prices in ads.

        Args:
        - title: the title of the ad
        - price: the price of the ad

        Returns:
        - JSON object containing the analysis results(dict)
        {
            "price_suspicious": bool,
            "reason": str
        }
        """
        prompt = self._build_prompt(title, price)
        response_on_price = self.llm_client.generate(prompt)
        return self._parse_response(response_on_price)
    

    def _build_prompt(self, title: str, price: float) -> str:
        return (
            "You are a price analysis agent for an ad safety system.\n\n"
            "Task:\n"
            "Determine whether the price of the following ad is suspicious.\n\n"
            "Ad details:\n"
            f"- Title: {title}\n"
            f"- Price: ${price:.2f}\n\n"
            "Analysis rules:\n"
            "- A price is suspicious if it is unrealistically low for the product category.\n"
            "- For example, a brand-name smartphone priced at $5.00 is suspicious. A used yoga mat priced at $15.00 is not suspicious.\n\n"
            "Output format (STRICT):\n"
            "{\n"
            "  \"price_suspicious\": true | false,\n"
            "  \"reason\": \"one sentence\"\n"
            "}\n\n"
            "Rules:\n"
            "- Output MUST ONLY be valid JSON\n"
            "- DO NOT include markdown or extra text\n"
        )
    

    def _parse_response(self, response: str) -> dict:
        try:
            cleaned_response_on_price = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            result_on_price = json.loads(cleaned_response_on_price)

            if "price_suspicious" not in result_on_price or "reason" not in result_on_price:
                raise ValueError("Missing required fields in response")
            
            if not isinstance(result_on_price["price_suspicious"], bool):
                raise ValueError("price_suspicious must be a boolean")
            
            return result_on_price
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"[PriceAgent] Failed to parse response: {e}")
            logger.warning(f"[PriceAgent] Response on price: {response}")
            return {
                "price_suspicious": True,
                "reason": "parse_failed"
            }