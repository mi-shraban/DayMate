# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import planning

app = FastAPI(title="DayMate Backend", version="1.0.0")

# Allow CORS for local frontend development (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(planning.router)

@app.get("/")
def read_root():
    return {"message": "DayMate Backend API is running!"}