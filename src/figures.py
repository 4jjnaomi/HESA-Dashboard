"""
This module contains functions for creating various visualizations and data manipulation operations.

Functions:
- load_data(file_path, columns): Loads data from a CSV file and 
returns a DataFrame with specified columns.
- filter_dataframe(data_df, filters): Filters a DataFrame based on 
specified column-value pairs.
- create_scatter_mapbox(region=None, hei=None): Creates a scatter 
mapbox plot of HE providers' locations.
- filter_data_for_table(data_df, ClassName, acedemic_year, 
selected_regions): Filters data for creating a table based on 
specified criteria.
- format_number(number): Formats a number with appropriate suffixes 
(e.g., k, M, B).
- create_card(ukprn): Creates a card with key metrics for a specific HE provider.
- create_line_chart(hei=None, Class=None, category_marker=None): Creates
a line chart showing trends of categories for a specific HE provider and class.
- create_options_from_data(data_df, column): Creates a list of 
options from unique values in a DataFrame column.
- create_bar_chart(hei=None, year=None, category=None): Creates a 
bar chart showing values for a specific HE provider, year, and category.
- create_ranking_table(ClassName=None, academic_year=None, selected_regions=None): Creates a ranking table based on 
specified criteria.
- create_category_marker_options(class_name): Creates a list of category marker options for a specific class.
- create_category_options(category_marker): Creates a list of category 
options for a specific category marker.
"""

from pathlib import Path
from urllib.parse import quote
import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


def load_data(file_path, columns):
    """
    Load data from a CSV file and return a DataFrame with specified columns.

    Parameters:
    file_path (str): The path to the CSV file.
    columns (list): A list of column names to be included in the DataFrame.

    Returns:
    pandas.DataFrame: A DataFrame containing the specified columns from the CSV file.
    """
    data_df = pd.read_csv(file_path, usecols=columns)
    return data_df


def filter_dataframe(data_df, filters):
    """
    Filters a pandas DataFrame based on the given filters.

    Args:
        data_df (pandas.DataFrame): The DataFrame to be filtered.
        filters (dict): A dictionary where the keys are column 
        names and the values are lists of values to filter on.

    Returns:
        pandas.DataFrame: The filtered DataFrame.

    Example:
        >>> data = pd.DataFrame({'A': [1, 2, 3, 4], 'B': ['a', 'b', 'c', 'd']})
        >>> filters = {'A': [2, 4]}
        >>> filtered_data = filter_dataframe(data, filters)
        >>> print(filtered_data)
           A  B
        1  2  b
        3  4  d
    """
    for column, values in filters.items():
        data_df = data_df[data_df[column].isin(values)]
    return data_df


def create_scatter_mapbox(region=None, hei=None):
    """
    Create a scatter mapbox plot of HE providers' locations.

    Args:
        region (str, optional): Filter the plot by region of HE provider. Defaults to None.
        hei (str, optional): Filter the plot by HE provider. Defaults to None.

    Returns:
        go.Figure: Plotly graph objects Scatter mapbox plot.
    """
    # Load HEI data
    hei_data = Path(__file__).parent.parent.joinpath('data', 'hei_data.csv')
    cols = ['UKPRN', 'HE Provider', 'Region of HE provider', 'lat', 'lon']
    df_loc = load_data(hei_data, cols)
    # Filter data based on region and HEI
    if region:
        df_loc = filter_dataframe(df_loc, {'Region of HE provider': region})
    if hei:
        df_loc = filter_dataframe(df_loc, {'HE Provider': hei})

    # Assign colors to regions
    regions = df_loc['Region of HE provider'].unique()
    colors = px.colors.qualitative.Set3[:len(regions)]
    color_scale = {region: color for region, color in zip(regions, colors)}

    # Create the scatter mapbox plot
    fig = go.Figure()
    added_regions = {}

    # Add traces for each HE provider
    for _, row in df_loc.iterrows():
        region = row['Region of HE provider']
        trace_settings = dict(lat=[row['lat']], lon=[row['lon']], mode='markers',
                              marker=dict(
                                  size=12, color=color_scale[region], opacity=0.7),
                              text=row['HE Provider'], hoverinfo='text',
                              # Custom data to store UKPRN for linking to university page
                              customdata=[row['UKPRN']])
        # Check if region has already been added to the plot
        if region not in added_regions:
            # Add trace with region name for legend
            trace_settings['name'] = region
            added_regions[region] = True
        # Hide legend for subsequent traces
        else:
            trace_settings['showlegend'] = False

        # Add trace to the figure
        fig.add_trace(go.Scattermapbox(**trace_settings))

    # Update layout
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.8,
                      mapbox_center={
                          # Center map on average location
                          "lat": df_loc['lat'].mean(), "lon": df_loc['lon'].mean()},
                      margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=800, height=370,
                      legend_title_text='Region', showlegend=True)
    return fig


