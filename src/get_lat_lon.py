from geopy.geocoders import Nominatim, photon
import pandas as pd
from pathlib import Path
import time

geolocator = Nominatim(user_agent="HeiEnvironmentalDashboard", timeout=10)

raw_data = Path(__file__).parent.parent.joinpath('data', 'dataset_prepared_lat_lon.csv')
data_df = pd.read_csv(raw_data)

# List of HEIs
heis = data_df['HE Provider'].unique()

# Function to find the latitude and longitude of HEIs in England
def get_lat_lon(heis1, data_df1):
    hei_array = heis1
    for i in hei_array:
        print(i)
        retry_count = 0
        while retry_count < 3:  # Retry up to 3 times
            try:
                # Geocode the HEI name within the bounding box of England
                location = geolocator.geocode(i, country_codes='GB')
                if location is not None:
                    data_df1.loc[data_df1['HE Provider'] == i, 'Latitude'] = location.latitude
                    data_df1.loc[data_df1['HE Provider'] == i, 'Longitude'] = location.longitude
                break  # Break out of the retry loop if successful
            except Exception as e:
                print(f"Error geocoding {i}: {e}")
                retry_count += 1
                time.sleep(2)  # Wait for 2 seconds before retrying
    return data_df1

#data_df = get_lat_lon(heis, data_df)

cols = ['HE Provider', 'Latitude', 'Longitude']
new_df = data_df[cols]
#remove duplicate rows
new_df = new_df.drop_duplicates(subset=['HE Provider'])


#find rows with missing lat and lon
#missing = new_df[new_df['Latitude'].isna()]
#print(missing)

#find rows where the he provider are different but lat and lon are the same
duplicate = new_df[new_df.duplicated(subset=['Latitude', 'Longitude'], keep=False)]
#include the row for The University of Reading
duplicate = duplicate._append(new_df[new_df['HE Provider'] == 'The University of Reading'])
print(duplicate)

# Dictionary to map universities to their alternative names
university_alternative_names = {
    'The University of Bradford': 'Bradford University',
    'The University of Brighton': 'Brighton University',
    'The University of Bristol': 'Bristol University',
    'The University of Central Lancashire': 'UCLan',
    'The University of Chichester': 'Chichester University',
    'The University of East Anglia': 'UEA',
    'The University of East London': 'UEL',
    'The University of Exeter': 'Exeter University',
    'The National Film and Television School': 'NFTS',
    'The University of Greenwich': 'Greenwich University',
    'The University of Huddersfield': 'Huddersfield University',
    'The University of Hull': 'Hull University',
    'Imperial College of Science, Technology and Medicine': 'Imperial College London',
    'The University of Leicester': 'Leicester University',
    'The University of Liverpool': 'Liverpool University',
    'University of London (Institutes and activities)': 'University of London',
    'The Manchester Metropolitan University': 'Manchester Met',
    'The University of Manchester': 'Manchester University',
    'The University of Northampton': 'Northampton University',
    'University of Northumbria at Newcastle': 'Northumbria University',
    'Rose Bruford College of Theatre and Performance': 'Rose Bruford College',
    'The University of Salford': 'Salford University',
    'The University of Southampton': 'Southampton University',
    'University of St Mark and St John': 'Marjon University',
    'The University of Surrey': 'Surrey University',
    'The University of Sussex': 'Sussex University',
    'The University of Warwick': 'Warwick University',
    'University of the West of England, Bristol': 'UWE Bristol',
    'Conservatoire for Dance and Drama': 'CDD',
    'The Liverpool Institute for Performing Arts': 'LIPA',
    'The University of Reading': 'Reading University'
}

new_df['HE Provider'] = new_df['HE Provider'].replace(university_alternative_names)

#Find lat and lon of each hei






# Save the dataframe to a csv file
#data_df.to_csv(Path(__file__).parent.parent.joinpath('data','dataset_prepared_lat_lon.csv'), index=False)
#print('Latitude and Longitude added to the dataset')
