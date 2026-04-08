import logging

logger = logging.getLogger(__name__)


class IllegalAgent:
    """
    Responsible for detecting illegal ads.
    Just focus on the title and description of the ad.
    """

    def __init__(self, llm_client):
        self.llm_client = llm_client
    

    def analyze(self, title: str, description: str) -> dict:
        """
        Use title and description to detect whether ad's description contains illegal content.

        Args:
        - title: the title of the ad
        - description: the description of the ad

        Returns:
        - JSON object containing the analysis results(dict)
        {
            "illegal_flag": bool,
            "reason": str
        }
        """
        pass
    