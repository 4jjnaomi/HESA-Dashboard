from dash import html, register_page
import dash_bootstrap_components as dbc
from urllib.parse import unquote

def title(he_provider=None):
    decoded_he_provider = unquote(he_provider)
    return f"{decoded_he_provider}"

register_page(__name__, path_template="/university/<he_provider>", title=title)

def layout(he_provider=None):
    decoded_he_provider = unquote(he_provider)
    row_one = dbc.Row([
        dbc.Col([html.H1(f"Overview of {decoded_he_provider}")], width=12)
    ])
    return row_one