"""
This script defines a Dash application that displays an HEI Environmental Dashboard.
It includes functions to create a navigation bar and a footer, as well as the layout of the application.
"""

import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap
# components (dbc)
external_stylesheets = [dbc.themes.MINTY]

# Define a variable that contains the meta tags
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet variable to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets,
           meta_tags=meta_tags, use_pages=True, suppress_callback_exceptions=True)

# Function to create a navigation bar with links to different pages
def create_navbar():
    """
    Creates a navigation bar with links to different pages.
    Returns:
        dbc.NavbarSimple: The navigation bar component.
    """
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(
                "Ranking Table", href=dash.page_registry['pages.ranking_table']['path'])),
            dbc.NavItem(dbc.NavLink("HEI Comparison",
                        href=dash.page_registry['pages.comparison']['path'])),
        ],
        brand="HEI Environmental Dashboard",
        brand_href="/",
        brand_style={"font-size": 40, "font-weight": "bold"},
        color="primary",
        dark=True,
    )

# Function to create the footer
def create_footer():
    """
    Creates the footer of the application.
    Returns:
        dbc.Container: The container component containing the footer.
    """
    return dbc.Container(
        dbc.Row(
            [dbc.Col(
                html.Div([
                    html.P("Data Source: HESA", style={
                        "color": "white"}, className="my-0"),
                    html.P([" Data file canonical link: ", html.A("https://www.hesa.ac.uk/data-and-analysis/estates/data.csv",
                           href="https://www.hesa.ac.uk/data-and-analysis/estates/data.csv", style={"color": "white"})], style={"color": "white"}, className="my-0"),
                    html.P(" Data file license: Creative Commons Attribution 4.0 International Licence", style={
                           "color": "white"}, className="my-0")
                ]),
                width=6
            )
            ],
            justify="center"
        ),
        fluid=True,
        style={"text-align": "center"}, className="bg-primary mt-3"
    )


# Define the layout of the application
app.layout = html.Div([
    # Nav bar
    create_navbar(),
    # Area where the page content is displayed
    dash.page_container,
    # Footer
    create_footer(),
    dcc.Location(id='url', refresh=True)
])

if __name__ == '__main__':
    app.run(debug=True, port=8051)
