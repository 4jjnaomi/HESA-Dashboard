from dash import html, register_page, dcc, get_asset_url
import dash_bootstrap_components as dbc
from pathlib import Path
import pandas as pd
from figures import create_scatter_mapbox


# Register the page with the Dash app
register_page(__name__, name="Map View", path='/map_view')
\
raw_data = Path(__file__).parent.parent.parent.joinpath('data','dataset_prepared.csv')
data_df = pd.read_csv(raw_data)

#Create map
map_fig = create_scatter_mapbox()

#Create an array of regions
regions = data_df['Region of HE provider'].unique()

#Create an array of HEI
heis = data_df['HE Provider'].unique()

region_dropdown = dcc.Dropdown(
    id="region-dropdown",
    options=regions,
    placeholder="Select Region(s)",
    multi=True
)

hei_dropdown = dcc.Dropdown(
    id="hei-dropdown",
    options=heis,
    placeholder="Select HEI(s)",
    multi=True,
    optionHeight=50,
    maxHeight=350
)

row_one = dbc.Row([
        dbc.Col([html.H1("Map view")], width=12)
    ])

row_two = dbc.Row([
    dbc.Col(children=[html.P(children=["Filter Regions", region_dropdown], style={"background-color": "lightgrey"}), html.P(["Filter HEIs", hei_dropdown], style={"background-color": "lightgrey"} )], width=3),
    dbc.Col(children=[dcc.Graph(figure=map_fig, id='england_map')], width=9)
])


layout =  dbc.Container([
    row_one,
    row_two
])  