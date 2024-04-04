from pathlib import Path
import time

from geopy.geocoders import Nominatim
import pandas as pd

geolocator = Nominatim(user_agent="HeiEnvironmentalDashboard", timeout=10)

raw_data = Path(__file__).parent.joinpath('hei_data.csv')
data_df = pd.read_csv(raw_data)


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
    'The Manchester Metropolitan University': 'Manchester Metropolitan University',
    'The University of Manchester': 'Manchester University',
    'The University of Northampton': 'Waterside Campus, University of Northampton',
    'University of Northumbria at Newcastle': 'Northumbria University',
    'Rose Bruford College of Theatre and Performance': 'Rose Bruford College',
    'The University of Salford': 'Salford University',
    'The University of Southampton': 'Southampton University',
    'University of St Mark and St John': 'Plymouth Marjon University, Derriford',
    'The University of Surrey': 'Surrey University',
    'The University of Sussex': 'Sussex University',
    'The University of Warwick': 'Warwick University',
    'University of the West of England, Bristol': 'UWE Bristol',
    'Conservatoire for Dance and Drama': 'Rambert School of Ballet and Contemporary Dance',
    'The Liverpool Institute for Performing Arts': 'LIPA',
    'The University of Reading': 'Reading University',
    'The University of Essex': 'University of Essex Colchester Campus',
    "King's College London": "King's College London, Strand",
    "SOAS University of London": "SOAS",
}

# Map university names to their alternative names and create a new column
data_df['Alternative Name'] = data_df['HE Provider'].map(
    university_alternative_names).fillna(data_df['HE Provider'])

# Create an array of HEIs
heis = data_df['Alternative Name']

# Function to find the latitude and longitude of HEIs in England


def get_lat_lon(heis1, data_df1):
    hei_array = heis1
    for i in hei_array:
        retry_count = 0
        while retry_count < 3:  # Retry up to 3 times
            try:
                # Geocode the HEI name within the bounding box of England
                location = geolocator.geocode(i, country_codes='GB')
                if location is not None:
                    data_df1.loc[data_df1['Alternative Name']
                                 == i, 'lat'] = location.latitude
                    data_df1.loc[data_df1['Alternative Name']
                                 == i, 'lon'] = location.longitude
                break  # Break out of the retry loop if successful
            except Exception as e:
                print(f"Error geocoding {i}: {e}")
                retry_count += 1
                time.sleep(2)  # Wait for 2 seconds before retrying
    return data_df1


new_df = get_lat_lon(heis, data_df)

# Save the dataframe to a csv file
new_df.to_csv(Path(__file__).parent.parent.joinpath(
    'data', 'hei_data.csv'), index=False)
print('Latitude and Longitude added to the dataset')

# find rows where the he provider are different but lat and lon are the same
duplicate = new_df[new_df.duplicated(subset=['lat', 'lon'], keep=False)]
print(duplicate)
