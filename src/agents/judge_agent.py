import logging

logger = logging.getLogger(__name__)


class JudgeAgent:
    """
    Combine the results from PriceAgent and IllegalAgent to determine if the ad is suspicious.
    Not directly use the original ads data.
    """

    def __init__(self, llm_client):
        self.llm_client = llm_client
    

    def judge(self, price_result: dict, illegal_result: dict) -> dict:
        """
        Give final judgement on the ad by combining the results from PriceAgent and IllegalAgent.

        Args:
        - price_result: the return value from PriceAgent.analyze()
        - illegal_result: the return value from IllegalAgent.analyze()

        Returns:
        - JSON object containing the analysis results(dict)
        {
            "label: "suspicious" | "safe",
            "reason": str
        }
        """
        pass