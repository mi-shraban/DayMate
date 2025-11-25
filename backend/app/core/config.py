from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    NEWSDATA_API_KEY: str
    GEMINI_API_KEY: str

    # Gemini API URL
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    # Make dynamic later
    DEFAULT_LAT: float = 40.7128  # Default: NewYork city
    DEFAULT_LON: float = -74.0060
    DEFAULT_CITY: str = "Dhaka"

    class Config:
        env_file = ".env"


settings = Settings()