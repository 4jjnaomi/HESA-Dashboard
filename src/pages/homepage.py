from pathlib import Path
from dash import html, register_page, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from figures import create_scatter_mapbox, create_card

# Register the page with the Dash app
register_page(__name__, name="Homepage", path='/')

raw_data = Path(__file__).parent.parent.parent.joinpath('data','hei_data.csv')
data_df = pd.read_csv(raw_data)

def create_button(text, href):
    return html.Div(
        dbc.Button(
            [html.H6(text), html.P("See the performance of all HEIs")],
            color="primary",
            href=href,
            style={"height": "70px"},
            id=f"{text.lower().replace(' ', '_')}-button"
        ),
        className="d-grid gap-2 mx-auto"
    )

def create_dropdown(id1, options, placeholder, multi=False, optionHeight=50, maxHeight=350):
    return dcc.Dropdown(
        id=id1,
        options=options,
        placeholder=placeholder,
        multi=multi,
        optionHeight=optionHeight,
        maxHeight=maxHeight
    )

def create_row(content):
    return dbc.Row(content, style={"padding-top": "20px"})

def layout():
    regions = [{'label': region, 'value': region} for region in data_df['Region of HE provider'].unique()]
    heis = [{'label': hei, 'value': hei} for hei in data_df['HE Provider'].unique()]

    button1 = create_button("Ranking Table", "/ranking_table")
    button2 = create_button("HEI overview", "/university/Anglia Ruskin University")
    button3 = create_button("HEI comparison", "/comparison")

    region_dropdown = create_dropdown("region-dropdown-map", regions, "Select Region(s)", multi=True)
    hei_dropdown = create_dropdown("hei-dropdown-map", heis, "Select HEI(s)", multi=True)

    row_one = html.Div([html.H1('Welcome to the England HEI Environmental Dashboard')])
    row_two = html.Div([html.P('This dashboard provides an overview of the environmental performance of Higher Education Institutions (HEIs) in England.')])
    row_three = create_row([dbc.Col(button1, width=4), dbc.Col(button2, width=4), dbc.Col(button3, width=4)])

    row_four = create_row([
        dbc.Col(children=[
            html.P("The map shows the location of HEIs in England. Hover over a point to see more information about the HEI.", style={"font-size": "14px"}),
            html.P(children=["Filter Regions", region_dropdown], style={"background-color": "lightgrey"}),
            html.P(["Filter HEIs", hei_dropdown], style={"background-color": "lightgrey"})], width=2),
        dbc.Col(children=[dcc.Graph(figure=create_scatter_mapbox(), id='england_map')], width=8),
        dbc.Col(children=[html.Div(id='card')], width=2)
    ])

    layout_page = dbc.Container([row_one, row_two, row_three, row_four])
    return layout_page

@callback(
    Output('hei-dropdown-map', 'options'),
    Input('region-dropdown-map', 'value')
)
def update_hei_options(selected_regions):
    if selected_regions:
        heis_in_selected_regions = data_df[data_df['Region of HE provider'].isin(selected_regions)]['HE Provider']
        hei_options = [{'label': hei, 'value': hei} for hei in heis_in_selected_regions]
    else:
        hei_options = [{'label': hei, 'value': hei} for hei in data_df['HE Provider']]

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
        if ukprn is not None:
            return create_card(ukprn)

