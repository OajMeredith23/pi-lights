import requests
from dotenv import load_dotenv
import os 

load_dotenv()
weather_key = os.environ.get('weather_key')
weather_url = "https://api.openweathermap.org/data/3.0/onecall?lat=51.07&lon=00.04&appid=" + weather_key

def getWeather():
    weather_data = requests.get(weather_url).json()
    sunrise_time = weather_data['current']['sunrise']
    sunset_time = weather_data['current']['sunset']
    weather_next_hour = weather_data['hourly'][1]['weather'][0]
    return [sunrise_time, sunset_time, weather_next_hour]