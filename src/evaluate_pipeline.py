import os
import sys
import logging
import time
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from loader import load_ads
from llm_client import LLMClient
from agents.price_agent import PriceAgent
from agents.illegal_agent import IllegalAgent
from agents.judge_agent import JudgeAgent
from evaluator import compute_confusion_matrix, print_metrics


def setup_logging() -> None:
    """
    Setup logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def parse_args():
    """
    Parse command line arguments.

    Returns:
        args: a namespace object containing the input path
    """
    parser = argparse.ArgumentParser(
        description="Ads safety evaluation pipeline: analyze ads data, mark suspicious ads, and evaluate the pipeline"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=os.path.join(BASE_DIR, "../data/labeled_ads.csv"),
        help="Path to the input CSV file (default: %(default)s)"
    )

    return parser.parse_args()


def run_pipeline_on_row(row: dict, price_agent: PriceAgent, illegal_agent: IllegalAgent, judge_agent: JudgeAgent) -> str:
    """
    Run the full multi-agent pipeline on a single ad.

    Returns:
        The predicted label, either "suspicious" or "safe"
    """
    price_agent_result = price_agent.analyze(row["title"], row["price"])
    illegal_agent_result = illegal_agent.analyze(row["title"], row["description"])
    judge_agent_result = judge_agent.judge(price_agent_result, illegal_agent_result)

    label = judge_agent_result.get("label", "suspicious")
    if label not in ("suspicious", "safe"):
        label = "suspicious"
    
    return label

def run_evaluation():
    """
    Load the labeled ads data, run pipeline, compute and print metrics, and show error cases.
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    args = parse_args()
    logger.info(f"Input: {args.input}")

    try:
        # load the labeled ads data
        df = load_ads(args.input)

        if "label" not in df.columns:
            raise ValueError("Input file must have a 'label' column with ground truth")

        # Initialize the agents
        client = LLMClient()
        price_agent = PriceAgent(client)
        illegal_agent = IllegalAgent(client)
        judge_agent = JudgeAgent(client)

        # run the pipeline to get each ad's analysis results
        results = []
        predicted_labels = []
        true_labels = []
        for _, row in df.iterrows():
            try:
                predicted_result = run_pipeline_on_row(row, price_agent, illegal_agent, judge_agent)
            except Exception as e:
                logger.warning(f"Pipeline failed for ad '{row['title']}': {e}, defaulting to suspicious")
                predicted_result = "suspicious"
            
            predicted_labels.append(predicted_result)
            true_labels.append(row["label"])
            results.append({
                "id": row["id"],
                "title": row["title"],
                "price": row["price"],
                "true_label": row["label"],
                "predicted_label": predicted_result,
                "correct": predicted_result == row["label"],
            })
            time.sleep(15)

        # compute and print metrics
        matrix = compute_confusion_matrix(true_labels, predicted_labels)
        print_metrics(matrix)

        # show error cases
        error_cases = [result for result in results if not result["correct"]]
        print(f"=== Error Cases ({len(error_cases)} / {len(results)}) ===")
        for result in error_cases:
            error_type = "FP" if result["predicted_label"] == "suspicious" and result["true_label"] == "safe" else "FN"
            print(f"[{error_type}] id={result['id']} | {result['title']} | ${result['price']} | true_label={result['true_label']} | predicted_label={result['predicted_label']}")
        print(f"\nTotal: {len(results)} ads processed, {len(error_cases)} errors found")

    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
    except ValueError as e:
        logger.error(f"Data validation failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_evaluation()