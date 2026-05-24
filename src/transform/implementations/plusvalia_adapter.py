from src.transform.interfaces.portal_adapter_interface import PortalAdapterInterface
import polars as pl


class PlusvaliaBuyAdapter(PortalAdapterInterface):
    # url: https://www.plusvalia.com/venta/inmuebles/pichincha/quito?propertyType=1,2,32,33&sort=more_recent
    property_type_map = {
        "DEPARTAMENTO": 2,
        "CASA": 1,
        "TERRENO": 3,
        "LOCAL COMERCIAL": 5,
        "OFICINA": 4,
    }

    def adapt(self, df):
        df = df.with_columns(
            pl.col("tipo")
            .replace(self.property_type_map)
            .alias("tipo_canonico_plusvalia")
        )
        return df
