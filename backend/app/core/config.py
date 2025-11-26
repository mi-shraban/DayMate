from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    NEWSDATA_API_KEY: str
    GEMINI_API_KEY: str

    # Gemini API URL
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    # Make dynamic later
    DEFAULT_LAT: float = 23.8041    # Default: Dhaka city
    DEFAULT_LON: float = 90.4152
    DEFAULT_CITY: str = "Dhaka"

    # Set to True to use One Call API 3.0 (requires subscription, 1000 free calls/day)
    # Set to False to use 5-day/3-hour forecast (completely free)
    USE_ONECALL_API: bool = False

    class Config:
        env_file = ".env"


settings = Settings()