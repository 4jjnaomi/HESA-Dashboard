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
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags, use_pages=True, suppress_callback_exceptions=True)

# From https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Ranking Table", href=dash.page_registry['pages.ranking_table']['path'])),
        dbc.NavItem(dbc.NavLink("HEI Comparison", href=dash.page_registry['pages.comparison']['path'])),
    ],
    brand="UK HEI Environmental Dashboard",
    brand_href="/",
    brand_style={"font-size": 40, "font-weight": "bold"},
    color="primary",
    dark=True,
)

app.layout = html.Div([
    # Nav bar
    navbar,
    # Area where the page content is displayed
    dash.page_container,
    dcc.Location(id='url', refresh=True)
])

if __name__ == '__main__':
    app.run(debug=True, port=8051)