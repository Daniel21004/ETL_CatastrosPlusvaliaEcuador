import streamlit as stl
from config import PROPERTY_TYPE_MAP
import duckdb

# Maps
import pydeck as pdk

# Colors
from utils.cluster_generator_color import generate_color_palete

# Stream page config
stl.set_page_config(
    # Browser pege title, browser page icon and layout
    page_title="Ecuador Properties Dashboard",
    page_icon="🇪🇨",
    layout="wide",
)

# Title on screen
stl.title("Properties Dashboard")
# Show or hidden About dataset section
with stl.expander("About Datasets"):
    # About dataset section
    stl.header("About the main datasets")
    stl.markdown("""
    This dashboard´ve been based on two main dataset:

    1. BASE DE DATOS DE BIENES INMUEBLES CATASTRADOS II SEMESTRE 2025 from [Datos abiertos](https://www.datosabiertos.gob.ec/dataset/base-de-datos-de-bienes-inmuebles-catastrados-ii-semestre-2025)
    2. WebScrapping to Plusvalia.com website with BeautifulSoup.

    The first dataset contains verified data about properties on Ecuador from 2025. All contable and location data is based on this dataset
    The second dataset contains data about the price of this properties. All price and m2 data is based on this dataset
        """)

# LOAD DATA
# Create connections
conn_gov = duckdb.connect("data/db/gov.duckdb")
conn_plusvalia = duckdb.connect("data/db/plusvalia.duckdb")
# create df
df_gov = conn_gov.execute(
    "SELECT provincia, canton, tipo, lon, lat, id_edificio FROM catastros"
).fetchdf()
df_plusvalia = conn_plusvalia.execute("SELECT * FROM propiedades").fetchdf()


# Get columns value
provincies = df_gov["provincia"].unique().tolist()
property_type = df_gov["tipo"].unique().tolist()

# Sidebar
with stl.sidebar:
    stl.header("Filters", divider=True)
    selected_cantons = []
    selected_provincias = stl.multiselect(
        "Province: ", provincies, placeholder="Filter by provincies"
    )
    if selected_provincias:
        cantons = (
            df_gov[df_gov["provincia"].isin(selected_provincias)]["canton"]
            .unique()
            .tolist()
        )
        selected_cantons = stl.multiselect(
            "Canton: ", cantons, placeholder="Filter by cantons"
        )
    selected_property_type = stl.multiselect(
        "Property Type: ", property_type, placeholder="Filter by tipo"
    )

# Apply filters
# Create a copy of df_gov
filtered_df_gov = df_gov.copy()
filtered_df_plusvalia = df_plusvalia.copy()

# Decision what filters apply
if selected_provincias:
    filtered_df_gov = filtered_df_gov[
        filtered_df_gov["provincia"].isin(selected_provincias)
    ]
    filtered_df_plusvalia = filtered_df_plusvalia[
        filtered_df_plusvalia["provincia"].isin(selected_provincias)
    ]
if selected_cantons:
    filtered_df_gov = filtered_df_gov[filtered_df_gov["canton"].isin(selected_cantons)]
    filtered_df_plusvalia = filtered_df_plusvalia[
        filtered_df_plusvalia["canton"].isin(selected_cantons)
    ]
if selected_property_type:
    filtered_df_gov = filtered_df_gov[
        filtered_df_gov["tipo"].isin(selected_property_type)
    ]
    filtered_df_plusvalia = filtered_df_plusvalia[
        filtered_df_plusvalia["tipo"].isin(
            map(lambda type: PROPERTY_TYPE_MAP[type], selected_property_type)
        )
    ]


# Display
total_properties = len(filtered_df_gov.index)

if total_properties > 0 and not filtered_df_plusvalia.empty:
    price_m2 = filtered_df_plusvalia["price"].sum() / filtered_df_plusvalia["m2"].sum()
    price_m2 = round(price_m2, 2)
else:
    price_m2 = 0

col1, col2 = stl.columns(2)
col1.metric("Total of Properties", total_properties)
col2.metric("Mean $/m2", f"${price_m2}")


# Map
# Colors
prov_list = filtered_df_gov["provincia"].unique().copy().tolist()
dict_canton_colors = {}

for i, provincia in enumerate(prov_list):
    cantons_list = (
        filtered_df_gov[filtered_df_gov["provincia"] == provincia]["canton"]
        .unique()
        .tolist()
    )
    color_palete = generate_color_palete(i, len(cantons_list))
    for j, canton in enumerate(cantons_list):
        dict_canton_colors[canton] = color_palete[j]
filtered_df_gov["colors"] = filtered_df_gov["canton"].map(dict_canton_colors)

ICON_URL = (
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png"
)

ICON_MAPPING = {
    "marker": {
        "x": 0,
        "y": 0,
        "width": 128,
        "height": 128,
        "anchorY": 128,
        "mask": True,
    }
}
# Layer
layer = pdk.Layer(
    "IconLayer",
    data=filtered_df_gov,
    get_position="[lon, lat]",
    get_icon="'marker'",
    get_size=4,
    size_scale=5,
    get_color="colors",
    icon_atlas=ICON_URL,
    icon_mapping=ICON_MAPPING,
    pickable=True,
)
#
# Vista inicial
view_state = pdk.ViewState(latitude=-3.9931, longitude=-79.2042, zoom=6, pitch=0)

# Mostrar mapa
stl.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{provincia}\n{canton}"},
        map_style="road",
    )
)


stl.write("Filtered Data", filtered_df_gov[["provincia", "canton", "tipo"]])
