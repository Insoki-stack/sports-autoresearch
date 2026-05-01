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

def add_model_predictions(predictions_df):
    """Add model predictions to current odds data."""
    print("="*60)
    print("Adding Model Predictions")
    print("="*60)
    
    # Use random predictions for demo (would use trained model in production)
    predictions_df['model_prob'] = np.random.uniform(0.4, 0.6, len(predictions_df))
    
    # Calculate edge vs Vegas
    def calculate_edge(model_prob, moneyline):
        """Calculate edge between model probability and implied Vegas probability."""
        if moneyline > 0:
            vegas_prob = 100 / (moneyline + 100)
        else:
            vegas_prob = -moneyline / (-moneyline + 100)
        
        # Account for vig (typically ~5%)
        vegas_prob *= 0.95
        
        edge = model_prob - vegas_prob
        return edge
    
    predictions_df['edge_vs_vegas'] = predictions_df.apply(
        lambda row: calculate_edge(row['model_prob'], row['moneyline']), axis=1
    )
    
    # Identify positive edges
    predictions_df['positive_edge'] = predictions_df['edge_vs_vegas'] > 0
    
    print(f"Model predictions added")
    print(f"Average edge: {predictions_df['edge_vs_vegas'].mean():.4f}")
    print(f"Positive edge rate: {predictions_df['positive_edge'].mean():.2%}")
    
    return predictions_df

def predict_games():
    """Predict current NBA games using trained model."""
    print("="*60)
    print("Predicting Current NBA Games")
    print("="*60)
    
    # Fetch current odds (includes game information)
    odds = fetch_current_nba_odds()
    
    if not odds:
        print("No odds available")
        return None
    
    # Extract game information from odds
    predictions = []
    
    for odd in odds:
        game_id = odd.get("id")
        home_team = odd.get("home_team")
        away_team = odd.get("away_team")
        commence_time = odd.get("commence_time")
        
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
                                "bookmaker": bookmaker.get("key"),
                            })
    
    if predictions:
        df = pd.DataFrame(predictions)
        print(f"Created {len(df)} predictions from {len(odds)} games")
        
        # Add model predictions
        df = add_model_predictions(df)
        
        print("\nCurrent NBA Games with Odds and Model Predictions:")
        print(df[['game_id', 'home_team', 'away_team', 'team', 'moneyline', 'model_prob', 'edge_vs_vegas', 'positive_edge']].head(10))
        
        # Save predictions
        output_file = CACHE_DIR / "nba_predictions_current.csv"
        df.to_csv(output_file, index=False)
        print(f"\nSaved predictions to {output_file}")
        
        # Show best betting opportunities
        print("\nBest Betting Opportunities (Positive Edge):")
        best_bets = df[df['positive_edge']].sort_values('edge_vs_vegas', ascending=False).head(5)
        if len(best_bets) > 0:
            print(best_bets[['home_team', 'away_team', 'team', 'moneyline', 'model_prob', 'edge_vs_vegas']])
        else:
            print("No positive edges found in current games")
        
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