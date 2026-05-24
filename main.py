import polars as pl
from utils.duckdb import DuckDB

from pipelines.gov import GovPipeline
from pipelines.plusvalia import PlusvaliaScrapper

from config import PROPERTY_TYPE_MAP

# Init gob pipeline
gov_pipeline = GovPipeline()
# Execute pipeline and export finish db
df = gov_pipeline.pipeline(export=True)

# Plusvalia
scraper = PlusvaliaScrapper()

# Duckdb plusvalia
# Set columns of the table propiedades
propiedades_cols = {
    "provincia": "VARCHAR",
    "canton": "VARCHAR",
    "tipo": "FLOAT",
    "price": "DOUBLE",
    "m2": "DOUBLE",
}

print("Ejecutando pipeline Plusvalia...")
# Create DB and table
name_plusvalia_table = "propiedades"
propiedades_plusvalia_db = DuckDB("plusvalia.duckdb")
propiedades_plusvalia_db.create_table(name_plusvalia_table, propiedades_cols)

# Get provincias for iterit
provincias = (
    df.group_by("provincia")
    .len()
    .sort("len", descending=True)
    .get_column("provincia")
    .to_list()
)

for provincia in provincias:
    cantones = (
        df.filter(pl.col("provincia") == provincia)
        .group_by("canton")
        .len()
        .sort("len", descending=True)
        .filter(pl.col("len") >= 5)
        .get_column("canton")
        .to_list()
    )
    for canton in cantones:
        for property_type in PROPERTY_TYPE_MAP.values():
            data = scraper.pipeline(
                provincia,
                canton,
                property_type,
                file_name=f"{provincia}_{canton}_{property_type}.html",
            )
            # print(data)
            if not data:
                continue
            for item in data:
                propiedades_plusvalia_db.insert_to_table(
                    name_plusvalia_table,
                    [
                        provincia,
                        canton,
                        property_type,
                        item.get("price"),
                        item.get("m2"),
                    ],
                )
print("Pipeline plusvalia finalizado")
