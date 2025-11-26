# import requests
# from app.core.config import settings
#
#
# def generate_recommendations(weather_data: dict, news_data: dict) -> str:
#     if not weather_data or not news_data:
#         return "Unable to generate recommendations due to missing data."
#
#     weather_desc = weather_data.get('weather', [{}])[0].get('description', 'Unknown')
#     temp = weather_data.get('main', {}).get('temp', 'N/A')
#     articles = news_data.get('articles', [])
#     headlines = [article.get('title', '') for article in articles[:3]] # Get first 3 headlines
#
#     prompt = f"""
#     You are DayMate, an AI assistant for daily planning.
#     The current weather is {weather_desc} with a temperature of {temp}°C.
#     Here are some local news headlines:
#     {chr(10).join(headlines)} # Join headlines with newlines
#
#     Based on the weather and news, provide 2-3 concise, personalized daily planning suggestions.
#     Be relevant and context-aware. For example:
#     - Suggest indoor activities if it's raining.
#     - Mention outdoor activities if it's sunny.
#     - Advise about potential schedule changes if there are traffic or emergency news alerts.
#     """
#
#     headers = {
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "contents": [{
#             "parts": [{
#                 "text": prompt
#             }]
#         }],
#         "generationConfig": {
#           "temperature": 0.7,
#           "maxOutputTokens": 200
#         }
#     }
#
#     url = f"{settings.GEMINI_API_URL}?key={settings.GEMINI_API_KEY}"
#
#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
#         result = response.json()
#         # Extract the generated text
#         recommendation_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No recommendations generated.')
#         return recommendation_text.strip()
#     except requests.exceptions.RequestException as e:
#         print(f"AI API Error: {e}")
#         return "Sorry, I couldn't generate recommendations at the moment."
#     except KeyError as e:
#         print(f"AI API Response Parsing Error: {e}")
#         return "Sorry, I encountered an issue processing the AI response."

import requests
from app.core.config import settings
from datetime import datetime


def format_forecast_summary(weather_data: dict) -> str:
    """Extract and format forecast summary for the AI prompt"""
    forecast_type = weather_data.get('forecast_type', 'none')

    if forecast_type == 'hourly' and weather_data.get('hourly_forecast'):
        # Use hourly forecast (next 12 hours)
        hourly = weather_data['hourly_forecast'][:12]
        summary = "Next 12 hours forecast:\n"
        for i, hour in enumerate(hourly):
            time = datetime.fromtimestamp(hour['dt']).strftime('%I%p')
            temp = hour['temp']
            desc = hour['weather'][0]['description']
            summary += f"- {time}: {temp}°C, {desc}\n"
        return summary

    elif forecast_type == '3-hour' and weather_data.get('forecast_list'):
        # Use 3-hour forecast (next 24 hours)
        forecast = weather_data['forecast_list'][:8]  # 8 * 3 = 24 hours
        summary = "Next 24 hours forecast:\n"
        for item in forecast:
            time = datetime.fromtimestamp(item['dt']).strftime('%I%p')
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            summary += f"- {time}: {temp}°C, {desc}\n"
        return summary

    return "No forecast data available."


def generate_recommendations(weather_data: dict, news_data: dict) -> str:
    if not weather_data or not news_data:
        return "Unable to generate recommendations due to missing data."

    # Current weather
    current = weather_data.get('current', {})
    weather_desc = current.get('weather', [{}])[0].get('description', 'Unknown')
    temp = current.get('main', {}).get('temp', 'N/A')

    # Forecast summary
    forecast_summary = format_forecast_summary(weather_data)

    # News
    articles = news_data.get('articles', [])
    headlines = [article.get('title', '') for article in articles[:3]]

    prompt = f"""
You are DayMate, an AI assistant for daily planning in Dhaka, Bangladesh.

CURRENT WEATHER:
- Condition: {weather_desc}
- Temperature: {temp}°C

FORECAST:
{forecast_summary}

LOCAL NEWS HEADLINES:
{chr(10).join(headlines) if headlines else "No news available"}

Based on this information, provide 3-4 personalized daily planning suggestions:

1. WEATHER-BASED ADVICE:
   - Comment on current conditions and how they'll change throughout the day
   - Suggest appropriate clothing/accessories (umbrella, sunscreen, etc.)
   - Recommend indoor vs outdoor activities based on forecast

2. SCHEDULE OPTIMIZATION:
   - Suggest best times for outdoor activities based on forecast
   - Warn about weather changes (rain, temperature drops, etc.)

3. LOCAL CONTEXT:
   - If news mentions traffic, events, or emergencies, incorporate that into planning
   - Suggest timing adjustments based on local conditions

4. HEALTH & COMFORT:
   - Hydration reminders if hot
   - Air quality considerations if relevant
   - Exercise timing based on temperature

Keep suggestions practical, concise, and specific to Dhaka. Use a friendly, helpful tone.
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
            "maxOutputTokens": 300
        }
    }

    url = f"{settings.GEMINI_API_URL}?key={settings.GEMINI_API_KEY}"

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        recommendation_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text',
                                                                                                             'No recommendations generated.')
        return recommendation_text.strip()
    except requests.exceptions.RequestException as e:
        print(f"AI API Error: {e}")
        return "Sorry, I couldn't generate recommendations at the moment."
    except KeyError as e:
        print(f"AI API Response Parsing Error: {e}")
        return "Sorry, I encountered an issue processing the AI response."