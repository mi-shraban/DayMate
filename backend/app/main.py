import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .services import weather, news, planner
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


app = FastAPI(title="DayMate API")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


class Location(BaseModel):
	lat: float
	lon: float
	city: str | None = None


@app.get("/health")
async def health():
	return {"status": "ok"}


@app.post("/data")
async def data(loc: Location):
	try:
		w = await weather.get_weather(lat=loc.lat, lon=loc.lon)
		n = await news.get_local_news(query=loc.city or f"{loc.lat},{loc.lon}")
		plan = await planner.generate_plan(weather=w, news=n)
		return {"weather": w, "news": n, "plan": plan}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))