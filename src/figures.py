from pathlib import Path
import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from urllib.parse import quote
import plotly.graph_objects as go


def load_data(file_path, columns):
    data_df = pd.read_csv(file_path, usecols=columns)
    return data_df


def filter_dataframe(data_df, filters):
    for column, values in filters.items():
        data_df = data_df[data_df[column].isin(values)]
    return data_df


def create_scatter_mapbox(region=None, hei=None):
    hei_data = Path(__file__).parent.parent.joinpath('data', 'hei_data.csv')
    cols = ['UKPRN', 'HE Provider', 'Region of HE provider', 'lat', 'lon']
    df_loc = load_data(hei_data, cols)
    if region:
        df_loc = filter_dataframe(df_loc, {'Region of HE provider': region})
    if hei:
        df_loc = filter_dataframe(df_loc, {'HE Provider': hei})

    regions = df_loc['Region of HE provider'].unique()
    colors = px.colors.qualitative.Set3[:len(regions)]
    color_scale = {region: color for region, color in zip(regions, colors)}

    fig = go.Figure()
    added_regions = {}

    for _, row in df_loc.iterrows():
        region = row['Region of HE provider']
        trace_settings = dict(lat=[row['lat']], lon=[row['lon']], mode='markers',
                              marker=dict(
                                  size=12, color=color_scale[region], opacity=0.7),
                              text=row['HE Provider'], hoverinfo='text',
                              customdata=[row['UKPRN']])

        if region not in added_regions:
            trace_settings['name'] = region
            added_regions[region] = True
        else:
            trace_settings['showlegend'] = False

        fig.add_trace(go.Scattermapbox(**trace_settings))

    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.8,
                      mapbox_center={
                          "lat": df_loc['lat'].mean(), "lon": df_loc['lon'].mean()},
                      margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=800, height=370,
                      legend_title_text='Region', showlegend=True)
    return fig


def filter_data_for_table(data_df, ClassName, acedemic_year, selected_regions):
    data_df = data_df[(data_df['Class'] == ClassName) & (
        data_df['Academic Year'] == acedemic_year)]
    if selected_regions:
        data_df = filter_dataframe(
            data_df, {'Region of HE provider': selected_regions})
    return data_df


def format_number(number):
    suffixes = ['', 'k', 'M', 'B']
    magnitude = 0
    while abs(number) >= 1000:
        magnitude += 1
        number /= 1000.0
    return f"{round(number, 3)}{suffixes[magnitude]}"


def create_card(ukprn):
    hei_data_path = Path(__file__).parent.parent.joinpath(
        'data', 'hei_data.csv')
    data_df = load_data(hei_data_path, ['HE Provider', 'UKPRN'])
    row = data_df[data_df['UKPRN'] == ukprn]
    ukprn_value, he_name = row.iloc[0]  # Swap the variable assignments

    entry_data_path = Path(__file__).parent.parent.joinpath(
        'data', 'entry_data.csv')
    entry_data_df = load_data(
        entry_data_path, ['HE Provider', 'Category', 'Value', 'Academic Year'])
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
        if not formatted_income_series.empty:
            formatted_income = format_number(
                float(formatted_income_series.iloc[0]))
        if not formatted_emissions_series.empty:
            formatted_emissions = format_number(
                float(formatted_emissions_series.iloc[0]))

    card = dbc.Card([
        dbc.CardHeader(html.A(
            html.H4(he_name, className='card-title'), href=f"/university/{he_name}")),
        dbc.CardBody([
            html.H6(f"UKPRN: {ukprn_value}", className='card-subtitle pb-2'),
            html.H6("Key metrics (2021/22):", style={"font-weight": "bold"}),
            html.H6(f"Total income: £{formatted_income}",
                    className='card-subtitle pb-2'),
            html.H6(f"Total scope 1 and 2 carbon emissions: {
                    formatted_emissions} Kg CO2e", className='card-subtitle pb-2')
        ])
    ])
    return card


def create_line_chart(hei=None, Class=None, category_marker=None):
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    data_df = load_data(data_path, [
                        'Academic Year', 'HE Provider', 'Class', 'Category marker', 'Category', 'Value'])
    data_df = data_df[(data_df['HE Provider'] == hei) & (
        data_df['Category marker'] == category_marker) & (data_df['Class'] == Class)]
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')
    data_df = data_df.sort_values(by='Academic Year')
    fig = px.line(data_df, x='Academic Year', y='Value', color='Category',
                  markers=True, color_discrete_sequence=px.colors.qualitative.Set3)

    if category_marker:
        fig.update_layout(title=f"Trend of '{category_marker}' categories:")
    else:
        fig.update_layout(title="Trend of categories:")

    return fig


def create_options_from_data(data_df, column):
    return data_df[column].unique().tolist()


def create_bar_chart(hei=None, year=None, category=None):
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    data_df = load_data(data_path, [
                        'Academic Year', 'HE Provider', 'Category marker', 'Category', 'Value'])
    if year:
        data_df = data_df[data_df['Academic Year'].isin(year)]
    if category:
        data_df = data_df[data_df['Category'] == category]
    if hei:
        data_df = data_df[data_df['HE Provider'].isin(hei)]
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')
    unique_years = sorted(data_df['Academic Year'].unique())
    color_scale = px.colors.qualitative.Set3[:len(unique_years)]
    data_df = data_df.drop_duplicates()
    fig = px.bar(data_df, x='HE Provider', y='Value', color='Academic Year',
                 barmode='group', color_discrete_sequence=color_scale)
    title = f"{data_df['Category marker'].iloc[0]}: {
        category}" if category else None
    fig.update_layout(title_text=title)
    return fig


def create_ranking_table(ClassName=None, academic_year=None, selected_regions=None):
    data_path = Path(__file__).parent.parent.joinpath(
        'data', 'dataset_prepared.csv')
    data_df = load_data(data_path, [
                        'HE Provider', 'Region of HE provider', 'Academic Year', 'Class', 'Category', 'Value'])
    data_df = filter_data_for_table(
        data_df, ClassName, academic_year, selected_regions)
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')
    category_order = data_df['Category'].unique().tolist()
    new_category_order = list(filter(
        lambda x: x != 'Environmental management system external verification', category_order))
    pivot_df = data_df.pivot_table(index='HE Provider', columns='Category', values='Value').reset_index()[
        ['HE Provider'] + new_category_order]
    pivot_df.columns.name = None
    pivot_df['HE Provider'] = pivot_df['HE Provider'].apply(
        lambda x: f"<a href=/university/{quote(x)}>{x}</a>")
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
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    # Load 'Class' and 'Category marker' columns
    data_df = load_data(data_path, ['Class', 'Category marker'])
    if 'Class' in data_df.columns:  # Check if 'Class' column exists
        data_df = data_df[data_df['Class'] == class_name]
        return create_options_from_data(data_df, 'Category marker')
    else:
        return []  # Return empty list if 'Class' column does not exist


def create_category_options(category_marker):
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    data_df = load_data(data_path, ['Category', 'Category marker'])
    data_df = data_df[data_df['Category marker'] == category_marker]
    return create_options_from_data(data_df, 'Category')
