from dash import html, register_page, dcc, get_asset_url
import dash_bootstrap_components as dbc
from figures import create_ranking_table


# Register the page with the Dash app
register_page(__name__, name="Ranking Table", path='/ranking_table')

class_dropdown = dbc.Select(
    id="class-dropdown",  # id uniquely identifies the element, will be needed later
    options=["Buildings and spaces", "Energy", "Emissions and waste", "Transport and environment", "Finances and people"],
    value="Building and spaces"
)

year_dropdown = dbc.Select(
    id="year-dropdown",
    options=[ "2018/19", "2019/20", "2020/21", "2021/22"],  
    value="2021/22"
)

table = create_ranking_table("Transport and environment", "2021/22")

row_one = dbc.Row([
        dbc.Col([html.H1("Ranking Table")], width=12)
    ])

row_two = dbc.Row([
    dbc.Col([html.P(children=["Class", class_dropdown], style={"font-size": 20})], width=6),
    dbc.Col([html.P(children=["Year", year_dropdown], style={"font-size":20})], width=6)
])

row_three = dbc.Row([
    dbc.Col(children=table, width=12)
])

layout = dbc.Container([
    row_one,
    row_two,
    row_three
])