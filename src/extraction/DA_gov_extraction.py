# Imports
import polars as pl

def extract_gov_data() -> pl.Dataframe:
    """
    Extract government data from a CSV file.
    """
    # Read data .csv
    df = pl.read_csv(source="data/raw/DA_CatastrosEcuador_2025/conjunto-de-datos.csv", 
                     separator=";", 
                     encoding="latin1",
                     truncate_ragged_lines=True,
                     schema_overrides={"Clave Catastral": pl.String})

    return df
