from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
from urllib.parse import unquote
from figures import create_line_chart

def title(he_provider=None):
    decoded_he_provider = unquote(he_provider)
    return f"{decoded_he_provider}"

register_page(__name__, path_template="/university/<he_provider>", title=title)

#Create a dropdown for the class
class_dropdown = dbc.Select(
    id="class-dropdown",  # id uniquely identifies the element, will be needed later
    options=["Building and spaces", "Energy", "Emissions and waste", "Transport and environment", "Finances and people"],
    value="Building and spaces"
)

#Create a dropdown for the category marker
category_marker_dropdown = dbc.Select(
    id="category-marker-dropdown",
    options=[],
    placeholder='Choose a category marker to see a graph'
)

line_chart = create_line_chart(None, None, None)

def layout(he_provider=None):
    decoded_he_provider = unquote(he_provider)
    row_one = dbc.Row([
        dbc.Col([html.H1(f"Overview of {decoded_he_provider}")], width=12)
    ])
    row_two = dbc.Row([
        dbc.Col([html.P(children=["Class", class_dropdown], style={"font-size": 20})], width=6),
        dbc.Col([html.P(children=["Category Marker", category_marker_dropdown], style={"font-size": 20})], width=6)
    ])
    row_three = dbc.Row([
        dbc.Col(children=[dcc.Graph(figure=line_chart, id='overview_line_chart')], width=12)
    ])
    return row_one, row_two, row_three