import os
import httpx
# from dotenv import load_dotenv
#
# load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


AI_KEY = os.getenv("AI_API_KEY")
AI_URL = os.getenv("AI_URL")


async def generate_plan(weather, news):
	prompt = f"Create a short, actionable daily plan based on the weather and top local news.\n\n"
	prompt += f"Weather summary:\n {weather.get('current', {})}\n\n"
	prompt += f"News summary:\n"

	for x in news[:5]:
		source_name = x.get('source', {}).get('name', 'Unknown Source')
		prompt += f"- {x.get('title')} ({source_name})\n"

	prompt += "Provide: 1) Top 3 actions for the morning, 2) things to carry/avoid, 3) a 1-sentence summary."

	if not AI_KEY:
		return {
			"summary": "Could not connect to AI Agent.",
			"actions": ["Check weather app", "Review headlines", "Plan indoor alternatives"]
		}

	headers = {
		"x-goog-api-key": AI_KEY,
		"Content-Type": "application/json"
	}

	payload = {
		"contents": [{
			"parts": [{"text": prompt}]
		}],
		"generationConfig": {
			"maxOutputTokens": 300
		}
	}

	async with httpx.AsyncClient() as client:
		r = await client.post(AI_URL, json=payload, headers=headers, timeout=20)
		r.raise_for_status()
		data = r.json()

		text = ""
		if 'candidates' in data and data['candidates']:
			candidate = data['candidates'][0]
			if 'content' in candidate and 'parts' in candidate['content']:
				text = candidate['content']['parts'][0].get('text', '')

		return {"ai_text": text}