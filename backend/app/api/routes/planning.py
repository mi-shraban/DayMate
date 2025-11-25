# backend/app/api/routes/planning.py
from fastapi import APIRouter, HTTPException
from app.services import weather_service, news_service, ai_service
from app.core.config import settings # Import settings to get the default city
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/planning", tags=["planning"])

class PlanResponse(BaseModel):
    weather: dict
    news: dict # This will now hold the full NewsData.io response or just the 'results'
    recommendations: str

@router.get("/daily-plan", response_model=PlanResponse)
async def get_daily_plan():
    try:
        weather_data = weather_service.get_weather_data()
        # Pass the city name to the news service, using the default from settings
        news_data_full = news_service.get_local_news(city_name=settings.DEFAULT_CITY)
        # The news_data_full contains the entire response from NewsData.io
        # The AI service expects the list of articles, which is in the 'results' key
        news_results = news_data_full.get('results', []) if news_data_full else []

        # Pass the list of articles ('results') to the AI service
        recommendations = ai_service.generate_recommendations(weather_data, {'articles': news_results})

        if not weather_data:
             raise HTTPException(status_code=502, detail="Failed to fetch weather data")
        # Check if news_results is empty, which means get_local_news returned {}
        # or {'results': []}
        if news_data_full is None or not news_results:
             # Consider this a non-critical failure, maybe log a warning
             # raise HTTPException(status_code=502, detail="Failed to fetch news data")
             # For now, let's proceed with potentially empty news
             news_results = [] # Ensure it's an empty list if nothing found
             print("Warning: No news articles retrieved from NewsData.io.")

        # Return the full weather data, and the *results* part of the news data
        # The frontend expects a structure with an 'articles' key under 'news'
        return PlanResponse(
            weather=weather_data,
            news={'articles': news_results}, # Structure the news response for the frontend
            recommendations=recommendations
        )
    except Exception as e:
        print(f"Error in get_daily_plan: {e}")
        import traceback
        traceback.print_exc() # Print the full traceback for debugging
        raise HTTPException(status_code=500, detail="An internal server error occurred")