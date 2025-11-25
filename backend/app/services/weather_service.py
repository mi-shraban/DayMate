import requests
from app.core.config import settings


def get_weather_data(lat: float = settings.DEFAULT_LAT, lon: float = settings.DEFAULT_LON) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Weather API Error: {e}")
        return {}

