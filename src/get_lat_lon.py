from geopy.geocoders import Nominatim, photon
import pandas as pd
from pathlib import Path

geolocator = Nominatim(user_agent="HeiEnvironmentalDashboard", timeout=10)

raw_data = Path(__file__).parent.parent.parent.joinpath('data','dataset_prepared.csv')
data_df = pd.read_csv(raw_data)

#List of heis
heis = data_df['HE Provider'].unique()

# Function to find the latitude and longitude of heis in the dataset by parsing through heis array and adding the latitude and longitude to the dataframe

def get_lat_lon(heis1, data_df1):
    hei_array = heis1
    for i in hei_array:
        print(i)
        location = geolocator.geocode(i)
        if location is not None:
            data_df1.loc[data_df1['HE Provider'] == i, 'Latitude'] = location.latitude
            data_df1.loc[data_df1['HE Provider'] == i, 'Longitude'] = location.longitude
    return data_df1

data_df = get_lat_lon(heis, data_df)

# Save the dataframe to a csv file
data_df.to_csv(Path(__file__).parent.parent.parent.joinpath('data','dataset_prepared_lat_lon.csv'), index=False)
print('Latitude and Longitude added to the dataset')
