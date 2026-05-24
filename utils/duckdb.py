import duckdb


class DuckDB:
    def __init__(self, db_name):
        self.connection = duckdb.connect(
            f"data/db/{db_name}"
        )  # For instance, properties.duckdb

    def create_table(self, table_name, columns):
        # columns is a dict with the name of the columns as key, and its type as value
        schema = ",".join([f"{key} {value}" for key, value in columns.items()])
        self.connection.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {schema}
            )
        """)

    def create_table_from_df(self, table_name, df):
        self.connection.register("temp_df", df)
        self.connection.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} AS
            SELECT * FROM temp_df
        """)

    def insert_to_table(self, table_name, values):
        # values is a list of values
        self.connection.execute(
            f"""
            INSERT INTO {table_name}
            VALUES ({", ".join(["?"] * len(values))})
        """,
            values,
        )
