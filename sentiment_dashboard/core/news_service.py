import os
import requests
from typing import List
from models.schemas import NewsArticle
from datetime import datetime, timedelta, timezone

class NewsService:
    """Handles all outbound communication with the NewsAPI.org service."""
    
    def __init__(self):
        
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        
        if not self.api_key:
            raise ValueError("CRITICAL: NEWS_API_KEY environment variable is missing.")

    def fetch_recent_news(self, search_term: str, limit: int = 10) -> List[NewsArticle]:
        """
        Fetches the most recent articles for a given keyword.
        """
        two_days_ago = (datetime.now(timezone.utc) - timedelta(days=2)).strftime('%Y-%m-%d')

        params = {
            "q": search_term,
            "searchIn": "title",
            "language": "en",
            "from": two_days_ago,    #  makes sure news only 2 days old
            "sortBy": "relevancy",   # makes sure its only about topic and not random articles
            "pageSize": limit,
            "apiKey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            
            articles = []
            for item in data.get("articles", []):
                # Map the raw JSON payload to our strictly typed Data Model
                article = NewsArticle(
                    title=item.get("title", "No Title"),
                    source=item.get("source", {}).get("name", "Unknown Source"),
                    url=item.get("url", "")
                )
                articles.append(article)
                
            return articles
            
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred while fetching news: {e}")
            return []