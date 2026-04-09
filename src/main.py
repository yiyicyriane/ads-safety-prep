# control the data pipeline
# currently load ads data from csv file, analyze and mark suspicious ads, write the completed results and suspicious results to output files
import os
import argparse
import logging
import sys
import time

from loader import load_ads
from agents.price_agent import PriceAgent
from agents.illegal_agent import IllegalAgent
from agents.judge_agent import JudgeAgent
from llm_client import LLMClient
from writer import write_results

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
        args: a namespace object containing the input and output paths
    """
    parser = argparse.ArgumentParser(
        description="Ads safety pipeline: analyze ads data and mark suspicious ads"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=os.path.join(BASE_DIR, "../data/ads.csv"),
        help="Path to the input CSV file (default: %(default)s)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join(BASE_DIR, "../output"),
        help="Path to the output directory (default: %(default)s)"
    )

    return parser.parse_args()


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    args = parse_args()

    logger.info(f"Input: {args.input}")
    logger.info(f"Output: {args.output}")

    try:
        # load ads data
        df = load_ads(args.input)
        
        # analyze ads data
        client = LLMClient()
        price_agent = PriceAgent(client)
        illegal_agent = IllegalAgent(client)
        judge_agent = JudgeAgent(client)

        results = []
        for _, row in df.iterrows():
            try:
                price_result = price_agent.analyze(row["title"], row["price"])
                illegal_result = illegal_agent.analyze(row["title"], row["description"])
                judge_result = judge_agent.judge(price_result, illegal_result)

                results.append({
                    "id": row["id"],
                    "title": row["title"],
                    "price": row["price"],
                    "label": judge_result["label"],
                    "price_suspicious": price_result["price_suspicious"],
                    "illegal_flag": illegal_result["illegal_flag"],
                    "reason": judge_result["reason"],
                })
            except Exception as e:
                logger.warning(f"Failed to analyze ad '{row['title']}': {e}")
                results.append({
                    "id": row["id"],
                    "title": row["title"],
                    "price": row["price"],
                    "label": "suspicious",
                    "price_suspicious": True,
                    "illegal_flag": True,
                    "reason": "analysis_failed",
                })
            time.sleep(60)

        # write the results to output files
        write_results(results, args.output)

        logger.info("Pipeline completed successfully")
    
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
    except ValueError as e:
        logger.error(f"Data validation failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
