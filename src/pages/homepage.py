from dash import html, register_page


# Register the page with the Dash app
register_page(__name__, name="Homepage", path='/')

layout =  html.Div([
    html.Div(children='Home page to come soon!')
])