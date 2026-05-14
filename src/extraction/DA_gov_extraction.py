# Imports
import polars as pl

# Read data .csv
df = pl.read_csv(source="data/raw/DA_CatastrosEcuador_2025/conjunto-de-datos.csv", 
                 separator=";", 
                 encoding="latin1",
                 truncate_ragged_lines=True,
                 schema_overrides={"Clave Catastral": pl.String})

# Clean false columns
df = df.select([c for c in df.columns if c and not c.startswith("_duplicated")])

# Delete spaces on columns
df = df.rename({c: c.strip() for c in df.columns})

# View data
print(df.columns)

