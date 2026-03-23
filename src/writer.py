# write the analyzed data to output files

import pandas as pd
import os

def write_results(df: pd.DataFrame, output_dir: str) -> None:
    """
    Write the completed analysis results and suspicious ads to output files in csv format.

    Args:
        df: pandas dataframe containing the is_suspicious column
        output_dir: the directory to write the output files
    
    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    # Write the completed analysis results
    completed_result_path = os.path.join(output_dir, "completed_results.csv")
    df.to_csv(completed_result_path, index=False)
    print(f"[Writer] Completed analysis results written to {completed_result_path}")

    # Write the suspicious results
    suspicious_result_path = os.path.join(output_dir, "suspicious_results.csv")
    suspicious_df = df[df["is_suspicious"]]
    suspicious_df.to_csv(suspicious_result_path, index=False)
    print(f"[Writer] Suspicious ads written to {suspicious_result_path} ")
    print(f"[Writer] Total {len(suspicious_df)} suspicious ads found")
