import os
from typing import Dict
import requests
from flask import jsonify
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')


def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius, 2)


def get_weather(lat, lon):
    OPENWEATHERMAP_API_URL = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}'
    try:
        response = requests.get(OPENWEATHERMAP_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({'error': 'Failed to retrieve weather data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def prepare_weather(weather_data: Dict):
    for key in ['temp', 'feels_like', 'temp_min', 'temp_max']:
        weather_data['main'][key] = kelvin_to_celsius(weather_data['main'][key])
    weather_data["weather"] = weather_data["weather"][0]
    return pd.json_normalize(weather_data).T
