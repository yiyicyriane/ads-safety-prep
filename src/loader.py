# 负责从数据源中加载数据
# use padas dataframe to load data
import pandas as pd
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"id", "title", "price", "description"}


def load_ads(file_path: str) -> pd.DataFrame:
    """
    Load ads data from a CSV file into a pandas dataframe.

    Args:
        file_path: The path to the CSV file containing the ads data.(str)
    
    Returns:
        A dataframe containing the ads data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file missing required columns.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File {file_path} not found")
        raise
    
    
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"[Loader] Missing required columns: {missing}")
    
    logger.info(f"Successfully loaded {len(df)} ads from {file_path}")
    return df