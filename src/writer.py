# write the analyzed data to output files

import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)


def write_results(results: list, output_dir: str) -> None:
    """
    Write the completed analysis results and suspicious ads to output files in csv format.

    Args:
        results: list of dictionaries containing the analysis results
        output_dir: the directory to write the output files
    
    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    # Write the completed analysis results
    completed_result_path = os.path.join(output_dir, "completed_results.csv")
    completed_df = pd.DataFrame(results)
    completed_df.to_csv(completed_result_path, index=False)
    logger.info(f"Completed analysis results written to {completed_result_path}")

    # Write the suspicious results
    suspicious_result_path = os.path.join(output_dir, "suspicious_results.csv")
    suspicious_df = completed_df[completed_df["label"] == "suspicious"]
    suspicious_df.to_csv(suspicious_result_path, index=False)
    logger.info(f"Suspicious ads written to {suspicious_result_path}")
    logger.info(f"Total {len(suspicious_df)} suspicious ads found")
