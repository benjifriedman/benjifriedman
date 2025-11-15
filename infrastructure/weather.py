from configparser import ConfigParser
from datetime import datetime, timedelta
import json
import os

import requests


def _get_weather_api_key():
    """Fetch the API key from config file in local project.
    Otherwise, grab from GitHub secrets.
    Be sure to add "secrets.ini" to your .gitignore file!

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    try:
        config = ConfigParser()
        config.read("secrets.ini")
        api_key = config["openweather"]["api_key"]
    except Exception:
        api_key = os.environ["openweather_api_key"]
    return api_key


def get_openweather_info():
    """Retrieve openweather data from API for Berkeley, CA"""
    WEATHER_API_KEY = _get_weather_api_key()
    OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?"
    # Berkeley, CA coordinates: lat=37.8715, lon=-122.2730
    OPEN_WEATHER_URL += f"lat=37.8715&lon=-122.2730&appid={WEATHER_API_KEY}&units=standard"
    res = requests.get(OPEN_WEATHER_URL)
    weather_dict = json.loads(res.text)

    city_temperature = round(
        ((((weather_dict.get("main").get("temp")) - 273.15) * 1.8) + 32), 1
    )
    sunrise_time_unix = weather_dict.get("sys").get("sunrise")
    sunset_time_unix = weather_dict.get("sys").get("sunset")

    return weather_dict, city_temperature, sunrise_time_unix, sunset_time_unix


def weather_icon(temp):
    if temp >= 85:
        return '🥵🌞'
    elif temp <= 50:
        return '🏂 ❄️ ⛄'
    else:
        return '👌😄'


def convert_timestamp_to_PST(time_stamp):
    """Convert unix timestamp to UTC then PST"""
    UTC = datetime.utcfromtimestamp(time_stamp)
    return UTC + timedelta(hours=-8)
