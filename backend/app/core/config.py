from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    OPENWEATHER_API_KEY: str
    NEWS_API_KEY: str
    GEMINI_API_KEY: str # Or key for your chosen free LLM provider

    # Gemini API URL
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    # Make dynamic later
    DEFAULT_LAT: float = 40.7128  # Default: NewYork city
    DEFAULT_LON: float = -74.0060

    class Config:
        env_file = ".env"


settings = Settings()