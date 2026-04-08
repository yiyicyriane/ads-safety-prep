import logging

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
        pass
