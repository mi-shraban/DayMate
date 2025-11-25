# backend/app/api/routes/planning.py
from fastapi import APIRouter, HTTPException
from app.services import weather_service, news_service, ai_service
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/planning", tags=["planning"])


class PlanResponse(BaseModel):
    weather: dict
    news: dict
    recommendations: str


@router.get("/daily-plan", response_model=PlanResponse)
async def get_daily_plan():
    try:
        weather_data = weather_service.get_weather_data()
        news_data = news_service.get_local_news()
        recommendations = ai_service.generate_recommendations(weather_data, news_data)

        if not weather_data:
             raise HTTPException(status_code=502, detail="Failed to fetch weather data")
        if not news_data:
             raise HTTPException(status_code=502, detail="Failed to fetch news data")

        return PlanResponse(
            weather=weather_data,
            news=news_data,
            recommendations=recommendations
        )
    except Exception as e:
        print(f"Error in get_daily_plan: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")