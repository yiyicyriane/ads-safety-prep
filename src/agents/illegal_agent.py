import logging
import json

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
        prompt = self._build_prompt(title, description)
        response_on_illegal = self.llm_client.generate(prompt)
        return self._parse_response(response_on_illegal)
    

    def _build_prompt(self, title: str, description: str) -> str:
        return (
            "You are a illegal content analysis agent for an ad safety system.\n\n"
            "Task:\n"
            "Determine whether the description of the following ad contains illegal content.\n\n"
            "Ad details:\n"
            f"- Title: {title}\n"
            f"- Description: {description}\n\n"
            "Analysis rules:\n"
            "- A description is illegal if it contains any illegal content. For example,\n" 
            "- Suspected sale of stolen goods: 'stolen', 'no questions asked', 'quick sale', etc.\n"
            "- Counterfeit goods: 'counterfeit', 'fake', 'replica', etc.\n"
            "- Illegal goods: 'weapon', 'drug', 'controlled substances', 'illegal services', etc.\n"
            "- Misleading claims: grossly exaggerated claims, and unsubstantiated statements.\n\n"
            "Output format (STRICT):\n"
            "{\n"
            "  \"illegal_flag\": true | false,\n"
            "  \"reason\": \"one sentence\"\n"
            "}\n\n"
            "Rules:\n"
            "- Output MUST ONLY be valid JSON\n"
            "- DO NOT include markdown or extra text\n"
        )
    

    def _parse_response(self, response: str) -> dict:
        try:
            cleaned_response_on_illegal = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            result_on_illegal = json.loads(cleaned_response_on_illegal)

            if "illegal_flag" not in result_on_illegal or "reason" not in result_on_illegal:
                raise ValueError("Missing required fields in response")
            
            if not isinstance(result_on_illegal["illegal_flag"], bool):
                raise ValueError("illegal_flag must be a boolean")
            
            return result_on_illegal
        
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"[IllegalAgent] Failed to parse response: {e}")
            logger.warning(f"[IllegalAgent] Response on illegal: {response}")
            return {
                "illegal_flag": True,
                "reason": "parse_failed"
            }