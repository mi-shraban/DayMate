import os
import httpx
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

API_KEY = os.getenv("NEWSAPI_KEY")
BASE = "https://newsapi.org/v2/everything"


async def get_local_news(query):
	if not API_KEY:
		raise Exception("No API key provided")
	params = {
		"q": query,
		"pageSize": 10,
		"apiKey": API_KEY,
		"sortBy": "publishedAt",
	}
	async with httpx.AsyncClient(timeout=10) as client:
		r = await client.get(BASE, params=params)
		r.raise_for_status()
		return r.json().get('articles', [])


# New function to print news data cleanly
# async def print_news(query):
# 	try:
# 		print(f"🔍 Fetching news for: '{query}'\n")
# 		articles = await get_local_news(query)
#
# 		if not articles:
# 			print("📭 No articles found!")
# 			return
#
# 		print(f"📰 Found {len(articles)} articles:\n")
# 		print("=" * 100)
#
# 		for i, article in enumerate(articles, 1):
# 			# Handle missing fields gracefully
# 			title = article.get('title', 'N/A') or 'N/A'
# 			source = article.get('source', {}).get('name', 'N/A')
# 			published_at = article.get('publishedAt', 'N/A')
# 			url = article.get('url', '#')
#
# 			# Format date nicely (if available)
# 			if published_at != 'N/A':
# 				try:
# 					dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
# 					published_at = dt.strftime('%Y-%m-%d %H:%M UTC')
# 				except:
# 					pass  # Keep original if parsing fails
#
# 			print(f"{i}. {title}")
# 			print(f"   📰 Source: {source}")
# 			print(f"   ⏰ Published: {published_at}")
# 			print(f"   🔗 URL: {url}")
# 			print("-" * 100)
#
# 	except httpx.HTTPStatusError as e:
# 		print(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
# 	except httpx.RequestError as e:
# 		print(f"❌ Request Error: {str(e)}")
# 	except Exception as e:
# 		print(f"❌ Error: {str(e)}")
#
#
# if __name__ == "__main__":
# 	asyncio.run(print_news("Dhaka"))