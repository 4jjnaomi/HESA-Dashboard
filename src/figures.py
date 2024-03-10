from pathlib import Path
import pandas as pd
import dash
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

def create_scatter_mapbox():
    hei_data = Path(__file__).parent.parent.joinpath('data','dataset_prepared_lat_lon.csv')
    cols = ['HE Provider', 'Latitude', 'Longitude']
    df_loc = pd.read_csv(hei_data, usecols=cols)
    df_loc['MarkerSize'] = 0.5
    fig = px.scatter_mapbox(df_loc, 
                            lat="Latitude", 
                            lon="Longitude", 
                            hover_name="HE Provider", 
                            zoom=5,
                            center={"lat": 52.3555, "lon": -1.1743},  # Approx center of England
                            mapbox_style="carto-positron",
                            color_continuous_scale='False',
                            height=600,
                            color_discrete_sequence=["#77dd77"],
                            opacity=0.8,
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
    pivot_df = pivot_df.sort_values(by=pivot_df.columns[1], ascending=False)

    # Add ranking column
    pivot_df.insert(0, 'Ranking', range(1, len(pivot_df) + 1))

    # Reset index
    pivot_df.reset_index(drop=True, inplace=True)

    # Rename columns
    pivot_df.columns.name = None

    #read df to csv
    pivot_df.to_csv(Path(__file__).parent.parent.joinpath('data','pivot_df.csv'))

    # Plotting
    table = dbc.Table.from_dataframe(pivot_df, striped=True, bordered=True, hover=True, responsive=True)

    return table
