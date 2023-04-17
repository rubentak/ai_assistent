# GEOSPATIALLY SUPPORTED STORYTELLER
# possible names: fun_fact, storymapper, ...

# Based on the current location, the storyteller will tell a fun fact or anecdote about nearby places
# Possible sources: Wikipedia, Google, ...
# Possine output: country, city, street information; historical events; future events and local ; stores and restaurants;
#                 famous people; myths and legends; weather incidents;



#%% IMPORTING LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium as fl
import wikipedia
import gtts
from numpy import random
from playsound import playsound
import pyttsx3
import numpy.random


# SETTINGS

#%% CHECK GPS

# Define GPS Coordinates of Barcelona
lat_input = 11.390
log_input = 11.154

# Define the radius of the circle
radius = 0.5

# Load worldcities dataset zip 'https://simplemaps.com/data/world-cities'
worldcities = pd.read_csv('simplemaps_worldcities_basicv1.75/worldcities.csv')

print(worldcities.tail(10))


#%% MATCH LOCATION

# Find closest city to the input coordinates
# Calculate the distance between the input coordinates and the coordinates of the cities
worldcities['distance'] = np.sqrt((worldcities['lat'] - lat_input)**2 + (worldcities['lng'] - log_input)**2)

# Find the closest cit
closest_cities = worldcities.sort_values(by='distance').head(10)
closest_city = worldcities.loc[worldcities['distance'].idxmin()]

# Print the closest city
print(closest_city)

#%% INFORMATION SEARCH

# Search for the closest city on wikipedia
try:

    page = wikipedia.page(closest_city['city'])
    wikipedia.set_lang("de")
    print(page.summary)
except:
    print('No information found')

# Search for the closest city with country on wikipedia
try:
    page = wikipedia.page(closest_city['city'], ',' , closest_city['country'])
    print(page.summary)
except:
    print('No information found')

# Possible source: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/6ZFC0V

#%% PLOT CITY MAP (FOLIUM as html in directory

# City Map with folium
# https://python-visualization.github.io/folium/

# Create a map of the city
city_map = fl.Map(location=[closest_city['lat'], closest_city['lng']], zoom_start=10)

# Add a marker to the map
fl.Marker([closest_city['lat'], closest_city['lng']], popup=closest_city['city']).add_to(city_map)

# Display the map

city_map.save(f"data/{closest_city['city']}_map.html")   # <- HTML file in directory

#%% Synthesize the story verbally

from gtts import gTTS

lang = gtts.lang.tts_langs()
rand_lang = random.choice(list(lang.keys()))  #  random.randint(0, 9)
print(type(lang))
story = f"The closest city is {closest_city}{page.summary}"
my_tts = story
tts = gTTS(text=my_tts, lang=rand_lang, slow=False)
tts.save(f"data/{closest_city['city']}_story.mp3")
print(lang)
print(rand_lang)
