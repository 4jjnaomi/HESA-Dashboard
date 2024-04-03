from pathlib import Path

from dash import html, register_page, dcc, callback, Output, Input, callback_context
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

raw_data = Path(__file__).parent.parent.parent.joinpath('data','hei_data.csv')
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
    dbc.Col(children=[html.P("The map shows the location of HEIs in England.  Hover over a point to see more information about the HEI.", style={"font-size": "14px"}),
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
    Output('hei-dropdown-map', 'options'),
    Input('region-dropdown-map', 'value')
)
def update_hei_options(selected_regions):
    if selected_regions:
        # Filter HEIs based on selected regions
        heis_in_selected_regions = data_df[data_df['Region of HE provider'].isin(selected_regions)]['HE Provider']
        hei_options = [{'label': hei, 'value': hei} for hei in heis_in_selected_regions]
    else:
        # If no regions are selected, show all HEIs
        hei_options = [{'label': hei, 'value': hei} for hei in heis]

    return hei_options

@callback(
    Output('england_map', 'figure'),
    [Input('region-dropdown-map', 'value'),
     Input('hei-dropdown-map', 'value')]
)
def update_map(selected_regions, selected_heis):
    ctx = callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']
        if prop_id == 'region-dropdown-map.value':
            return create_scatter_mapbox(region=selected_regions)
        elif prop_id == 'hei-dropdown-map.value':
            return create_scatter_mapbox(hei=selected_heis)
    return create_scatter_mapbox()  # default to showing all data

@callback(
    Output('card', 'children'),
    Input('england_map', 'hoverData')
)
def display_card(hover_data):
    if hover_data is not None:
        ukprn = hover_data['points'][0]['customdata']
        if  ukprn is not None:
            return create_card(ukprn)