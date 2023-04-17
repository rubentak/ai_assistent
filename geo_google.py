#%%
# Libraries
import requests
import credentials
from geo_location_point import get_location
import pandas as pd
import time

# Get surroundings by google maps api
api_key = credentials.google_api_key

lat = 41.3828
lng =  2.1824
radius = 1000               # -33.8670522,151.1957362&radius=500&
types = ''
search_name = ''

#%% Get location function

def get_surroundings(lat, lng, radius, types, search_name):
    api_key = credentials.google_api_key
    # Google Maps directions API endpoint
    prompt = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&types={types}&name={search_name}&key={api_key}'
    # Send request and get response
    response = requests.get(prompt)
    # Get response data as Python object
    data = response.json()
    results = data['results']
    # Parse the results to a dataframe
    df = pd.DataFrame.from_dict(results)
    df = df[['geometry', 'name', 'place_id', 'types', 'vicinity', 'business_status', 'rating', 'user_ratings_total', 'opening_hours']]
    df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
    df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])
    df = df.drop(columns=['geometry'])
    return df

get_surroundings(lat, lng, radius, types, search_name)

#%%
# Get surroundings with pagination 3*20



def get_surroundings_pagination(lat, lng, radius, types, search_name):
    api_key = credentials.google_api_key
    # Paginated request
    df_list = []
    for i in range(0, 3):
        # Google Maps directions API endpoint
        prompt = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&types={types}&name={search_name}&key={api_key}&pagetoken={i}'
        # Send request and get response
        response = requests.get(prompt)
        # Get response data as Python object
        data = response.json()
        results = data['results']
        # Parse the results to a dataframe
        df_list.append(pd.DataFrame.from_dict(results))
        time.sleep(1)  # Add a 1-second delay before the next request
    df = pd.concat(df_list, ignore_index=True)
    df = df[['geometry', 'name', 'place_id', 'types', 'vicinity', 'business_status', 'rating', 'user_ratings_total', 'opening_hours']]
    df['lat'] = df['geometry'].apply(lambda x: x['location']['lat'])
    df['lng'] = df['geometry'].apply(lambda x: x['location']['lng'])
    df = df.drop(columns=['geometry'])
    return df


#%%
