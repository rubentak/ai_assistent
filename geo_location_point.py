#%%
# importing geopy library
from geopy.geocoders import Nominatim
import json
from urllib.request import urlopen
import pandas as pd


#%%
def get_geo_location(city_name):
    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    # entering the location name
    getLoc = loc.geocode(city_name)

    # printing address
    print(getLoc.address)

    # printing latitude and longitude
    print("Latitude = ", getLoc.latitude, "\n")
    print("Longitude = ", getLoc.longitude)

    return getLoc


def get_location():
    url = "http://ipinfo.io/json"
    response = urlopen(url)
    data = json.load(response)
    # Get location
    lng = data['loc'].split(',')[1]
    lat = data['loc'].split(',')[0]
    location = {'lat': lat, 'lng': lng}
    return location

