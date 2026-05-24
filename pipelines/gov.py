from utils.duckdb import DuckDB

from src.extraction.DA_gov_extraction import extract_gov_data
from src.cleaning.hygiene_gov_data import clean_hygiene_gov_data
from src.transform.transform_gov import transform_gov_data


class GovPipeline:
    def export_df(self, df):
        duck = DuckDB("gov.duckdb")
        duck.create_table_from_df("catastros", df)
#         df = duck.connection.execute("""
#         SELECT * FROM catastros LIMIT 10
#         """).fetchdf()
#         print(df)

    def pipeline(self, export=False):
        print("Ejecutando pipeline Gov...")
        df = extract_gov_data()
        df = clean_hygiene_gov_data(df)
        df = transform_gov_data(df)
        if export:
            self.export_df(df)    
        print("Pipeline finalizado y exportado correctamente")
        return df
