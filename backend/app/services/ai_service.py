# backend/app/services/ai_service.py
import requests
from app.core.config import settings


def generate_recommendations(weather_data: dict, news_data: dict) -> str:
    if not weather_data or not news_data:
        return "Unable to generate recommendations due to missing data."

    weather_desc = weather_data.get('weather', [{}])[0].get('description', 'Unknown')
    temp = weather_data.get('main', {}).get('temp', 'N/A')
    articles = news_data.get('articles', [])
    headlines = [article.get('title', '') for article in articles[:3]] # Get first 3 headlines

    prompt = f"""
    You are DayMate, an AI assistant for daily planning.
    The current weather is {weather_desc} with a temperature of {temp}°C.
    Here are some local news headlines:
    {chr(10).join(headlines)} # Join headlines with newlines

    Based on the weather and news, provide 2-3 concise, personalized daily planning suggestions.
    Be relevant and context-aware. For example:
    - Suggest indoor activities if it's raining.
    - Mention outdoor activities if it's sunny.
    - Advise about potential schedule changes if there are traffic or emergency news alerts.
    """

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
          "temperature": 0.7,
          "maxOutputTokens": 200
        }
    }

    url = f"{settings.GEMINI_API_URL}?key={settings.GEMINI_API_KEY}"

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # Extract the generated text
        recommendation_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No recommendations generated.')
        return recommendation_text.strip()
    except requests.exceptions.RequestException as e:
        print(f"AI API Error: {e}")
        return "Sorry, I couldn't generate recommendations at the moment."
    except KeyError as e:
        print(f"AI API Response Parsing Error: {e}")
        return "Sorry, I encountered an issue processing the AI response."