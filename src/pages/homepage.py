"""
This module contains the code for the homepage of the England HEI Environmental Dashboard.

The homepage displays a map of Higher Education Institutions (HEIs) in England and provides options to filter the HEIs by region and view additional information about each HEI.

The module defines functions for creating buttons, dropdowns, rows, and the overall layout of the homepage. It also includes callback functions for updating the map and displaying information cards based on user interactions.
"""

from pathlib import Path
from dash import html, register_page, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from figures import create_scatter_mapbox, create_card

# Register the page with the Dash app
register_page(__name__, name="Homepage", path='/')

# Load the data
raw_data = Path(__file__).parent.parent.parent.joinpath('data', 'hei_data.csv')
data_df = pd.read_csv(raw_data)


def create_button(text, href):
    """
    Create a button with the given text and href.

    Args:
        text (str): The text to display on the button.
        href (str): The URL to navigate to when the button is clicked.

    Returns:
        html.Div: The button wrapped in a div element.
    """
    if text == "Ranking Table":
        description = "See the ranking of all HEIs"
    elif text == "HEI overview":
        description = "Analyse the performance of a specific HEI"
    else:
        description = "Compare the performance of multiple HEIs"
    return html.Div(
        dbc.Button(
            [html.H6(text), html.P(description)],
            color="primary",
            href=href,
            style={"height": "70px"},
            id=f"{text.lower().replace(' ', '_')}-button"
        ),
        className="d-grid gap-2 mx-auto"
    )


def create_dropdown(id1, options, placeholder, multi=False, optionHeight=50, maxHeight=350):
    """
    Create a dropdown component with the given options and placeholder.

    Args:
        id1 (str): The ID of the dropdown component.
        options (list): The list of options to display in the dropdown.
        placeholder (str): The text to display when no option is selected.
        multi (bool, optional): Whether multiple options can be selected. Defaults to False.
        optionHeight (int, optional): The height of each option in pixels. Defaults to 50.
        maxHeight (int, optional): The maximum height of the dropdown menu in pixels. Defaults to 350.

    Returns:
        dcc.Dropdown: The dropdown component.
    """
    return dcc.Dropdown(
        id=id1,
        options=options,
        placeholder=placeholder,
        multi=multi,
        optionHeight=optionHeight,
        maxHeight=maxHeight
    )


def create_row(content):
    """
    Create a row with the given content.

    Args:
        content (list): The list of elements to include in the row.

    Returns:
        dbc.Row: The row component.
    """
    return dbc.Row(content, style={"padding-top": "20px"})


def layout():
    """
    Create the layout for the homepage.

    Returns:
        dbc.Container: The container component containing the homepage layout.
    """
    # Create the options for the dropdowns
    regions = [{'label': region, 'value': region}
               for region in data_df['Region of HE provider'].unique()]
    heis = [{'label': hei, 'value': hei}
            for hei in data_df['HE Provider'].unique()]
    
    # Create the buttons
    button1 = create_button("Ranking Table", "/ranking_table")
    button2 = create_button(
        "HEI overview", "/university/Anglia Ruskin University")
    button3 = create_button("HEI comparison", "/comparison")

    # Create the dropdowns
    region_dropdown = create_dropdown(
        "region-dropdown-map", regions, "Select Region(s)", multi=True)
    hei_dropdown = create_dropdown(
        "hei-dropdown-map", heis, "Select HEI(s)", multi=True)

    # Create the rows
    row_one = html.Div(
        [html.H1('Welcome to the England HEI Environmental Dashboard')])
    row_two = html.Div([html.P(
        'This dashboard provides an overview of the environmental performance of Higher Education Institutions (HEIs) in England.')])
    row_three = create_row([dbc.Col(button1, width=4), dbc.Col(
        button2, width=4), dbc.Col(button3, width=4)]) # 3 buttons in a row

    row_four = create_row([
        dbc.Col(children=[
            html.P("The map shows the location of HEIs in England. Hover over a point to see more information about the HEI.", style={
                   "font-size": "14px"}),
            html.P(children=["Filter Regions", region_dropdown],
                   style={"background-color": "lightgrey"}),
            html.P(["Filter HEIs", hei_dropdown], style={"background-color": "lightgrey"})], width=2), # filters on the left
        dbc.Col(children=[dcc.Graph(
            figure=create_scatter_mapbox(), id='england_map')], width=8), # map in the middle
        dbc.Col(children=[html.Div(id='card')], width=2) # card on the right
    ])

    layout_page = dbc.Container([row_one, row_two, row_three, row_four])
    return layout_page


@callback(
    Output('hei-dropdown-map', 'options'),
    Input('region-dropdown-map', 'value')
)
def update_hei_options(selected_regions):
    """
    Update the options of the HEI dropdown based on the selected regions.

    Args:
        selected_regions (list): The list of selected regions.

    Returns:
        list: The updated options for the HEI dropdown.
    """
    if selected_regions: # if regions are selected, show only HEIs in those regions
        heis_in_selected_regions = data_df[data_df['Region of HE provider'].isin(
            selected_regions)]['HE Provider']
        hei_options = [{'label': hei, 'value': hei}
                       for hei in heis_in_selected_regions]
    else: # if no regions are selected, show all HEIs
        hei_options = [{'label': hei, 'value': hei}
                       for hei in data_df['HE Provider']]

    return hei_options


@callback(
    Output('england_map', 'figure'),
    [Input('region-dropdown-map', 'value'),
     Input('hei-dropdown-map', 'value')]
)
def update_map(selected_regions, selected_heis):
    """
    Update the map figure based on the selected regions and HEIs.

    Args:
        selected_regions (list): The list of selected regions.
        selected_heis (list): The list of selected HEIs.

    Returns:
          go.Figure: the updated Plotly graph objects Scatter mapbox plot with the filters applied if applicable.
    """
    ctx = callback_context # get the context of the callback
    if ctx.triggered: # if the callback was triggered
        prop_id = ctx.triggered[0]['prop_id']
        # check which dropdown was changed
        # if the region dropdown was changed, update the map with the selected regions
        if prop_id == 'region-dropdown-map.value':
            return create_scatter_mapbox(region=selected_regions)
        # if the HEI dropdown was changed, update the map with the selected HEIs
        elif prop_id == 'hei-dropdown-map.value':
            return create_scatter_mapbox(hei=selected_heis)
    return create_scatter_mapbox()  # default to showing all data


@callback(
    Output('card', 'children'),
    Input('england_map', 'hoverData')
)
def display_card(hover_data):
    """
    Display the card with information about the selected HEI.

    Args:
        hover_data (dict): The hover data from the map.

    Returns:
        card (dbc.Card): A Bootstrap Card component containing information about the university being hovered on.
    """
    # if a point is hovered over, get the UKPRN and create a card for that HEI
    if hover_data is not None:
        ukprn = hover_data['points'][0]['customdata']
        if ukprn is not None:
            return create_card(ukprn)