def filter_data_for_table(data_df, ClassName, acedemic_year, selected_regions):
    """
    Filters the data dataframe based on the given class name, academic year, and selected regions.

    Args:
        data_df (pandas.DataFrame): The input dataframe containing the data.
        ClassName (str): The class name to filter by.
        acedemic_year (str): The academic year to filter by.
        selected_regions (list): The list of selected regions to filter by.

    Returns:
        pandas.DataFrame: The filtered dataframe.

    """
    data_df = data_df[(data_df['Class'] == ClassName) & (
        data_df['Academic Year'] == acedemic_year)]
    if selected_regions:
        data_df = filter_dataframe(
            data_df, {'Region of HE provider': selected_regions})
    return data_df


def format_number(number):
    """
    Formats a number by adding a suffix to represent its magnitude.

    Args:
        number (float): The number to be formatted.

    Returns:
        str: The formatted number with a suffix representing its magnitude.

    Example:
        >>> format_number(1234567)
        '1.235M'
    """
    suffixes = ['', 'k', 'M', 'B']
    magnitude = 0
    # Divide the number by 1000 until it is less than 1000
    while abs(number) >= 1000:
        # Increase the magnitude index
        magnitude += 1
        # Divide the number by 1000
        number /= 1000.0
    # Round the number to 3 decimal places
    return f"{round(number, 3)}{suffixes[magnitude]}"


def create_card(ukprn):
    """
    Create a card component for a university based on the given UKPRN.

    Parameters:
    - ukprn (str): The UKPRN (UK Provider Reference Number) of the university.

    Returns:
    - card (dbc.Card): A Bootstrap Card component containing information about the university.

    """
    hei_data_path = Path(__file__).parent.parent.joinpath(
        'data', 'hei_data.csv')
    data_df = load_data(hei_data_path, ['HE Provider', 'UKPRN'])
    # Filter the row with the given UKPRN
    row = data_df[data_df['UKPRN'] == ukprn]
    ukprn_value, he_name = row.iloc[0]

    # Load entry data
    entry_data_path = Path(__file__).parent.parent.joinpath(
        'data', 'entry_data.csv')
    entry_data_df = load_data(
        entry_data_path, ['HE Provider', 'Category', 'Value', 'Academic Year'])
    # Filter the entries for the given HE provider and academic year
    he_entries = entry_data_df[(entry_data_df['HE Provider'] == he_name) & (
        entry_data_df['Academic Year'] == '2021/22')]

    # Check if he_entries DataFrame is empty before accessing its elements
    formatted_income = "No data"
    formatted_emissions = "No data"
    if not he_entries.empty:
        # Access elements and calculate formatted_income and formatted_emissions
        formatted_income_series = he_entries[he_entries['Category']
                                             == 'Total income (£)']['Value']
        formatted_emissions_series = he_entries[he_entries['Category']
                                                == 'Total scope 1 and 2 carbon emissions (Kg CO2e)']['Value']
        # Check if the series are not empty before accessing the first element
        if not formatted_income_series.empty:
            formatted_income = format_number(
                float(formatted_income_series.iloc[0]))
        if not formatted_emissions_series.empty:
            formatted_emissions = format_number(
                float(formatted_emissions_series.iloc[0]))

    card = dbc.Card([
        dbc.CardHeader(html.A(
            # Add a link to the university page
            html.H4(he_name, className='card-title'), href=f"/university/{he_name}")),
        dbc.CardBody([
            html.H6(f"UKPRN: {ukprn_value}", className='card-subtitle pb-2'),
            # Add key metrics
            html.H6("Key metrics (2021/22):", style={"font-weight": "bold"}),
            html.H6(f"Total income: £{formatted_income}",
                    className='card-subtitle pb-2'),
            html.H6(f"Total scope 1 and 2 carbon emissions: {
                    formatted_emissions} Kg CO2e", className='card-subtitle pb-2')
        ])
    ])
    return card


def create_line_chart(hei=None, Class=None, category_marker=None):
    """
    Create a line chart based on the provided parameters.

    Args:
        hei (str, optional): The Higher Education Institution (HEI) provider.
        Class (str, optional): The class of the data.
        category_marker (str, optional): The category marker.

    Returns:
        fig: The plotly express line chart figure.

    """
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    data_df = load_data(data_path, [
                        'Academic Year', 'HE Provider', 'Class', 'Category marker', 'Category', 'Value'])
    # Filter data based on HEI, category marker, and class
    data_df = data_df[(data_df['HE Provider'] == hei) & (
        data_df['Category marker'] == category_marker) & (data_df['Class'] == Class)]
    # Convert 'Value' column to numeric
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')
    data_df = data_df.sort_values(by='Academic Year')
    # Create the line chart
    fig = px.line(data_df, x='Academic Year', y='Value', color='Category',
                  markers=True, color_discrete_sequence=px.colors.qualitative.Set3)
    # Update layout
    # Set title based on category marker
    if category_marker:
        fig.update_layout(title=f"Trend of '{category_marker}' categories:")
    else:
        fig.update_layout(title="Trend of categories:")

    return fig


