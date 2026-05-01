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
            
            # Parse and flatten data to match dashboard format
            predictions = []
            for game in odds:
                home_team = game.get('home_team', '')
                away_team = game.get('away_team', '')
                
                # Extract odds from each bookmaker
                bookmakers = game.get('bookmakers', [])
                for bookmaker in bookmakers:
                    bookmaker_name = bookmaker.get('title', 'Unknown')
                    markets = bookmaker.get('markets', [])
                    
                    for market in markets:
                        if market.get('key') == 'h2h':
                            outcomes = market.get('outcomes', [])
                            for outcome in outcomes:
                                team_name = outcome.get('name', '')
                                price = outcome.get('price', 0)
                                
                                # Create prediction entry
                                prediction = {
                                    'away_team': away_team,
                                    'home_team': home_team,
                                    'team': team_name,
                                    'moneyline': price,
                                    'model_prob': 0.5,
                                    'edge_vs_vegas': 0.0,
                                    'positive_edge': False,
                                    'bookmaker': bookmaker_name,
                                    'sport': 'mlb'
                                }
                                
                                # Calculate edge (simplified)
                                if price > 0:
                                    vegas_prob = 100 / (price + 100)
                                else:
                                    vegas_prob = -price / (-price + 100)
                                vegas_prob *= 0.95
                                
                                edge = 0.5 - vegas_prob
                                prediction['edge_vs_vegas'] = edge
                                prediction['positive_edge'] = edge > 0
                                prediction['model_prob'] = min(vegas_prob + edge, 1.0)
                                
                                predictions.append(prediction)
            
            # Save to cache
            df = pd.DataFrame(predictions)
            output_file = CACHE_DIR / "mlb_predictions_current.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved {len(predictions)} predictions to {output_file}")
            
            return predictions
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
            
            # Parse and flatten data to match dashboard format
            predictions = []
            for game in odds:
                home_team = game.get('home_team', '')
                away_team = game.get('away_team', '')
                
                # Extract odds from each bookmaker
                bookmakers = game.get('bookmakers', [])
                for bookmaker in bookmakers:
                    bookmaker_name = bookmaker.get('title', 'Unknown')
                    markets = bookmaker.get('markets', [])
                    
                    for market in markets:
                        if market.get('key') == 'h2h':
                            outcomes = market.get('outcomes', [])
                            for outcome in outcomes:
                                team_name = outcome.get('name', '')
                                price = outcome.get('price', 0)
                                
                                # Create prediction entry
                                prediction = {
                                    'away_team': away_team,
                                    'home_team': home_team,
                                    'team': team_name,
                                    'moneyline': price,
                                    'model_prob': 0.5,
                                    'edge_vs_vegas': 0.0,
                                    'positive_edge': False,
                                    'bookmaker': bookmaker_name,
                                    'sport': sport_key
                                }
                                
                                # Calculate edge (simplified)
                                if price > 0:
                                    vegas_prob = 100 / (price + 100)
                                else:
                                    vegas_prob = -price / (-price + 100)
                                vegas_prob *= 0.95
                                
                                edge = 0.5 - vegas_prob
                                prediction['edge_vs_vegas'] = edge
                                prediction['positive_edge'] = edge > 0
                                prediction['model_prob'] = min(vegas_prob + edge, 1.0)
                                
                                predictions.append(prediction)
            
            # Save to cache
            df = pd.DataFrame(predictions)
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
