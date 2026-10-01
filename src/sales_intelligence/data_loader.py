"""Data loading and validation module."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"Product", "Category", "Price", "Units_Sold", "Cost"}


def load_sales_data(filepath: str) -> pd.DataFrame:
    """
    Load and validate sales CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Validated DataFrame containing sales data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing or file is empty.
    """
    logger.info("Loading data from %s", filepath)
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        logger.error("File not found: %s", filepath)
        raise

    if df.empty:
        logger.error("The provided CSV file is empty.")
        raise ValueError("The provided CSV file is empty.")

    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        logger.error("Missing required columns: %s", missing_cols)
        raise ValueError(f"Missing required columns: {missing_cols}")

    logger.info("Successfully loaded %d records.", len(df))
    return df
