"""
This module contains the layout and callbacks for the HEI Comparison page.

The page allows users to compare the performance of different Higher 
Education Institutions (HEIs) in various environmental categories. 
Users can select the year, class, category marker, category, 
and HEIs to compare on a bar chart.

The module defines the following components:
- create_dropdown: A function to create a dropdown component.
- year_dropdown: A dropdown component for selecting the year(s).
- class_dropdown: A dropdown component for selecting the class.
- category_marker_dropdown: A dropdown component for selecting 
the category marker.
- category_dropdown: A dropdown component for selecting the category.
- hei_dropdown: A dropdown component for selecting the HEIs to compare.
- layout: The layout of the page.

The module also defines the following callback functions:
- update_category_marker_dropdown_comparison: A callback function 
to update the category marker dropdown based on the selected class.
- update_category_dropdown_comparison: A callback function to 
update the category dropdown based on the selected category marker.
- update_bar_chart: A callback function to update the bar chart 
based on the selected HEIs, year(s), and category.
"""

from pathlib import Path
from dash import html, register_page, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from figures import create_category_marker_options, create_category_options, create_bar_chart

# Register the page with the Dash app
register_page(__name__, name="HEI Comparison", path='/comparison')

def create_dropdown(id1, options, placeholder, multi=False, dropdown_type='dcc'):
    """
    Create a dropdown component based on the specified dropdown_type.

    Parameters:
    - id1 (str): The ID of the dropdown component.
    - options (list): A list of dictionaries representing the dropdown options.
    - placeholder (str): The placeholder text to display when no option is selected.
    - multi (bool, optional): Whether the dropdown allows multiple selections. Defaults to False.
    - dropdown_type (str, optional): The type of dropdown component to create. Valid values are 'dcc' (for dcc.Dropdown) and 'dbc' (for dbc.Select). Defaults to 'dcc'.

    Returns:
    - The created dropdown component.

    Raises:
    - ValueError: If an invalid dropdown_type is provided.

    """
    if dropdown_type == 'dcc':
        return dcc.Dropdown(
            id=id1,
            options=options,
            placeholder=placeholder,
            multi=multi
        )
    elif dropdown_type == 'dbc':
        return dbc.Select(
            id=id1,
            options=options,
            placeholder=placeholder
        )
    else:
        raise ValueError("Invalid dropdown_type. Use 'dcc' or 'dbc'.")


year_dropdown = create_dropdown(
    "year-dropdown-comparison",
    options=[{"label": year, "value": year}
             for year in ["2018/19", "2019/20", "2020/21", "2021/22"]],
    placeholder="Select Year(s)",
    multi=True
)

class_dropdown = create_dropdown(
    "class-dropdown-comparison",
    options=[{"label": cls, "value": cls} for cls in ["Building and spaces", "Energy",
                                                      "Emissions and waste", "Transport and environment", "Finances and people"]],
    placeholder="Choose a class to see available category markers",
    dropdown_type='dbc'
)

category_marker_dropdown = create_dropdown(
    "category-marker-dropdown-comparison",
    options=[],
    placeholder="Choose a category marker to see available categories",
    dropdown_type='dbc'
)

category_dropdown = create_dropdown(
    "category-dropdown-comparison",
    options=[],
    placeholder="Choose a category",
    dropdown_type='dbc'
)


def create_hei_dropdown():
    """
    Create a dropdown component for selecting HEI(s) to compare on the graph.

    Returns:
        A dropdown component with options to select HEI(s) for comparison.
    """
    # Load the dataset
    data_path = Path(__file__).parent.parent.parent.joinpath(
        'data', 'hei_data.csv')
    data_df = pd.read_csv(data_path)
    hei_providers = [{"label": provider, "value": provider}
                     for provider in data_df['HE Provider']]
    return create_dropdown(
        "hei-dropdown-comparison",
        options=hei_providers,
        placeholder="Select HEI(s) to compare on the graph",
        multi=True
    )


hei_dropdown = create_hei_dropdown()

row_one = dbc.Row([
    dbc.Col([html.H1("HEI Comparison")], width=12)
])

row_two = dbc.Row([
    dbc.Col([html.P("To see a bar chart, you need to select one or more academic years from the dropdown. You will then need to choose a category marker and then select a category. You will then need to choose one or more HEIs to see how they perform in that category metric.")], width=12)
])

row_three = dbc.Row([
    dbc.Col(children=[
        html.P(children=["Year", year_dropdown]),
        html.P(children=["Class", class_dropdown]),
        html.P(children=["Category Marker", category_marker_dropdown]),
        html.P(children=["Category", category_dropdown]),
        html.P(children=["HEI", hei_dropdown])
    ], width=4),
    dbc.Col(children=[dcc.Graph(id='bar_chart')], width=8),
    html.Script('''
        // Get the dropdown menu element
        var dropdownMenu = document.getElementById('Select-menu-outer');

        // Add an event listener to the dropdown menu to stop propagation of click events
        dropdownMenu.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    ''')
])

layout = dbc.Container([
    row_one,
    row_two,
    row_three
])


@callback(
    Output("category-marker-dropdown-comparison", "options"),
    Output("category-marker-dropdown-comparison", "value"),
    Input("class-dropdown-comparison", "value")
)
def update_category_marker_dropdown_comparison(class_name):
    """
    Updates the category marker dropdown in the comparison page.

    Args:
        class_name (str): The name of the class.

    Returns:
        tuple: A tuple containing the options for the dropdown and None.

    Raises:
        PreventUpdate: If the class name is missing or empty.
    """
    if not class_name:
        raise PreventUpdate
    options = create_category_marker_options(class_name)
    return options, None


@callback(
    Output("category-dropdown-comparison", "options"),
    Output("category-dropdown-comparison", "value"),
    Input("category-marker-dropdown-comparison", "value"),
)
def update_category_dropdown_comparison(category_marker):
    """
    Updates the category dropdown options based on the selected category marker.

    Args:
        category_marker (str): The selected category marker.

    Returns:
        tuple: A tuple containing the updated dropdown options and None.

    Raises:
        PreventUpdate: If the category marker is missing or empty.
    """
    if not category_marker:
        raise PreventUpdate
    options = create_category_options(category_marker)
    return options, None


@callback(
    Output('bar_chart', 'figure'),
    Input('hei-dropdown-comparison', 'value'),
    Input('year-dropdown-comparison', 'value'),
    Input('category-dropdown-comparison', 'value')
)
def update_bar_chart(hei, year, category):
    """
    Update the bar chart based on the selected height, year, and category.

    Parameters:
    hei (float): The height value for the bar chart.
    year (int): The year value for the bar chart.
    category (str): The category value for the bar chart.

    Returns:
    fig: A plotly express bar chart figure object.

    Raises:
    PreventUpdate: If any of the input parameters are missing or empty.
    """
    if not hei or not year or not category:
        raise PreventUpdate
    return create_bar_chart(hei, year, category)
