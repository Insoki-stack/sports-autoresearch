"""
fetch_odds.py - Fetch betting odds from The Odds API
Run this script to download odds data for sports betting.
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import time

# API Configuration
ODDS_API_KEY = "da6e9aec8a38554193953371d6a8dca5"
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"
CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Sport mapping for Odds API
SPORTS_MAP = {
    "mlb": "baseball_mlb",
    "nba": "basketball_nba",
    # Golf and Tennis use specific tournaments, not general sport keys
    # For now, we'll skip them or use specific tournaments when in season
}

def fetch_odds_for_sport(sport: str, days_from: int = 1) -> pd.DataFrame:
    """Fetch odds for a specific sport from Odds API."""
    if sport not in SPORTS_MAP:
        print(f"Sport {sport} not supported by Odds API")
        return pd.DataFrame()
    
    sport_key = SPORTS_MAP[sport]
    odds_data = []
    
    try:
        # Fetch odds for the sport
        url = f"{ODDS_API_BASE_URL}/sports/{sport_key}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us,uk",
            "markets": "h2h",
            "oddsFormat": "american",
            "daysFrom": days_from,
        }
        
        print(f"Fetching {sport.upper()} odds from Odds API...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            for game in data:
                game_data = {
                    "id": game.get("id"),
                    "sport": sport,
                    "commence_time": game.get("commence_time"),
                    "home_team": game.get("home_team"),
                    "away_team": game.get("away_team"),
                }
                
                # Extract odds from bookmakers
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
                print(f"Fetched {len(df)} odds entries for {sport}")
                return df
            else:
                print(f"No odds data found for {sport}")
                return pd.DataFrame()
        else:
            print(f"Error fetching odds for {sport}: {response.status_code}")
            print(f"Response: {response.text}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error fetching odds for {sport}: {e}")
        return pd.DataFrame()

def main():
    """Fetch odds for all sports."""
    print("="*60)
    print("Sports Odds Fetcher (The Odds API)")
    print("="*60)
    
    # Fetch odds for each sport
    sports = ["mlb", "nba"]  # Only MLB and NBA have general sport keys
    
    for sport in sports:
        print(f"\n{'='*60}")
        print(f"Fetching {sport.upper()} Odds")
        print(f"{'='*60}")
        
        odds_df = fetch_odds_for_sport(sport, days_from=3)
        
        if not odds_df.empty:
            odds_file = CACHE_DIR / f"{sport}_odds.csv"
            odds_df.to_csv(odds_file, index=False)
            print(f"✅ Saved {len(odds_df)} odds entries to {odds_file}")
        else:
            print(f"❌ No odds data for {sport}")
    
    print("\n" + "="*60)
    print("Odds Fetch Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
