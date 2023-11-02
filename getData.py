# ! pip install openai
# ! pip install geopy
# ! pip install geopy
# ! pip install timezonefinder

# Make the OpenAI code library available to your application
from geopy.geocoders import Nominatim
from datetime import datetime
import requests
from timezonefinder import TimezoneFinder 
import json
from pprint import pprint

######################################################
# Time functions not really needed
######################################################

# What are Keiser University’s coordinates?
# location_name_to_latlong("5002 W Waters Ave, Tampa, FL USA")

def get_timezone_from_latlong(latitude_longitude_tuple):
    latitude, longitude = latitude_longitude_tuple
    tz_finder = TimezoneFinder()
    return tz_finder.timezone_at(lat = latitude, lng = longitude)

# testing
# get_timezone_from_latlong(location_name_to_latlong("Tokyo"))
# get_timezone_from_latlong(location_name_to_latlong("Denver"))

def get_current_date_and_time_in_timezone(timezone_name):
    url = f"http://worldtimeapi.org/api/timezone/{timezone_name}"
    response = requests.get(url)
    json = response.json()
    raw_date_and_time = json['datetime']
    date_and_time = datetime.strptime(raw_date_and_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    formatted_time = date_and_time.strftime("%I:%M %p on %A, %B %d")
    # Remove leading zeros
    formatted_time = formatted_time.replace(" 0", " ")
    return formatted_time

# get_current_date_and_time_in_timezone('Asia/Tokyo')
# get_current_date_and_time_in_timezone('America/Denver')

def get_current_date_and_time_in_location(location_name):
    return get_current_date_and_time_in_timezone(get_timezone_from_latlong(location_name_to_latlong(location_name)))

# get_current_date_and_time_in_location("Tokyo")
# get_current_date_and_time_in_location("Denver")

def create_weather_poem_prompt(location_name):
    weather = get_current_weather(location_name)
    # print(f'weather: {weather}')
    prompt = (
        f"The weather in {location_name} is {weather['weather']}, " +
        f"with a temperature of {celsius_to_fahrenheit(weather['temperature'])} degrees F, " +
        f"{weather['cloud_cover']}% cloud cover, and " +
        f"{weather['humidity']}% humidity. " +
        f"The current date and time there is {get_current_date_and_time_in_location(location_name)}. " +
        "Create a short poem about all this in the style of Edgar Allen Poe."
    )
    
    return prompt



# create_weather_poem_prompt("Denver, CO")

# def create_weather_poem_for_location(location):
#     return create_completion(create_weather_poem_prompt(location))

# print(create_weather_poem_for_location("Cairo"))
# print(create_weather_poem_for_location("Denver, CO"))
# print(create_weather_poem_for_location("Tampa, FL"))

######################################################
# location functions all that's really needed
######################################################

def location_name_to_latlong(location_name):
    geolocator = Nominatim(user_agent="Tampa Code Camp 2023 AI demo app")
    location = geolocator.geocode(location_name)
    return (location.latitude, location.longitude)

def celsius_to_fahrenheit(degrees_celsius):
    return (degrees_celsius * 1.8) + 32

WMO_CODE_TABLE = {
    0:  "clear sky",
    1:  "mainly clear", 
    2:  "partly cloudy",
    3:  "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "light rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}

def get_current_weather(location_name):
    latitude, longitude = location_name_to_latlong(location_name)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relativehumidity_2m,weathercode,cloudcover"
    #url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,weathercode,cloudcover"
    response = requests.get(url)
    json = response.json()
    # pretty print json
    # pprint(f'json: {json}', indent=4)
    result = {
        "weather":     WMO_CODE_TABLE.get(json["current"]["weathercode"], "unknown"),
        "cloud_cover": json['current']['cloudcover'],
        "temperature": json['current']['temperature_2m'],
        "humidity":    json['current']['relativehumidity_2m'],
    }
    return result


# get_current_weather("Tampa, FL")
# get_current_weather("Denver, CO")
