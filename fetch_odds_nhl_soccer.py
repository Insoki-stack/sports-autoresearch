"""
fetch_odds_nhl_soccer.py - Fetch real odds for NHL and soccer from The Odds API
"""

import requests
import pandas as pd
from pathlib import Path
import os

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
ODDS_API_KEY = os.getenv('ODDS_API_KEY', 'your_api_key_here')

def fetch_nhl_odds():
    """Fetch NHL odds from The Odds API"""
    url = "https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched {len(data)} NHL games with odds")
            
            processed = []
            for game in data:
                try:
                    bookmakers = game.get('bookmakers', [])
                    if bookmakers:
                        bm = bookmakers[0]  # Use first bookmaker
                        outcomes = bm.get('markets', [{}])[0].get('outcomes', [])
                        
                        if len(outcomes) >= 2:
                            home_outcome = outcomes[0]
                            away_outcome = outcomes[1]
                            
                            processed.append({
                                'game_id': game.get('id'),
                                'home_team': game.get('home_team'),
                                'away_team': game.get('away_team'),
                                'home_odds': home_outcome.get('price'),
                                'away_odds': away_outcome.get('price'),
                                'commence_time': game.get('commence_time')
                            })
                except Exception:
                    continue
            
            if processed:
                df = pd.DataFrame(processed)
                output_file = CACHE_DIR / "nhl_odds.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} NHL odds to {output_file}")
                return df
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_soccer_odds():
    """Fetch soccer odds from The Odds API"""
    url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched {len(data)} soccer games with odds")
            
            processed = []
            for game in data:
                try:
                    bookmakers = game.get('bookmakers', [])
                    if bookmakers:
                        bm = bookmakers[0]
                        outcomes = bm.get('markets', [{}])[0].get('outcomes', [])
                        
                        if len(outcomes) >= 2:
                            home_outcome = outcomes[0]
                            away_outcome = outcomes[1]
                            
                            processed.append({
                                'game_id': game.get('id'),
                                'home_team': game.get('home_team'),
                                'away_team': game.get('away_team'),
                                'home_odds': home_outcome.get('price'),
                                'away_odds': away_outcome.get('price'),
                                'commence_time': game.get('commence_time')
                            })
                except Exception:
                    continue
            
            if processed:
                df = pd.DataFrame(processed)
                output_file = CACHE_DIR / "soccer_odds.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} soccer odds to {output_file}")
                return df
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Fetching odds from The Odds API...")
    fetch_nhl_odds()
    fetch_soccer_odds()
