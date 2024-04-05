"""
This module contains the layout for the overview page of the app.
The overview page is where users can see how a specific university has
performed between 2018/19 - 2021/22 in various environmental categories.
Users can also analyse other universities using the sidebar.

The module defines the following components:
- create_sidebar: A function to create the sidebar with links to different universities.
- create_nav_links: A function to create navigation links for the sidebar.
- class_dropdown: A dropdown component for selecting the class.
- category_marker_dropdown: A dropdown component for selecting the category marker.
- line_chart: A line chart component for displaying the data.
- layout: The layout of the page.

The module also defines the following callback functions:
- toggle_collapse: A callback function to toggle the sidebar.
- update_nav: A callback function to update the sidebar navigation links based on the search input.
- update_category_marker_dropdown_overview: A callback function to
update the category marker dropdown based on the selected class.
- update_line_chart: A callback function to update the line
chart based on the selected class and category marker.
"""

from urllib.parse import unquote
from pathlib import Path

from dash import html, register_page, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from figures import create_line_chart, create_category_marker_options


def title(he_provider=None):
    """
    Returns the decoded HE provider name as a string.

    Args:
        he_provider (str): The encoded HE provider name.

    Returns:
        str: The decoded HE provider name.
    """
    decoded_he_provider = unquote(he_provider)
    return f"{decoded_he_provider}"


register_page(__name__, path_template="/university/<he_provider>", title=title)


def generate_sidebar_links():
    """
    Generates sidebar links for universities.

    Returns:
        A list of dictionaries, where each dictionary represents a sidebar link.
        Each dictionary has the following keys:
        - "children": The name of the university.
        - "href": The URL for the university's page.
        - "active": The active state of the link (e.g., "exact" for exact match).
    """
    data = Path(__file__).parent.parent.parent.joinpath('data', 'hei_data.csv')
    universities = pd.read_csv(data)['HE Provider']
    return [{"children": uni, "href": f"/university/{uni}", "active": "exact"} for uni in universities]

def create_sidebar():
    """
    Creates a sidebar component for the overview page.

    Returns:
        dbc.Nav: The sidebar component.
    """
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
    """
    Create navigation links for a Bootstrap Dash component.

    Args:
        links (list): A list of dictionaries representing the navigation links.
            Each dictionary should have the following keys:
            - "children": The text to display for the link.
            - "href": The URL to navigate to when the link is clicked.
            - "active": A boolean indicating whether the link should be active.

    Returns:
        list: A list of dbc.NavLink objects representing the navigation links.
    """
    return [dbc.NavLink(link["children"], href=link["href"], active=link["active"]) for link in links]


# Create the components
class_dropdown = dbc.Select(id="class-dropdown", options=[{"label": cls, "value": cls} for cls in ["Building and spaces", "Energy",
                            "Emissions and waste", "Transport and environment", "Finances and people"]], placeholder="Choose a class to see options for 'Category Marker'")

category_marker_dropdown = dbc.Select(
    id="category-marker-dropdown", options=[], placeholder="Choose a category marker to see a graph")

line_chart = create_line_chart(None, None, None)

# Define the layout of the page


def layout(he_provider=None):
    """
    Generates the layout for the overview page.

    Args:
        he_provider (str): The higher education provider.

    Returns:
        dbc.Container: The layout for the overview page.
    """
    decoded_he_provider = unquote(he_provider)
    universities = generate_sidebar_links()
    universities_list = [uni["children"] for uni in universities]

    # The standard rows for the overview page
    row_one = dbc.Row([dbc.Col([html.H1(f"{decoded_he_provider}")], width=12)])
    row_two = dbc.Row([dbc.Col(children=[html.P(f"Use this page to see how {decoded_he_provider} has performed between 2018/19 - 2012/22 in various environmental categories."), html.P(
        "You can analyse other universities using the button to the side.", style={"font-weight": "bold"})], width=12)])
    row_three = dbc.Row([dbc.Col([html.P(children=["Class", class_dropdown], style={"font-size": 20})], width=6), dbc.Col(
        [html.P(children=["Category Marker", category_marker_dropdown], style={"font-size": 20})], width=6)])
    row_four = dbc.Row([dbc.Col(
        children=[dcc.Graph(figure=line_chart, id='overview_line_chart')], width=12)])

    # The standard layout for the page
    page_layout = dbc.Container([dbc.Row([dbc.Col(create_sidebar(), width=2), dbc.Col(
        [row_one, row_two, row_three, row_four], width=10)])])

    # If the university does not exist in the database, display a message
    # to the user
    non_existent_uni_layout = dbc.Container([dbc.Row([dbc.Col(create_sidebar(), width=2), dbc.Col([html.H1("University not found"), html.P(
        "The university you are looking for does not exist in our database."), html.P("Please edit the url to choose a different university or click on a university from the sidebar.")], width=10)])])

    # Return the standard layout for the university if it exists, otherwise return a message
    return non_existent_uni_layout if decoded_he_provider not in universities_list else page_layout


@callback(Output("collapse", "is_open"), [Input("toggle", "n_clicks")], [State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    """
    Toggles the collapse state based on the value of `n`.

    Parameters:
    - n (bool): The value used to determine the new collapse state.
    - is_open (bool): The current collapse state.

    Returns:
    - bool: The new collapse state.
    """
    return not is_open if n else is_open


@callback(Output("sidebar-nav", "children"), [Input("search_input", "value")])
def update_nav(search_value):
    """
    Update the navigation links based on the search value.

    Args:
        search_value (str): The search value to filter the navigation links.

    Returns:
        list: The updated navigation links.
    """
    universities = generate_sidebar_links()
    links = universities if not search_value else [
        uni for uni in universities if search_value.lower() in uni["children"].lower()]
    return create_nav_links(links)


@callback(Output('category-marker-dropdown', 'options'), Output('category-marker-dropdown', 'value'), Input('class-dropdown', 'value'))
def update_category_marker_dropdown_overview(class_name):
    """
    Updates the category marker dropdown in the overview page.

    Args:
        class_name (str): The name of the class.

    Returns:
        tuple: A tuple containing the options for the dropdown and None.
    """
    # If no class name is selected, raise PreventUpdate to prevent updating the dropdown
    if not class_name:
        raise PreventUpdate
    options = create_category_marker_options(class_name)
    return options, None


@callback(Output('overview_line_chart', 'figure'), Input('class-dropdown', 'value'), Input('category-marker-dropdown', 'value'), Input('url', 'pathname'))
def update_line_chart(class_name, category_marker, pathname):
    """
    Update the line chart based on the selected class name, category marker, and pathname.

    Args:
        class_name (str): The selected class name.
        category_marker (str): The selected category marker.
        pathname (str): The pathname of the file.

    Returns:
        The updated line chart based on the selected parameters.
    """
    # If no class name is selected, raise PreventUpdate to prevent updating the line chart
    if not class_name:
        raise PreventUpdate
    # Decode the HE provider name from the pathname and create the line chart
    decoded_he_provider = unquote(pathname.split('/')[-1])
    return create_line_chart(decoded_he_provider, class_name, category_marker)
