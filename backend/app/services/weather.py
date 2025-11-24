import os
import httpx
import asyncio
from dotenv import load_dotenv
from datetime import datetime

# load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE = "https://api.openweathermap.org/data/2.5/onecall"


async def get_weather(lat, lon):
	if not API_KEY:
		raise Exception("No API key provided")

	params = {
		"lat": lat,
		"lon": lon,
		"exclude": "minutely,alerts",
		"units": "metric",
		"appid": API_KEY
	}

	async with httpx.AsyncClient(timeout=10) as client:
		r = await client.get(BASE, params=params)
		r.raise_for_status()
		data = r.json()
		return {
			"current": data.get("current"),
			"hourly": data.get("hourly", [])[:12],
		}


def format_weather_data(weather_data, lat, lon):
	"""Print weather data in a human-readable format"""
	if not weather_data:
		print("📭 No weather data received!")
		return

	print(f"📍 Weather for Latitude: {lat}, Longitude: {lon}\n")

	# === CURRENT WEATHER ===
	current = weather_data.get("current")
	if current:
		dt = datetime.fromtimestamp(current["dt"])
		temp = current["temp"]
		feels_like = current["feels_like"]
		humidity = current["humidity"]
		description = current["weather"][0]["description"].title() if current.get("weather") else "N/A"

		print("🌤️  CURRENT WEATHER")
		print(f"   Time: {dt.strftime('%Y-%m-%d %H:%M')} ({dt.strftime('%A')})")
		print(f"   Temperature: {temp:.1f}°C (feels like {feels_like:.1f}°C)")
		print(f"   Condition: {description}")
		print(f"   Humidity: {humidity}%")
		print()

	# === HOURLY FORECAST ===
	hourly = weather_data.get("hourly", [])
	if hourly:
		print("🕐 HOURLY FORECAST (next 12 hours):")
		print("-" * 60)
		for i, hour in enumerate(hourly):
			dt = datetime.fromtimestamp(hour["dt"])
			temp = hour["temp"]
			description = hour["weather"][0]["description"].title() if hour.get("weather") else "N/A"

			time_str = dt.strftime('%H:%M')
			if i == 0:
				time_str += " (now)"

			print(f"{time_str:>8} | {temp:>5.1f}°C | {description}")
		print()


async def print_weather(lat, lon):
	"""Fetch and print weather data"""
	try:
		print(f"📡 Fetching weather data for ({lat}, {lon})...\n")
		weather_data = await get_weather(lat, lon)
		format_weather_data(weather_data, lat, lon)

	except httpx.HTTPStatusError as e:
		status = e.response.status_code
		if status == 401:
			print("❌ Invalid API key. Please check your OPENWEATHER_API_KEY.")
		elif status == 400:
			print("❌ Invalid coordinates. Please check latitude/longitude values.")
		else:
			print(f"❌ HTTP Error {status}: {e.response.text}")

	except httpx.RequestError as e:
		print(f"❌ Network error: {str(e)}")

	except Exception as e:
		print(f"❌ Unexpected error: {str(e)}")


# Example usage
if __name__ == "__main__":
	# Example: Dhaka city coordinates
	asyncio.run(print_weather(23.8041, 90.4152))

# Try other locations:
# asyncio.run(print_weather(51.5074, -0.1278))   # London
# asyncio.run(print_weather(35.6895, 139.6917))  # Tokyo