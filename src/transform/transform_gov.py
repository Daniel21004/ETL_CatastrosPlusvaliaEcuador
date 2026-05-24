# Imports
import polars as pl
from pyproj import Transformer
from src.transform.implementations.plusvalia_adapter import PlusvaliaBuyAdapter


def transform_gov_data(df):
    # pipeline implementation
    return pipeline(
        remove_columns,
        rename_columns,
        delete_nulls,
        strip_chars,
        filter_types,
        adapt_types_buy_plusvalia,
        transform_geolocation_to_WSG84,
        group_properties_grid,
    )(df)


# Transforms
def remove_columns(df):
    # Remove columns
    drop_columns = [
        "nro",
        "gid",
        "clave catastral",
        "numero de predio",
        "descripción del inmueble",
    ]
    df = df.drop(drop_columns)
    return df


def rename_columns(df):
    cols = {
        "tipo de bien": "tipo",
        "regimen del bien": "regimen",
        "coordenadas x": "x",
        "coordenadas y": "y",
    }
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
    valid_types = [
        "DEPARTAMENTO",
        "CASA",
        "TERRENO",
        "LOCAL COMERCIAL",
        "OFICINA",
    ]
    df = df.filter(pl.col("tipo").is_in(valid_types))
    return df


def adapt_types_buy_plusvalia(df):
    adapter = PlusvaliaBuyAdapter()
    return adapter.adapt(df)


def transform_geolocation_to_WSG84(df):
    # Transformación de UTM zona 17S a WGS84 (lat/lon)
    transformer = Transformer.from_crs("epsg:32717", "epsg:4326", always_xy=True)
    # Apply transform to coords and create latlon column e.g of row (x,y)
    lon, lat = transformer.transform(df["x"].to_numpy(), df["y"].to_numpy())

    df = df.with_columns(
        [pl.Series("lon", lon).alias("lon"), pl.Series("lat", lat).alias("lat")]
    )
    df = df.drop(["x", "y"])
    return df


def group_properties_grid(df):
    df = df.with_columns(pl.concat_str(["lon", "lat"], separator="_").alias("coord"))
    df_ids = df.select("coord").unique().with_row_index("id_edificio")
    df = df.join(other=df_ids, how="left", on="coord")
    df = df.drop("coord")
    return df


# Pipeline declaration
def pipeline(*transforms):
    def wrapper(value: pl.DataFrame):
        for t in transforms:
            value = apply(t, value)
        return value

    return wrapper


def apply(transform, value):
    return transform(value)
