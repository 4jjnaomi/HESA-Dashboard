from dash import html, register_page, callback, Output, Input, dcc
import dash_bootstrap_components as dbc
from figures import create_ranking_table

# Register the page with the Dash app
register_page(__name__, name="Ranking Table", path='/ranking_table')

class_dropdown = dbc.Select(
    id="class-dropdown-rank",  # id uniquely identifies the element, will be needed later
    options=["Building and spaces", "Energy", "Emissions and waste", "Transport and environment", "Finances and people"],
    value="Building and spaces"
)

year_dropdown = dbc.Select(
    id="year-dropdown-rank",
    options=[ "2018/19", "2019/20", "2020/21", "2021/22"],  
    value="2021/22"
)

region_dropdown = dcc.Dropdown(
    id="region-dropdown-map",
    placeholder="Filter Regions",
    multi=True,
    options = ["East Midlands", "East of England", "London", "North East", "North West", "South East", "South West", "West Midlands", "Yorkshire and The Humber"]
)

table = create_ranking_table()

row_one = dbc.Row([
        dbc.Col([html.H1("Ranking Table")], width=12)
    ])

row_two = dbc.Row([
    dbc.Col([html.P(children=["Class", class_dropdown], style={"font-size": 20})], width=4),
    dbc.Col([html.P(children=["Year", year_dropdown], style={"font-size":20})], width=4),
    dbc.Col([html.P(children=["Region", region_dropdown], style={"font-size":20})], width=4)
])

row_three = dbc.Row([
    dbc.Col(children=table, width=12, id="ranking-table-div", style={'width': '100%'})
])

layout = dbc.Container([
    row_one,
    row_two,
    row_three
])

@callback(
    Output('ranking-table-div', 'children'),
    Input('class-dropdown-rank', 'value'),
    Input('year-dropdown-rank', 'value'),
    Input('region-dropdown-map', 'value')
)
def update_table(class_name, academic_year, selected_regions):
    table_created = create_ranking_table(class_name, academic_year, selected_regions)

    return table_created