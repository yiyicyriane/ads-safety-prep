# analyze the ads data: mark suspicious ads
# detect logics:
# 1. price < 20
# 2. for title contains luxury word, price < 50

import pandas as pd
import logging

logger = logging.getLogger(__name__)
# Key words for luxury ads
LUXURY_KEYWORDS = {
    "rolex",
    "gucci",
    "louis vuitton",
    "iphone",
    "macbook",
    "airpods",
    "playstation"
}

PRICE_THRESHOLD_GENERAL = 20.0 # Threshold for all ads
PRICE_THRESHOLD_LUXURY = 50.0 # Threshold for luxury ads

def contains_luxury_keywords(title: str) -> bool:
    """
    Check whether the ads title contains any luxury keywords.

    Args:
        title: the title of the ad (str)
    
    Returns:
        True if contains any luxury keywords, False otherwise
    """
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in LUXURY_KEYWORDS)


def analyze_ads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze ads data and mark suspicious ads.

    Rules:
        1. all price less than PRICE_THRESHOLD_GENERAL are suspicious
        2. for title contains luxury word, price less than PRICE_THRESHOLD_LUXURY are suspicious

    Args:
        df: pandas dataframe containing the ads data
    
    Returns:
        A dataframe with a new column 'suspicious' indicating if the ad is suspicious
    """
    df = df.copy() # make a copy of the dataframe to avoid modifying the original data
    df["is_suspicious"] = False

    rule1 = df["price"] < PRICE_THRESHOLD_GENERAL
    has_luxury_keywords = df["title"].apply(contains_luxury_keywords)
    rule2 = has_luxury_keywords & (df["price"] < PRICE_THRESHOLD_LUXURY)
   
    df.loc[rule1 | rule2, "is_suspicious"] = True

    suspicious_count = df["is_suspicious"].sum()
    logger.info(f"Detected {suspicious_count} suspicious ads out of {len(df)}")
    return df