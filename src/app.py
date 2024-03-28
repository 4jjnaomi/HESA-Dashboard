from urllib.parse import unquote
import dash
from dash import html, dcc, Dash, Input, Output
import dash_bootstrap_components as dbc
from figures import create_ranking_table, create_card, create_category_marker_options, create_line_chart



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
        dbc.NavItem(dbc.NavLink("Map View", href=dash.page_registry['pages.map_view']['path'])),
        dbc.NavItem(dbc.NavLink("Ranking Table", href=dash.page_registry['pages.ranking_table']['path'])),
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

@app.callback(
    Output('ranking-table-div', 'children'),
    Input('class-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_table(class_name, academic_year):
    return create_ranking_table(class_name, academic_year)

@app.callback(
    Output('card', 'children'),
    Input('england_map', 'hoverData')
)
def display_card(hover_data):
    if hover_data is not None:
        ukprn = hover_data['points'][0]['customdata'][0]
        if  ukprn is not None:
            return create_card(ukprn)
           
@app.callback(
    Output('category-marker-dropdown', 'options'),
    Input('class-dropdown', 'value')
)

def update_category_dropdown(class_name):
    return create_category_marker_options(class_name)

@app.callback(
    Output('overview_line_chart', 'figure'),
    Input('class-dropdown', 'value'),
    Input('category-marker-dropdown', 'value'),
    Input('url', 'pathname')
)

def update_line_chart(class_name, category_marker, pathname):
    hei_name = pathname.split('/')[-1]
    decoded_he_provider = unquote(hei_name)
    return create_line_chart(decoded_he_provider, class_name, category_marker)



if __name__ == '__main__':
    app.run(debug=True, port=8051)