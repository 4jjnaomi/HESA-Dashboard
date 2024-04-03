from urllib.parse import unquote
from pathlib import Path

from dash import html, register_page, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
from figures import create_line_chart, create_category_marker_options
from dash.exceptions import PreventUpdate

def title(he_provider=None):
    decoded_he_provider = unquote(he_provider)
    return f"{decoded_he_provider}"

register_page(__name__, path_template="/university/<he_provider>", title=title)

def generate_sidebar_links():
    data = Path(__file__).parent.parent.parent.joinpath('data','hei_data.csv')
    df = pd.read_csv(data)
    universities = df['HE Provider']
    sidebar_links = []
    for uni in universities:
        sidebar_links.append(
            {"children": uni, 
             "href": f"/university/{uni}", 
             "active": "exact"}
        )
    return sidebar_links

def sidebar():
    sidebar_links = generate_sidebar_links()

    # Create list of dbc.NavLink components
    nav_links = [
        dbc.NavLink(
            link["children"],
            href=link["href"],
            active=link["active"]
        )
        for link in sidebar_links
    ]

    instructions = html.P("Click on a HEI to go to its overview page.", className="lead", style={"font-size": 15, "padding": 10, "font-weight": "bold"})

    search_bar = dbc.Input(
        id = "search_input",
        type="search",
        placeholder="Search for a HEI",
        className="mb-3",
        style=({"padding": 10})
    )

    collapse = dbc.Collapse(
        children=[search_bar,
                dbc.Nav(nav_links, vertical=True, id="sidebar-nav")],
                id = "collapse")

    toggle_button = dbc.Button(
        "Choose a HEI", 
        id="toggle", 
        className="mb-3", 
        color="primary"
    )

    sidebar_layout = dbc.Nav(
        [instructions, toggle_button, collapse],
        vertical=True,
    )

    return sidebar_layout

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
    data = Path(__file__).parent.parent.parent.joinpath('data','hei_data.csv')
    df = pd.read_csv(data)
    universities = df['HE Provider']   
    row_one = dbc.Row([
        dbc.Col([html.H1(f"{decoded_he_provider}")], width=12)
    ])
    row_two = dbc.Row([
        dbc.Col(children = [html.P(f"Use this page to see how {decoded_he_provider} has performed between 2018/19 - 2012/22 in various environmental categories."), html.P("You can analyse other universities using the button to the side.", style={"font-weight": "bold"})], width=12)
    ])
    row_three = dbc.Row([
        dbc.Col([html.P(children=["Class", class_dropdown], style={"font-size": 20})], width=6),
        dbc.Col([html.P(children=["Category Marker", category_marker_dropdown], style={"font-size": 20})], width=6)
    ])
    row_four = dbc.Row([
        dbc.Col(children=[dcc.Graph(figure=line_chart, id='overview_line_chart')], width=12)
    ])
    page_layout = dbc.Container([
        dbc.Row([
            dbc.Col(sidebar(), width=2),
            dbc.Col([
                row_one,
                row_two,
                row_three,
                row_four
            ], width=10)
        ])
    ])
    non_existent_uni_layout = dbc.Container([
        dbc.Row([
            dbc.Col(sidebar(), width=2),
            dbc.Col([
                html.H1("University not found"),
                html.P("The university you are looking for does not exist in our database."),
                html.P("Please edit the url to choose a different university or click on a university from the sidebar.")
            ], width=10)
        ])
    ])
    #Not traditional error handling
    if decoded_he_provider not in universities.values:
        return non_existent_uni_layout        
    else:
        return page_layout

@callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("sidebar-nav", "children"),
    [Input("search_input", "value")]
)
def update_nav(search_value):
    universities = generate_sidebar_links()
    
    if not search_value:
        nav_links = [
            dbc.NavLink(
                uni["children"],
                href=uni["href"],
                active=uni["active"]
            )
            for uni in universities
        ]
        return nav_links
    
    filtered_universities = [uni for uni in universities if search_value.lower() in uni["children"].lower()]
    
    nav_links = [
        dbc.NavLink(
            uni["children"],
            href=uni["href"],
            active=uni["active"]
        )
        for uni in filtered_universities
    ]
    
    return nav_links

@callback(
    Output('category-marker-dropdown', 'options'),
    Output('category-marker-dropdown', 'value'),
    Input('class-dropdown', 'value')
)

def update_category_marker_dropdown_overview(class_name):
    if not class_name:
        raise PreventUpdate

    options = create_category_marker_options(class_name)
    return options, None

@callback(
    Output('overview_line_chart', 'figure'),
    Input('class-dropdown', 'value'),
    Input('category-marker-dropdown', 'value'),
    Input('url', 'pathname')
)

def update_line_chart(class_name, category_marker, pathname):
    if not class_name:
        raise PreventUpdate
    
    hei_name = pathname.split('/')[-1]
    decoded_he_provider = unquote(hei_name)
    return create_line_chart(decoded_he_provider, class_name, category_marker)

