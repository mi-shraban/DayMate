# backend/app/api/routes/planning.py
from fastapi import APIRouter, HTTPException
from app.services import weather_service, news_service, ai_service
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/planning", tags=["planning"])


class PlanResponse(BaseModel):
	weather: dict
	forecast: dict
	news: dict
	recommendations: str


@router.get("/debug/config")
async def debug_config():
	"""Debug endpoint to check configuration values"""
	return {
		"default_lat": settings.DEFAULT_LAT,
		"default_lon": settings.DEFAULT_LON,
		"default_city": settings.DEFAULT_CITY,
		"api_key_present": bool(settings.OPENWEATHER_API_KEY),
		"use_onecall": getattr(settings, 'USE_ONECALL_API', False)
	}


@router.get("/daily-plan", response_model=PlanResponse)
async def get_daily_plan():
	try:
		print("=== Starting daily plan generation ===")

		# Get combined weather data (current + forecast)
		weather_data = weather_service.get_combined_weather_data()
		print(f"Weather data type: {weather_data.get('forecast_type', 'none')}")
		print(f"Current weather: {weather_data.get('current', {}).get('name', 'Unknown')}")

		# Get news
		news_data_full = news_service.get_local_news(city_name=settings.DEFAULT_CITY)
		news_results = news_data_full.get('results', []) if news_data_full else []

		# Generate AI recommendations with forecast data
		recommendations = ai_service.generate_recommendations(
			weather_data,
			{'articles': news_results}
		)

		if not weather_data or not weather_data.get('current'):
			raise HTTPException(status_code=502, detail="Failed to fetch weather data")

		if not news_results:
			news_results = []
			print("Warning: No news articles retrieved from NewsData.io.")

		# Extract current and forecast separately for response
		current_weather = weather_data.get('current', {})
		forecast_data = {
			'type': weather_data.get('forecast_type', 'none'),
			'hourly': weather_data.get('hourly_forecast', []),
			'daily': weather_data.get('daily_forecast', []),
			'list': weather_data.get('forecast_list', [])
		}

		print(f"Forecast data being sent: type={forecast_data['type']}, items={len(forecast_data.get('list', []))}")
		print("=== Daily plan generation complete ===")

		return PlanResponse(
			weather=current_weather,
			forecast=forecast_data,
			news={'articles': news_results},
			recommendations=recommendations
		)
	except Exception as e:
		print(f"Error in get_daily_plan: {e}")
		import traceback
		traceback.print_exc()
		raise HTTPException(status_code=500, detail="An internal server error occurred")