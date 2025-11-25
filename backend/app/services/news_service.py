import requests
from app.core.config import settings


def get_local_news(country_code: str = "US") -> dict: # Adjust country code as needed
    url = f"https://newsapi.org/v2/top-headlines"
    params = {
        'category': 'general',
        'country': country_code,
        'apiKey': settings.NEWS_API_KEY,
        'pageSize': 5
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"News API Error: {e}")
        return {}