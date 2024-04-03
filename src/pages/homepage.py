from pathlib import Path

from dash import html, register_page, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from figures import create_scatter_mapbox, create_card

# Register the page with the Dash app
register_page(__name__, name="Homepage", path='/')

button1 = html.Div([
    dbc.Button([html.H6("Ranking Table"), html.P("See the performance of all HEIs")], color="primary", href="/ranking_table", style = {"height": "70px"}, id="ranking_table-button") 
],
className="d-grid gap-2 mx-auto"
)

button2 = html.Div([
    dbc.Button([html.H6("HEI overview"), html.P("Analyse the performance of a specific HEI")], color="primary", href="/university/Anglia Ruskin University", style = {"height": "70px"}, id="hei_overview-button")
],
className="d-grid gap-2 mx-auto"
)

button3 = html.Div([
    dbc.Button([html.H6("HEI comparison"), html.P("Compare the performance a set of HEIs")], color="primary", href="/comparison", style = {"height": "70px"}, id="hei_comparison-button")
],
className= "d-grid gap-2 mx-auto"
)

raw_data = Path(__file__).parent.parent.parent.joinpath('data','dataset_prepared.csv')
data_df = pd.read_csv(raw_data)

#Create map
map_fig = create_scatter_mapbox()

#Create an array of regions
regions = data_df['Region of HE provider'].unique()

#Create an array of HEI
heis = data_df['HE Provider'].unique()

region_dropdown = dcc.Dropdown(
    id="region-dropdown-map",
    options=regions,
    placeholder="Select Region(s)",
    multi=True
)

hei_dropdown = dcc.Dropdown(
    id="hei-dropdown-map",
    options=heis,
    placeholder="Select HEI(s)",
    multi=True,
    optionHeight=50,
    maxHeight=350
)

row_one = html.Div([
    html.H1('Welcome to the UK HEI Environmental Dashboard')
])

row_two = html.Div([
    html.P
    ('This dashboard provides an overview of the environmental performance of Higher Education Institutions (HEIs) in England.')
])

row_three = dbc.Row([
    dbc.Col(button1, width=4),
    dbc.Col(button2, width=4),
    dbc.Col(button3, width=4)
])

row_four = dbc.Row([
    dbc.Col(children=[html.Br(),
                      html.P(children=["Filter Regions", region_dropdown], style={"background-color": "lightgrey"}), 
                      html.P(["Filter HEIs", hei_dropdown], style={"background-color": "lightgrey"} )], width=2),
    dbc.Col(children=[dcc.Graph(figure=map_fig, id='england_map')], width=8),
    dbc.Col(children=[html.Div(id='card')], width=2)
],
style={"padding-top": "20px"})


layout =  dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four
])

@callback(
    Output('card', 'children'),
    Input('england_map', 'hoverData')
)
def display_card(hover_data):
    if hover_data is not None:
        ukprn = hover_data['points'][0]['customdata'][0]
        if  ukprn is not None:
            return create_card(ukprn)