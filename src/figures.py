from pathlib import Path
import pandas as pd
import dash
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

hei_data = Path(__file__).parent.parent.joinpath('data','dataset_prepared_lat_lon.csv')

def create_scatter_mapbox():
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
