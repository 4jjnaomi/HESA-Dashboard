from urllib.parse import unquote
from pathlib import Path

from dash import html, register_page, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
from pages.overview import layout as overview_layout

# Define the custom 404 error page layout
def custom_404_layout(pathname):
    return dbc.Container([
        html.H1("404 - Not Found"),
        html.P(f"The page '{pathname}' was not found. That university is not in the dataset."),
        dcc.Link("Return to homepage", href="/")
    ])

# Register the custom error page layout with Dash
register_page(__name__, name="404", path="/404", layout_callable=custom_404_layout)

# Define a callback to handle 404 errors
@callback(Output("content", "children"), 
          [Input("url", "pathname")])
def display_custom_error(pathname):
    data = Path(__file__).parent.parent.parent.joinpath('data','hei_data.csv')
    df = pd.read_csv(data)
    universities = df['HE Provider']

    if pathname == "/404":
        # Prevent infinite recursion
        raise PreventUpdate

    #If the url has /university/ in it, then we want to extract the HE provider value from the URL
    # Get the he_provider value from the URL
    if "/university/" in pathname:
        he_provider = unquote(pathname.split("/")[-1])
        # Check if he_provider is not in your dataset
        if he_provider not in universities:
            return custom_404_layout(pathname)
        else:
            # Return the normal layout if he_provider is valid
            return overview_layout(he_provider)