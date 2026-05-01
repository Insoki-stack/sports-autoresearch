"""
fetch_odds_historical.py - Fetch historical odds using Odds API with daysFrom parameter
Uses the Odds API's historical data capability.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

ODDS_API_KEY = "da6e9aec8a38554193953371d6a8dca5"
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"
CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_nba_historical_odds(days_from: int = 30):
    """Fetch historical NBA odds using Odds API."""
    print("="*60)
    print(f"Fetching NBA Historical Odds (last {days_from} days)")
    print("="*60)
    
    try:
        url = f"{ODDS_API_BASE_URL}/sports/basketball_nba/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "american",
            "daysFrom": days_from,
        }
        
        print(f"Fetching from {url} with daysFrom={days_from}...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            odds_data = []
            for game in data:
                game_data = {
                    "id": game.get("id"),
                    "sport": "nba",
                    "commence_time": game.get("commence_time"),
                    "home_team": game.get("home_team"),
                    "away_team": game.get("away_team"),
                }
                
                for bookmaker in game.get("bookmakers", []):
                    for market in bookmaker.get("markets", []):
                        if market.get("key") == "h2h":
                            for outcome in market.get("outcomes", []):
                                odds_data.append({
                                    **game_data,
                                    "bookmaker": bookmaker.get("key"),
                                    "outcome": outcome.get("name"),
                                    "price": outcome.get("price"),
                                })
            
            if odds_data:
                df = pd.DataFrame(odds_data)
                output_file = CACHE_DIR / "nba_odds_historical.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} odds entries to {output_file}")
                print(f"Date range: {df['commence_time'].min()} to {df['commence_time'].max()}")
                return df
            else:
                print("No odds data found")
                return None
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Fetch historical odds."""
    # Try to get more historical data - Odds API limits how far back we can go
    print("Trying different time ranges...")
    
    for days in [7, 14, 30]:
        print(f"\nFetching last {days} days...")
        odds_df = fetch_nba_historical_odds(days_from=days)
        if odds_df is not None:
            print(f"Success: {len(odds_df)} odds entries")
    
    print("\n" + "="*60)
    print("Historical Odds Fetch Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