def create_options_from_data(data_df, column):
    """
    Create a list of unique options from a specific column in a DataFrame.

    Parameters:
    data_df (pandas.DataFrame): The DataFrame containing the data.
    column (str): The name of the column to extract options from.

    Returns:
    list: A list of unique options from the specified column.
    """
    return data_df[column].unique().tolist()


def create_bar_chart(hei=None, year=None, category=None):
    """
    Create a bar chart based on the provided parameters.

    Args:
        hei (list, optional): List of Higher Education Institutions 
        (HEI) to include in the chart. Defaults to None.
        year (list, optional): List of academic years to include in 
        the chart. Defaults to None.
        category (str, optional): Category of data to include in the 
        chart. Defaults to None.

    Returns:
        fig: A plotly express bar chart figure object.

    """
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    data_df = load_data(data_path, [
                        'Academic Year', 'HE Provider', 'Category marker', 'Category', 'Value'])
    # Filter data based on HEI, year, and category
    if year:
        data_df = data_df[data_df['Academic Year'].isin(year)]
    if category:
        data_df = data_df[data_df['Category'] == category]
    if hei:
        data_df = data_df[data_df['HE Provider'].isin(hei)]
    # Convert 'Value' column to numeric
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')

    unique_years = sorted(data_df['Academic Year'].unique())
    color_scale = px.colors.qualitative.Set3[:len(unique_years)]
    data_df = data_df.drop_duplicates()
    # Create the bar chart
    fig = px.bar(data_df, x='HE Provider', y='Value', color='Academic Year',
                 barmode='group', color_discrete_sequence=color_scale)
    title = f"{data_df['Category marker'].iloc[0]}: {
        category}" if category else None
    fig.update_layout(title_text=title)
    return fig


def create_ranking_table(ClassName=None, academic_year=None, selected_regions=None):
    """
    Create a ranking table for HE providers based on the given parameters.

    Args:
        ClassName (str, optional): The class name to filter the data. Defaults to None.
        academic_year (str, optional): The academic year to filter the data. Defaults to None.
        selected_regions (list, optional): The list of regions to filter the data. Defaults to None.

    Returns:
        dash_table.DataTable: The ranking table as a Dash DataTable
        object.
    """
    data_path = Path(__file__).parent.parent.joinpath(
        'data', 'dataset_prepared.csv')
    data_df = load_data(data_path, [
                        'HE Provider', 'Region of HE provider', 'Academic Year', 'Class', 'Category', 'Value'])
    # Filter data based on the given parameters
    data_df = filter_data_for_table(
        data_df, ClassName, academic_year, selected_regions)
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')
    # Pivot the data to create the ranking table
    category_order = data_df['Category'].unique().tolist()
    new_category_order = list(filter(
        lambda x: x != 'Environmental management system external verification', category_order))
    pivot_df = data_df.pivot_table(index='HE Provider', columns='Category', values='Value').reset_index()[
        ['HE Provider'] + new_category_order]
    # Sort the columns based on the category order
    pivot_df.columns.name = None
    # Change the HE Provider column to a hyperlink in html format
    pivot_df['HE Provider'] = pivot_df['HE Provider'].apply(
        lambda x: f"<a href=/university/{quote(x)}>{x}</a>")
    # Create the ranking table
    table = dash_table.DataTable(
        id='ranking-table',
        columns=[{'name': col, 'id': col, 'presentation': "markdown"}
                 for col in pivot_df.columns],
        data=pivot_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': 'rgb(204, 255, 221)', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}],
        export_format='csv',
        sort_action='native',
        filter_action='native',
        markdown_options={'html': True}
    )
    return table


def create_category_marker_options(class_name):
    """
    Create a list of category marker options for a given class name.

    Parameters:
        class_name (str): The name of the class.

    Returns:
        list: A list of category marker options for the given class name.
    """
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    # Load 'Class' and 'Category marker' columns
    data_df = load_data(data_path, ['Class', 'Category marker'])
    if 'Class' in data_df.columns:  # Check if 'Class' column exists
        data_df = data_df[data_df['Class'] == class_name]
        return create_options_from_data(data_df, 'Category marker')
    else:
        return []  # Return empty list if 'Class' column does not exist


def create_category_options(category_marker):
    """
    Create a list of category options based on the given category marker.

    Parameters:
    - category_marker (str): The category marker to filter the data.

    Returns:
    - list: A list of category options.

    """
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    data_df = load_data(data_path, ['Category', 'Category marker'])
    data_df = data_df[data_df['Category marker'] == category_marker]
    return create_options_from_data(data_df, 'Category')
