# Imports
import polars as pl

def clean_hygiene_gov_data(df):
    """
    Clean the hygiene for government data. This includes:
    - Removing false columns (those that start with "_duplicated")
    - Stripping spaces and converting column names to lowercase
    """
    # Clean false columns
    df = df.select([c for c in df.columns if c and not c.startswith("_duplicated")])

    # Delete spaces on columns
    df = df.rename({c: c.strip().lower() for c in df.columns})

    return df