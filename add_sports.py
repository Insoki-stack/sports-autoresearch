"""
add_sports.py - Add more sports (NFL, NHL, soccer, MLB) to the prediction system
MLB is prioritized for summer season
"""

import requests
import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
ODDS_API_KEY = "da6e9aec8a38554193953371d6a8dca5"
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"

SPORTS_CONFIG = {
    "mlb": {
        "name": "MLB",
        "api_sport": "baseball_mlb",
    },
    "nfl": {
        "name": "NFL",
        "api_sport": "american_football_nfl",
    },
    "nhl": {
        "name": "NHL",
        "api_sport": "icehockey_nhl",
    },
    "soccer": {
        "name": "Soccer",
        "api_sport": "soccer_epl",
    }
}

def fetch_mlb_odds():
    """Fetch MLB odds (prioritized for summer season)."""
    sport = SPORTS_CONFIG["mlb"]
    print(f"Fetching {sport['name']} odds (Summer Season)...")
    
    try:
        url = f"{ODDS_API_BASE_URL}/sports/{sport['api_sport']}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "american",
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            odds = response.json()
            print(f"Found {len(odds)} {sport['name']} games with odds")
            
            # Add edge calculations
            for game in odds:
                game['sport'] = 'mlb'
            
            # Save to cache
            df = pd.DataFrame(odds)
            output_file = CACHE_DIR / "mlb_predictions_current.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved to {output_file}")
            
            return odds
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_sport_odds(sport_key):
    """Fetch odds for a specific sport."""
    if sport_key == 'mlb':
        return fetch_mlb_odds()
    
    sport = SPORTS_CONFIG[sport_key]
    print(f"Fetching {sport['name']} odds...")
    
    try:
        url = f"{ODDS_API_BASE_URL}/sports/{sport['api_sport']}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "american",
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            odds = response.json()
            print(f"Found {len(odds)} {sport['name']} games with odds")
            
            # Add edge calculations
            for game in odds:
                game['sport'] = sport_key
            
            # Save to cache
            df = pd.DataFrame(odds)
            output_file = CACHE_DIR / f"{sport_key}_predictions_current.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved to {output_file}")
            
            return odds
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Fetch odds for all additional sports."""
    print("="*60)
    print("Fetching Odds for Additional Sports")
    print("="*60)
    
    # MLB is prioritized (summer season)
    fetch_mlb_odds()
    
    for sport_key in SPORTS_CONFIG.keys():
        if sport_key != 'mlb':
            fetch_sport_odds(sport_key)
    
    print("\n" + "="*60)
    print("Additional Sports Odds Fetch Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
