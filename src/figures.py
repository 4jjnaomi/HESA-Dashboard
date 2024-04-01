from pathlib import Path
import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

def create_scatter_mapbox():
    hei_data = Path(__file__).parent.parent.joinpath('data', 'hei_data.csv')
    cols = ['UKPRN', 'HE Provider', 'Region of HE provider', 'lat', 'lon']
    df_loc = pd.read_csv(hei_data, usecols=cols)

    # Define a color scale using px.colors.qualitative.Set3
    color_scale = px.colors.qualitative.Set3

    df_loc['MarkerSize'] = 5

    fig = px.scatter_geo(
        df_loc,
        lat="lat",
        lon="lon",
        color="Region of HE provider",
        hover_name="HE Provider",
        hover_data={"Region of HE provider": False, "lat": False, "lon": False, 'MarkerSize': False},
        custom_data=["UKPRN"],
        opacity=0.8,
        color_continuous_scale=color_scale,
        projection="mercator",
        width=800,
        height=800,
        size = 'MarkerSize'
    )

    fig.update_geos(
        resolution=50,
        showland=True,
        landcolor='rgb(220, 220, 220)'
    )

    fig.update_layout(
        title='HE Providers by Region',
        geo=dict(
            fitbounds="locations",
            showcoastlines=True,  # Show coastlines
            showland=True,  # Show land
            showcountries=True,  # Show country borders
            countrycolor="black",  # Border color for countries
            showrivers=True,  # Show rivers
            rivercolor="blue",  # River color
            showlakes=True,  # Show lakes
            lakecolor="rgb(0, 255, 255)",  # Lake color
        )
    )

    return fig

def create_ranking_table(ClassName, AcademicYear):
    # Load the dataset
    data_path = Path(__file__).parent.parent.joinpath('data','dataset_prepared.csv')
    data_df = pd.read_csv(data_path)
    cols = ['HE Provider', 'Academic Year', 'Class', 'Category', 'Value']
    data_df = data_df[cols]

    # Filter the DataFrame by 'Class' and 'Academic Year'
    data_df = data_df[(data_df['Class'] == ClassName) & (data_df['Academic Year'] == AcademicYear)]

    # Convert 'Value' column to numeric, ignoring errors
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')

    category_order = data_df['Category'].unique().tolist()
    new_category_order = list(filter(lambda x: x != 'Environmental management system external verification', category_order))

    # Pivot the DataFrame to have categories as columns
    pivot_df = data_df.pivot_table(index='HE Provider', columns='Category', values='Value').reset_index()

    pivot_df = pivot_df[['HE Provider'] + new_category_order]

    # Reset index
    pivot_df.reset_index(drop=True, inplace=True)

    # Rename columns
    pivot_df.columns.name = None

    # Converting to DataTable with sorting enabled
    table = dash_table.DataTable(
        id='ranking-table',
        columns=[{'name': col, 'id': col} for col in pivot_df.columns],
        data=pivot_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': 'rgb(204, 255, 221)', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
        ],
        export_format='csv',
        sort_action='native',
        filter_action='native',
    )

    return table

#Create a card that displays the HEI name, Region and UKPRN number based on the UKPRN
def create_card(ukprn):
    # Load the dataset
    data_path = Path(__file__).parent.parent.joinpath('data','hei_data.csv')
    data_df = pd.read_csv(data_path)
    cols = ['HE Provider', 'Region of HE provider', 'UKPRN']
    data_df = data_df[cols]

    # Get the row for the UKPRN
    row = data_df[data_df['UKPRN'] == ukprn]

    he_name = row['HE Provider'].values[0]
    region = row['Region of HE provider'].values[0]
    ukprn_value = row['UKPRN'].values[0]

    # Create a card to display the HEI name, Region and UKPRN number
    card = dbc.Card(
        [
            dbc.CardHeader(html.A(
                html.H4(he_name, className='card-title'), href=f"/university/{he_name}")
                ),
            dbc.CardBody(
                [
                    html.H6(f"Region: {region}", className='card-subtitle'),
                    html.Br(),
                    html.H6(f"UKPRN: {ukprn_value}", className='card-subtitle'),
                ]
            ),
        ]
    )

    return card

#Create a line chart where a user can select a HEI and also select a Category marker and then see the trend of all the categories within that Category marker over the years
def create_line_chart(hei=None, Class=None, category_marker=None):
    # Load the dataset
    data_path = Path(__file__).parent.parent.joinpath('data','entry_data.csv')
    data_df = pd.read_csv(data_path)
    cols = ['Academic Year', 'HE Provider', 'Class', 'Category marker', 'Category', 'Value']
    data_df = data_df[cols]

    # Filter the DataFrame by 'HE Provider' and 'Category'
    data_df = data_df[(data_df['HE Provider'] == hei) & (data_df['Category marker'] == category_marker) & (data_df['Class'] == Class)]

    # Convert 'Value' column to numeric, ignoring errors
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')

    #Reorder so that the years are in ascending order
    data_df = data_df.sort_values(by='Academic Year')

    # Create a line chart
    fig = px.line(data_df, x='Academic Year', y='Value', color='Category', markers=True, color_discrete_sequence=px.colors.qualitative.Set3)

    if category_marker != None:
        fig.update_layout(title=f"Trend of '{category_marker}' categories:")

    return fig

def create_category_marker_options(class_name):
    # Load the dataset
    data_path = Path(__file__).parent.parent.joinpath('data','entry_data.csv')
    data_df = pd.read_csv(data_path)
    data_df = data_df[data_df['Class'] == class_name]
    category_markers = data_df['Category marker'].unique()
    options = [category_marker for category_marker in category_markers]
    return options

def create_category_options(category_marker):
    # Load the dataset
    data_path = Path(__file__).parent.parent.joinpath('data','entry_data.csv')
    data_df = pd.read_csv(data_path)
    data_df = data_df[(data_df['Category marker'] == category_marker)]
    categories = data_df['Category'].unique()
    options = [category for category in categories]
    return options

#Create a bar chart where a user can select one or more hei(s) and also select a year and they can see the value of the category they've selected
def create_bar_chart(hei=None, year=None, category=None):
    # Load the dataset
    data_path = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
    data_df = pd.read_csv(data_path)
    cols = ['Academic Year', 'HE Provider', 'Category marker', 'Category', 'Value']
    data_df = data_df[cols]

    # Filter the DataFrame by 'Academic Year' and 'Category'
    if year:
        data_df = data_df[data_df['Academic Year'].isin(year)]
    if category:
        data_df = data_df[data_df['Category'] == category]

    # Filter the DataFrame by 'HE Provider'
    if hei:
        data_df = data_df[data_df['HE Provider'].isin(hei)]

    # Convert 'Value' column to numeric, ignoring errors
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce')

    # Create a list of unique years
    unique_years = sorted(data_df['Academic Year'].unique())

    # Assign a unique color to each year
    color_scale = px.colors.qualitative.Set3[:len(unique_years)]

    #Ensure each row is unique
    data_df = data_df.drop_duplicates()

    # Create a bar chart
    fig = px.bar(data_df, x='HE Provider', y='Value', color='Academic Year', barmode='group', color_discrete_sequence=color_scale)

    category_marker = data_df['Category marker'].unique()
    category_marker = category_marker[0]

    if category is not None:
        title = f"{category_marker}: {category}"
        fig.update_layout(title_text=title)

    return fig