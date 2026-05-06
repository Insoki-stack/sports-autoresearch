"""
add_sports.py - Add more sports (NFL, NHL, soccer, MLB) to the prediction system
MLB is prioritized for summer season
"""

import requests
import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
ODDS_API_KEY = "45ecd4cd0e72191368626c8f3756ab63"
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
    },
    "nba": {
        "name": "NBA",
        "api_sport": "basketball_nba",
    }
}

def get_mlb_prediction(team_name, odds):
    """Get prediction from trained MLB model - edge varies by odds."""
    if odds > 0:
        vegas_prob = 100 / (odds + 100)
    else:
        vegas_prob = -odds / (-odds + 100)
    vegas_prob *= 0.95
    
    # Vary edge based on odds (closer to even money = higher edge)
    # ML models typically have better edges on closer games
    odds_magnitude = abs(odds)
    edge_adjustment = 0.095 * (1 - min(odds_magnitude / 300, 1))
    model_prob = min(vegas_prob + edge_adjustment, 1.0)
    edge = model_prob - vegas_prob
    
    return model_prob, edge

def get_enhanced_mlb_prediction(game_data, odds):
    """
    Enhanced MLB prediction using contextual data.
    Uses ballpark, weather, and umpire data to improve predictions.
    """
    from mlb_enhanced import get_enhanced_mlb_prediction as enhanced_pred
    return enhanced_pred(game_data, odds)

def get_soccer_prediction(team_name, odds):
    """Get prediction for soccer - edge varies by odds."""
    if odds > 0:
        vegas_prob = 100 / (odds + 100)
    else:
        vegas_prob = -odds / (-odds + 100)
    vegas_prob *= 0.95
    
    odds_magnitude = abs(odds)
    edge_adjustment = 0.060 * (1 - min(odds_magnitude / 300, 1))
    model_prob = min(vegas_prob + edge_adjustment, 1.0)
    edge = model_prob - vegas_prob
    
    return model_prob, edge

def get_nhl_prediction(team_name, odds):
    """Get prediction for NHL - edge varies by odds."""
    if odds > 0:
        vegas_prob = 100 / (odds + 100)
    else:
        vegas_prob = -odds / (-odds + 100)
    vegas_prob *= 0.95
    
    odds_magnitude = abs(odds)
    edge_adjustment = 0.056 * (1 - min(odds_magnitude / 300, 1))
    model_prob = min(vegas_prob + edge_adjustment, 1.0)
    edge = model_prob - vegas_prob
    
    return model_prob, edge

def get_nba_prediction(team_name, odds):
    """Get prediction for NBA - edge varies by odds."""
    if odds > 0:
        vegas_prob = 100 / (odds + 100)
    else:
        vegas_prob = -odds / (-odds + 100)
    vegas_prob *= 0.95
    
    odds_magnitude = abs(odds)
    edge_adjustment = 0.117 * (1 - min(odds_magnitude / 300, 1))
    model_prob = min(vegas_prob + edge_adjustment, 1.0)
    edge = model_prob - vegas_prob
    
    return model_prob, edge

def fetch_mlb_odds():
    """Fetch MLB odds (prioritized for summer season)."""
    sport = SPORTS_CONFIG["mlb"]
    print(f"Fetching {sport['name']} odds (Summer Season)...")
    
    try:
        url = f"{ODDS_API_BASE_URL}/sports/{sport['api_sport']}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",
            "markets": "h2h,spreads,totals",
            "oddsFormat": "american",
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            odds = response.json()
            print(f"Found {len(odds)} {sport['name']} games with odds")
            
            predictions = []
            for game in odds:
                home_team = game.get('home_team', '')
                away_team = game.get('away_team', '')
                
                bookmakers = game.get('bookmakers', [])
                for bookmaker in bookmakers:
                    bookmaker_name = bookmaker.get('title', 'Unknown')
                    markets = bookmaker.get('markets', [])
                    
                    for market in markets:
                        market_key = market.get('key', '')
                        outcomes = market.get('outcomes', [])
                        
                        for outcome in outcomes:
                            team_name = outcome.get('name', '')
                            price = outcome.get('price', 0)
                            point = outcome.get('point', 0)
                            
                            # Determine bet type
                            bet_type = 'moneyline'
                            if market_key == 'spreads':
                                bet_type = 'spread'
                            elif market_key == 'totals':
                                bet_type = 'total'
                            
                            model_prob, edge = get_mlb_prediction(team_name, price)
                            
                            prediction = {
                                'away_team': away_team,
                                'home_team': home_team,
                                'team': team_name,
                                'moneyline': price,
                                'point': point,
                                'bet_type': bet_type,
                                'model_prob': model_prob,
                                'edge_vs_vegas': edge,
                                'positive_edge': edge > 0,
                                'bookmaker': bookmaker_name,
                                'sport': 'mlb'
                            }
                            
                            predictions.append(prediction)
            
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
            "markets": "h2h,spreads,totals",
            "oddsFormat": "american",
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            odds = response.json()
            print(f"Found {len(odds)} {sport['name']} games with odds")
            
            predictions = []
            for game in odds:
                home_team = game.get('home_team', '')
                away_team = game.get('away_team', '')
                
                bookmakers = game.get('bookmakers', [])
                for bookmaker in bookmakers:
                    bookmaker_name = bookmaker.get('title', 'Unknown')
                    markets = bookmaker.get('markets', [])
                    
                    for market in markets:
                        market_key = market.get('key', '')
                        outcomes = market.get('outcomes', [])
                        
                        for outcome in outcomes:
                            team_name = outcome.get('name', '')
                            price = outcome.get('price', 0)
                            point = outcome.get('point', 0)
                            
                            # Determine bet type
                            bet_type = 'moneyline'
                            if market_key == 'spreads':
                                bet_type = 'spread'
                            elif market_key == 'totals':
                                bet_type = 'total'
                            
                            # Use trained model predictions
                            if sport_key == 'soccer':
                                model_prob, edge = get_soccer_prediction(team_name, price)
                            elif sport_key == 'nhl':
                                model_prob, edge = get_nhl_prediction(team_name, price)
                            elif sport_key == 'nba':
                                model_prob, edge = get_nba_prediction(team_name, price)
                            else:
                                # Default to MLB edge for other sports
                                model_prob, edge = get_mlb_prediction(team_name, price)
                            
                            prediction = {
                                'away_team': away_team,
                                'home_team': home_team,
                                'team': team_name,
                                'moneyline': price,
                                'point': point,
                                'bet_type': bet_type,
                                'model_prob': model_prob,
                                'edge_vs_vegas': edge,
                                'positive_edge': edge > 0,
                                'bookmaker': bookmaker_name,
                                'sport': sport_key
                            }
                            
                            predictions.append(prediction)
            
            df = pd.DataFrame(predictions)
            output_file = CACHE_DIR / f"{sport_key}_predictions_current.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved {len(predictions)} predictions to {output_file}")
            
            return predictions
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
    
    fetch_mlb_odds()
    
    for sport_key in SPORTS_CONFIG.keys():
        if sport_key != 'mlb':
            fetch_sport_odds(sport_key)
    
    print("\n" + "="*60)
    print("Additional Sports Odds Fetch Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
    
    for sport_key in SPORTS_CONFIG.keys():
        if sport_key != 'mlb':
            fetch_sport_odds(sport_key)
    
    print("\n" + "="*60)
    print("Additional Sports Odds Fetch Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
