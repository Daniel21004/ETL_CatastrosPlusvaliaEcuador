# Imports
import polars as pl
from src.transform.implementations.plusvalia_adapter import PlusvaliaBuyAdapter

def transform_gov_data(df):
    # pipeline implementation
    return pipeline(remove_columns,rename_columns, delete_nulls, strip_chars, filter_types, adapt_types_buy_plusvalia )(df)

# Transforms
def remove_columns(df):
    # Remove columns
    drop_columns = ["nro", "gid", "clave catastral", "numero de predio", "descripción del inmueble"]
    df = df.drop(drop_columns)
    return df

def rename_columns(df):
    cols = {"tipo de bien": "tipo",
              "regimen del bien": "regimen",
              "coordenadas x": "x",
              "coordenadas y": "y"}
    df = df.rename(cols)
    return df

def delete_nulls(df):
   if df.null_count().sum_horizontal().item() > 0:
        df = df.drop_nulls()
   return df

def strip_chars(df):
    df = df.with_columns(pl.col(pl.String).str.strip_chars())
    return df

def filter_types(df):
    # notes: BODEGA = bodega-galpon
    #notes: EDIFICIO = edificio-hotel-fabrica
    valid_types = ["DEPARTAMENTO", "CASA", "GALPON", "TERRENO", "LOCAL COMERCIAL", "OFICINA", "BODEGA","EDIFICIO", "PARQUEADERO"]
    df = df.filter(pl.col("tipo").is_in(valid_types))
    return df
    
def adapt_types_buy_plusvalia(df):
    adapter = PlusvaliaBuyAdapter()
    return adapter.adapt(df)

# Pipeline declaration 
def pipeline(*transforms):
    def wrapper(value: pl.DataFrame):
        for t in transforms:
            value = apply(t, value)
        return value
    return wrapper

def apply(transform, value):
    return transform(value)