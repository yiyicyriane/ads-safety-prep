# control the data pipeline
# currently load ads data from csv file, analyze and mark suspicious ads, write the completed results and suspicious results to output files
import os
import argparse
import logging

from loader import load_ads
from analyzer import analyze_ads
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
    args = parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"Input: {args.input}")
    logger.info(f"Output: {args.output}")

    try:
        # load ads data
        df = load_ads(args.input)
        
        # analyze ads data
        df_analyzed = analyze_ads(df)

        # write the results to output files
        write_results(df_analyzed, args.output)

        logger.info("Pipeline completed successfully")
    
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
    except ValueError as e:
        logger.error(f"Data validation failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
