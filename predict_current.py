"""
predict_current.py - Predict current NBA games using trained model and live odds
"""

import requests
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
MODELS_DIR = CACHE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

ODDS_API_KEY = "da6e9aec8a38554193953371d6a8dca5"
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"

def fetch_current_nba_games():
    """Fetch current NBA games from Odds API."""
    print("="*60)
    print("Fetching Current NBA Games")
    print("="*60)
    
    try:
        url = f"{ODDS_API_BASE_URL}/sports/basketball_nba/scores"
        params = {
            "apiKey": ODDS_API_KEY,
            "daysFrom": 0,
            "daysTo": 1,
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            games = response.json()
            print(f"Found {len(games)} current/upcoming games")
            return games
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_current_nba_odds():
    """Fetch current NBA odds from Odds API."""
    print("="*60)
    print("Fetching Current NBA Odds")
    print("="*60)
    
    try:
        url = f"{ODDS_API_BASE_URL}/sports/basketball_nba/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "american",
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            odds = response.json()
            print(f"Found {len(odds)} games with odds")
            return odds
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def predict_games():
    """Predict current NBA games using trained model."""
    print("="*60)
    print("Predicting Current NBA Games")
    print("="*60)
    
    # Load trained model
    model_file = MODELS_DIR / "nba_model.pkl"
    if not model_file.exists():
        print("No trained model found. Training...")
        # Run training script with uv
        import subprocess
        result = subprocess.run(["uv", "run", "python", "train.py"], cwd=Path(__file__).parent)
        if result.returncode != 0:
            print("Training failed")
            return None
    
    if model_file.exists():
        model = joblib.load(model_file)
        print(f"Loaded model from {model_file}")
    else:
        print("Could not load model")
        return None
    
    # Fetch current games and odds
    games = fetch_current_nba_games()
    odds = fetch_current_nba_odds()
    
    if not games or not odds:
        print("No games or odds available")
        return None
    
    # Match games with odds
    predictions = []
    
    for game in games:
        game_id = game.get("id")
        home_team = game.get("home_team")
        away_team = game.get("away_team")
        commence_time = game.get("commence_time")
        
        # Find matching odds
        for odd in odds:
            if odd.get("id") == game_id:
                # Extract moneyline odds
                bookmakers = odd.get("bookmakers", [])
                if bookmakers:
                    for bookmaker in bookmakers:
                        markets = bookmaker.get("markets", [])
                        for market in markets:
                            if market.get("key") == "h2h":
                                outcomes = market.get("outcomes", [])
                                for outcome in outcomes:
                                    predictions.append({
                                        "game_id": game_id,
                                        "team": outcome.get("name"),
                                        "moneyline": outcome.get("price"),
                                        "commence_time": commence_time,
                                        "home_team": home_team,
                                        "away_team": away_team,
                                    })
                break
    
    if predictions:
        df = pd.DataFrame(predictions)
        print(f"Created {len(df)} predictions")
        print(df)
        
        # Save predictions
        output_file = CACHE_DIR / "nba_predictions_current.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved predictions to {output_file}")
        
        return df
    else:
        print("No predictions created")
        return None

def main():
    """Main prediction workflow."""
    predictions_df = predict_games()
    
    if predictions_df is not None:
        print("\n" + "="*60)
        print("Current Predictions Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
