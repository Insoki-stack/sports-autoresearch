"""
engineer_current_features.py - Engineer features for current/live games
Extracts pre-game features for current NBA games to make real model predictions.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def engineer_current_game_features(current_games):
    """Engineer pre-game features for current NBA games."""
    print("="*60)
    print("Engineering Features for Current Games")
    print("="*60)
    
    # Load historical features
    features_file = CACHE_DIR / "nba_features_with_injuries.csv"
    if not features_file.exists():
        print("No historical features found")
        return current_games
    
    historical_df = pd.read_csv(features_file)
    print(f"Loaded {len(historical_df)} historical features")
    
    # Calculate team-level rolling averages from historical data
    team_stats = historical_df.groupby('teamName').agg({
        'pts_last5': 'mean',
        'reb_last5': 'mean',
        'ast_last5': 'mean',
        'fg_pct_last5': 'mean',
        'win_rate_last5': 'mean',
        'injury_count': 'mean',
    }).reset_index()
    
    # Map team names (normalize for matching)
    team_name_map = {
        'Los Angeles Lakers': 'Lakers',
        'Boston Celtics': 'Celtics',
        'Golden State Warriors': 'Warriors',
        'Miami Heat': 'Heat',
        # Add more mappings as needed
    }
    
    # Add features to current games
    for game in current_games:
        home_team = game.get('home_team', '')
        away_team = game.get('away_team', '')
        
        # Find matching team stats (simple string matching)
        home_stats = team_stats[team_stats['teamName'].str.contains(home_team, case=False, na=False)]
        away_stats = team_stats[team_stats['teamName'].str.contains(away_team, case=False, na=False)]
        
        if len(home_stats) > 0:
            game['home_pts_last5'] = home_stats['pts_last5'].values[0]
            game['home_reb_last5'] = home_stats['reb_last5'].values[0]
            game['home_ast_last5'] = home_stats['ast_last5'].values[0]
            game['home_win_rate'] = home_stats['win_rate_last5'].values[0]
            game['home_injury_count'] = home_stats['injury_count'].values[0]
        else:
            game['home_pts_last5'] = historical_df['pts_last5'].mean()
            game['home_reb_last5'] = historical_df['reb_last5'].mean()
            game['home_ast_last5'] = historical_df['ast_last5'].mean()
            game['home_win_rate'] = historical_df['win_rate_last5'].mean()
            game['home_injury_count'] = 0
        
        if len(away_stats) > 0:
            game['away_pts_last5'] = away_stats['pts_last5'].values[0]
            game['away_reb_last5'] = away_stats['reb_last5'].values[0]
            game['away_ast_last5'] = away_stats['ast_last5'].values[0]
            game['away_win_rate'] = away_stats['win_rate_last5'].values[0]
            game['away_injury_count'] = away_stats['injury_count'].values[0]
        else:
            game['away_pts_last5'] = historical_df['pts_last5'].mean()
            game['away_reb_last5'] = historical_df['reb_last5'].mean()
            game['away_ast_last5'] = historical_df['ast_last5'].mean()
            game['away_win_rate'] = historical_df['win_rate_last5'].mean()
            game['away_injury_count'] = 0
    
    return current_games

def main():
    """Test feature engineering."""
    # Load current predictions to test
    predictions_file = CACHE_DIR / "nba_predictions_current.csv"
    if predictions_file.exists():
        df = pd.read_csv(predictions_file)
        games = df.to_dict('records')
        engineered = engineer_current_game_features(games)
        print(f"Engineered features for {len(engineered)} games")
    else:
        print("No current predictions found")

if __name__ == "__main__":
    main()
