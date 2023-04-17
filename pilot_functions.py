# Location Based Storyteller

# %% IMPORTING LIBRARIES
import pandas as pd
import numpy as np
import wikipedia
import pyttsx3
import random

# %% CHECK GPS

def get_story():
    ''' Parameters: lat_input, log_input
        Returns: closest_city, page.summary '''
    lat_input = random.uniform(40, 45)
    log_input = random.uniform(0, 5)
    radius = 0.5

    # Load worldcities dataset and calculate closest city
    worldcities = pd.read_csv('data/worldcities.csv')
    worldcities['distance'] = np.sqrt((worldcities['lat'] - lat_input) ** 2 + (worldcities['lng'] - log_input) ** 2)

    # Selection of one or more cities
    closest_cities = worldcities.sort_values(by='distance').head(10)
    closest_city = worldcities.loc[worldcities['distance'].idxmin()]

    # Wikipedia search
    try:
        page = wikipedia.page(closest_city['city'], ',', closest_city['country'])
        print(page.summary)
    except:
        try:
            page = wikipedia.page(closest_city['city'])
            print(page.summary)
        except:
            print('No information found')

    # Create the story
    story = 'The closest city to your location is ' + closest_city['city'] + ' in ' + closest_city['country'] + '. ' + page.summary
    shortstory = str(story.split('.', 4)[0:4])     # Cut story after 4th sentence if possible and convert to string
    shortstory = shortstory.replace('[', '').replace(']', '').replace("'", '')

    # Synthesize story with pyttsx3
    tts = pyttsx3.init()
    tts.setProperty('rate', 80)
    tts.say(shortstory)
    tts.runAndWait()

get_story()
#%%
import pandas as pd
import wikipedia
import pyttsx3

def get_location_story(city_name):
    ''' Parameters: city_name
        Returns: closest_city, page.summary '''
    radius = 0.5

    # Load worldcities dataset and retrieve latitude and longitude values of the city
    worldcities = pd.read_csv('data/worldcities.csv')
    city_data = worldcities[worldcities['city_ascii'] == city_name]
    if city_data.empty:
        print(f"No data found for city: {city_name}")
        return

    lat_input = city_data['lat'].values[0]
    log_input = city_data['lng'].values[0]

    # Calculate closest city
    worldcities['distance'] = ((worldcities['lat'] - lat_input) ** 2 + (worldcities['lng'] - log_input) ** 2).apply(np.sqrt)
    closest_city = worldcities.loc[worldcities['distance'].idxmin()]

    # Wikipedia search
    try:
        page = wikipedia.page(closest_city['city'], ',', closest_city['country'])
        print(page.summary)
    except:
        try:
            page = wikipedia.page(closest_city['city'])
            print(page.summary)
        except:
            print('No information found')

    # Create the story
    story = 'The closest city to your location is ' + closest_city['city'] + ' in ' + closest_city['country'] + '. ' + page.summary
    shortstory = str(story.split('.', 4)[0:4])     # Cut story after 4th sentence if possible and convert to string
    shortstory = shortstory.replace('[', '').replace(']', '').replace("'", '')

    # Synthesize story with pyttsx3
    tts = pyttsx3.init()
    tts.setProperty('rate', 80)
    tts.say(shortstory)
    tts.runAndWait()
#%%
