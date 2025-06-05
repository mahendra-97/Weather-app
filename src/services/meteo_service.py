import requests
import json
from flask import current_app

def fetch_weather_data(latitude, longitude, start_date, end_date):
    """Fetch historical weather data from Open Meteo API."""
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        current_app.logger.error(f"Error fetching weather data: {response.text}")
        return None
    return response.json()