# backend/app/services/news_service.py
import requests
from app.core.config import settings


def get_local_news(city_name: str = settings.DEFAULT_CITY) -> dict:
    # NewsData.io endpoint
    url = "https://newsdata.io/api/1/news"

    params = {
        'apikey': settings.NEWSDATA_API_KEY,
        'q': city_name,
        'language': 'en',
        'country': 'bd',
        'size': 5
    }

    try:
        print(f"Attempting to fetch news with query: {city_name}") # Debug log
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check for API-specific error responses
        if data.get('status') == 'error':
            print(f"NewsData.io API Error: {data.get('reason', 'Unknown error')}")
            return {}

        # Check if results were found based on the response structure
        # NewsData.io response structure: {"totalResults": N, "results": [...]}
        if data.get('totalResults', 0) == 0:
             print(f"No results found for query '{city_name}' using NewsData.io.")
             return {} # Return empty dict if no articles

        # Return the relevant part of the response, typically 'results'
        return data # Return the full response, the route will handle 'results'

    except requests.exceptions.HTTPError as e:
        print(f"NewsData.io HTTP Error: {e}")
        print(f"Response Body: {e.response.text}") # Print response body for debugging
        return {}
    except requests.exceptions.RequestException as e:
        print(f"NewsData.io Request Error: {e}")
        return {}
    except ValueError as e: # Decode error if response is not JSON
         print(f"NewsData.io Response Decode Error: {e}")
         return {}