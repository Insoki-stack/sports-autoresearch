"""
fetch_news.py - Fetch sports news for sentiment analysis
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def fetch_nba_news():
    """Fetch NBA news from various sources."""
    print("="*60)
    print("Fetching NBA News")
    print("="*60)
    
    # Using a free news API (NewsAPI)
    # You'll need to get a free API key from newsapi.org
    api_key = "your_newsapi_key_here"  # Replace with actual API key
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "NBA basketball",
            "apiKey": api_key,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 20
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "published_at": article.get("publishedAt"),
                    "source": article.get("source", {}).get("name"),
                })
            
            if articles:
                df = pd.DataFrame(articles)
                output_file = CACHE_DIR / "nba_news.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(articles)} news articles to {output_file}")
                return df
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error fetching news: {e}")
        print("Note: You need a NewsAPI key. Get one free at newsapi.org")
        return None

def main():
    """Fetch news."""
    news_df = fetch_nba_news()
    
    if news_df is not None:
        print("\n" + "="*60)
        print("News Fetch Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
