from dash import html, register_page, dcc, get_asset_url
import dash_bootstrap_components as dbc


# Register the page with the Dash app
register_page(__name__, name="Homepage", path='/')

layout =  html.Div([
    html.Div(children='Hello World')
])