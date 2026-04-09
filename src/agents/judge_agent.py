import logging
import json

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
            "label": "suspicious" | "safe",
            "reason": str
        }
        """
        prompt = self._build_prompt(price_result, illegal_result)
        response_on_judge = self.llm_client.generate(prompt)
        return self._parse_response(response_on_judge)
    

    def _build_prompt(self, price_result: dict, illegal_result: dict) -> str:
        return (
            "You are a judge agent for an ad safety system.\n\n"
            "Task:\n"
            "Determine whether the ad is suspicious based on the price and illegal flag.\n\n"
            "Ad details:\n"
            f"- Price suspicious: {price_result['price_suspicious']} with reason {price_result['reason']}\n"
            f"- Illegal flag: {illegal_result['illegal_flag']} with reason {illegal_result['reason']}\n\n"
            "Analysis rules:\n"
            "- If either the price is suspicious or the illegal flag is true, the ad is suspicious.\n"
            "- Otherwise, the ad is safe.\n\n"
            "Output format (STRICT):\n"
            "{\n"
            "  \"label\": \"suspicious\" | \"safe\",\n"
            "  \"reason\": \"one sentence\"\n"
            "}\n\n"
            "Rules:\n"
            "- Output MUST ONLY be valid JSON\n"
            "- DO NOT include markdown or extra text\n"
        )
    

    def _parse_response(self, response: str) -> dict:
        try:
            cleaned_response_on_judge = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            result_on_judge = json.loads(cleaned_response_on_judge)

            if "label" not in result_on_judge or "reason" not in result_on_judge:
                raise ValueError("Missing required fields in response")
            
            if result_on_judge["label"] not in ("suspicious", "safe"):
                raise ValueError("label must be either 'suspicious' or 'safe'")
            
            return result_on_judge
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"[JudgeAgent] Failed to parse response: {e}")
            logger.warning(f"[JudgeAgent] Response on judge: {response}")
            return {
                "label": "suspicious",
                "reason": "parse_failed"
            }