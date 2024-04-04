from urllib.parse import unquote
from pathlib import Path

from dash import html, register_page, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
from figures import create_line_chart, create_category_marker_options


def title(he_provider=None):
    decoded_he_provider = unquote(he_provider)
    return f"{decoded_he_provider}"


register_page(__name__, path_template="/university/<he_provider>", title=title)


def generate_sidebar_links():
    data = Path(__file__).parent.parent.parent.joinpath('data', 'hei_data.csv')
    universities = pd.read_csv(data)['HE Provider']
    return [{"children": uni, "href": f"/university/{uni}", "active": "exact"} for uni in universities]


def create_sidebar():
    universities = generate_sidebar_links()
    instructions = html.P("Click on a HEI to go to its overview page.", className="lead", style={
                          "font-size": 15, "padding": 10, "font-weight": "bold"})
    search_bar = dbc.Input(id="search_input", type="search",
                           placeholder="Search for a HEI", className="mb-3", style={"padding": 10})
    collapse = dbc.Collapse(children=[search_bar, dbc.Nav(create_nav_links(
        universities), vertical=True, id="sidebar-nav")], id="collapse")
    toggle_button = dbc.Button(
        "Choose a HEI", id="toggle", className="mb-3", color="primary")
    return dbc.Nav([instructions, toggle_button, collapse], vertical=True)


def create_nav_links(links):
    return [dbc.NavLink(link["children"], href=link["href"], active=link["active"]) for link in links]


class_dropdown = dbc.Select(id="class-dropdown", options=[{"label": cls, "value": cls} for cls in ["Building and spaces", "Energy",
                            "Emissions and waste", "Transport and environment", "Finances and people"]], placeholder="Choose a class to see options for 'Category Marker'")

category_marker_dropdown = dbc.Select(
    id="category-marker-dropdown", options=[], placeholder="Choose a category marker to see a graph")

line_chart = create_line_chart(None, None, None)


def layout(he_provider=None):
    decoded_he_provider = unquote(he_provider)
    universities = generate_sidebar_links()
    universities_list = [uni["children"] for uni in universities]

    row_one = dbc.Row([dbc.Col([html.H1(f"{decoded_he_provider}")], width=12)])
    row_two = dbc.Row([dbc.Col(children=[html.P(f"Use this page to see how {decoded_he_provider} has performed between 2018/19 - 2012/22 in various environmental categories."), html.P(
        "You can analyse other universities using the button to the side.", style={"font-weight": "bold"})], width=12)])
    row_three = dbc.Row([dbc.Col([html.P(children=["Class", class_dropdown], style={"font-size": 20})], width=6), dbc.Col(
        [html.P(children=["Category Marker", category_marker_dropdown], style={"font-size": 20})], width=6)])
    row_four = dbc.Row([dbc.Col(
        children=[dcc.Graph(figure=line_chart, id='overview_line_chart')], width=12)])
    page_layout = dbc.Container([dbc.Row([dbc.Col(create_sidebar(), width=2), dbc.Col(
        [row_one, row_two, row_three, row_four], width=10)])])
    non_existent_uni_layout = dbc.Container([dbc.Row([dbc.Col(create_sidebar(), width=2), dbc.Col([html.H1("University not found"), html.P(
        "The university you are looking for does not exist in our database."), html.P("Please edit the url to choose a different university or click on a university from the sidebar.")], width=10)])])
    return non_existent_uni_layout if decoded_he_provider not in universities_list else page_layout


@callback(Output("collapse", "is_open"), [Input("toggle", "n_clicks")], [State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    return not is_open if n else is_open


@callback(Output("sidebar-nav", "children"), [Input("search_input", "value")])
def update_nav(search_value):
    universities = generate_sidebar_links()
    links = universities if not search_value else [
        uni for uni in universities if search_value.lower() in uni["children"].lower()]
    return create_nav_links(links)


@callback(Output('category-marker-dropdown', 'options'), Output('category-marker-dropdown', 'value'), Input('class-dropdown', 'value'))
def update_category_marker_dropdown_overview(class_name):
    if not class_name:
        raise PreventUpdate
    options = create_category_marker_options(class_name)
    return options, None


@callback(Output('overview_line_chart', 'figure'), Input('class-dropdown', 'value'), Input('category-marker-dropdown', 'value'), Input('url', 'pathname'))
def update_line_chart(class_name, category_marker, pathname):
    if not class_name:
        raise PreventUpdate
    decoded_he_provider = unquote(pathname.split('/')[-1])
    return create_line_chart(decoded_he_provider, class_name, category_marker)
