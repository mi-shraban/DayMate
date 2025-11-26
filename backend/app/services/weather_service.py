import requests
from app.core.config import settings


def get_weather_data(lat: float = settings.DEFAULT_LAT, lon: float = settings.DEFAULT_LON) -> dict:
	"""Get current weather data"""
	url = f"https://api.openweathermap.org/data/2.5/weather"
	params = {
		'lat': lat,
		'lon': lon,
		'appid': settings.OPENWEATHER_API_KEY,
		'units': 'metric'
	}
	print(f"DEBUG: Requesting weather for lat={lat}, lon={lon}")
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()
		print(f"DEBUG: Received weather for {data.get('name', 'Unknown')}")
		return data
	except requests.exceptions.RequestException as e:
		print(f"Weather API Error: {e}")
		return {}


def get_forecast_data(lat: float = settings.DEFAULT_LAT, lon: float = settings.DEFAULT_LON) -> dict:
	"""
    Get 5-day forecast with 3-hour intervals (FREE TIER)
    Returns forecast for the next 5 days with data every 3 hours (40 data points)
    """
	url = "https://api.openweathermap.org/data/2.5/forecast"
	params = {
		'lat': lat,
		'lon': lon,
		'appid': settings.OPENWEATHER_API_KEY,
		'units': 'metric'
	}
	print(f"DEBUG: Requesting forecast for lat={lat}, lon={lon}")
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()
		print(f"DEBUG: Received forecast with {len(data.get('list', []))} data points")
		return data
	except requests.exceptions.RequestException as e:
		print(f"Forecast API Error: {e}")
		return {}


def get_hourly_forecast_onecall(lat: float = settings.DEFAULT_LAT, lon: float = settings.DEFAULT_LON) -> dict:
	"""
    Get hourly forecast using One Call API 3.0
    Provides 48-hour hourly forecast (REQUIRES ONE CALL SUBSCRIPTION)
    Free tier: 1,000 calls/day
    """
	url = "https://api.openweathermap.org/data/3.0/onecall"
	params = {
		'lat': lat,
		'lon': lon,
		'appid': settings.OPENWEATHER_API_KEY,
		'units': 'metric',
		'exclude': 'minutely,alerts'
	}
	print(f"DEBUG: Requesting One Call API for lat={lat}, lon={lon}")
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()
		print(f"DEBUG: Received One Call data with {len(data.get('hourly', []))} hourly forecasts")
		return data
	except requests.exceptions.RequestException as e:
		print(f"One Call API Error: {e}")
		if "401" in str(e):
			print("One Call API requires subscription. Falling back to 5-day forecast.")
		return {}


def get_combined_weather_data(lat: float = settings.DEFAULT_LAT, lon: float = settings.DEFAULT_LON) -> dict:
	"""
    Get both current weather and forecast data
    Uses 5-day/3-hour forecast (FREE) by default
    Set USE_ONECALL_API=true in .env to use hourly forecast (requires One Call subscription)
    """
	current = get_weather_data(lat, lon)

	# Try One Call API first if enabled, otherwise use 5-day forecast
	if getattr(settings, 'USE_ONECALL_API', False):
		forecast = get_hourly_forecast_onecall(lat, lon)
		if forecast:
			return {
				'current': current,
				'hourly_forecast': forecast.get('hourly', []),
				'daily_forecast': forecast.get('daily', []),
				'forecast_type': 'hourly'
			}

	# Fallback to 5-day/3-hour forecast (FREE tier)
	forecast = get_forecast_data(lat, lon)
	return {
		'current': current,
		'forecast_list': forecast.get('list', []),
		'forecast_type': '3-hour'
	}