from pathlib import Path
import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

def create_scatter_mapbox():
    hei_data = Path(__file__).parent.parent.joinpath('data','hei_data.csv')
    cols = ['UKPRN','HE Provider', 'lat', 'lon']
    df_loc = pd.read_csv(hei_data, usecols=cols)
    df_loc['MarkerSize'] = 0.5
    fig = px.scatter_mapbox(df_loc, 
                            lat="lat", 
                            lon="lon", 
                            hover_name="HE Provider", 
                            zoom=5,
                            center={"lat": 52.3555, "lon": -1.1743},  # Approx center of England
                            mapbox_style="carto-positron",
                            color_continuous_scale='False',
                            height=600,
                            color_discrete_sequence=["#77dd77"],
                            opacity=0.8,
                            custom_data='UKPRN'
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
            dbc.CardHeader(html.H4(he_name, className='card-title')),
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
    fig = px.line(data_df, x='Academic Year', y='Value', color='Category', markers=True)

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
