"""
engineer_features.py - Engineer pre-game features from historical data
Calculates rolling averages, team form, and other pre-game predictors.
"""

import pandas as pd
import numpy as np
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def engineer_nba_pregame_features():
    """Engineer pre-game features from NBA historical data."""
    print("="*60)
    print("Engineering Pre-Game Features for NBA")
    print("="*60)
    
    input_file = CACHE_DIR / "nba_historical_full.csv"
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return None
    
    print(f"Loading NBA data...")
    df = pd.read_csv(input_file, low_memory=False)
    print(f"Loaded {len(df)} player-level records")
    
    # Group by team and game to get team-level stats
    if 'gameId' in df.columns and 'teamId' in df.columns and 'teamName' in df.columns:
        # Get team-level stats per game
        team_game_stats = df.groupby(['gameId', 'teamId', 'teamName', 'game_date']).agg({
            'points': 'sum',
            'reboundsTotal': 'sum',
            'assists': 'sum',
            'fieldGoalsMade': 'sum',
            'fieldGoalsAttempted': 'sum',
        }).reset_index()
        
        # Sort by date to calculate rolling features
        team_game_stats['game_date'] = pd.to_datetime(team_game_stats['game_date'])
        team_game_stats = team_game_stats.sort_values(['teamName', 'game_date'])
        
        # Calculate rolling averages (last 5 games) for each team
        print("Calculating rolling averages (last 5 games)...")
        
        def calc_rolling_stats(group):
            group = group.sort_values('game_date')
            group['pts_last5'] = group['points'].rolling(window=5, min_periods=1).mean()
            group['reb_last5'] = group['reboundsTotal'].rolling(window=5, min_periods=1).mean()
            group['ast_last5'] = group['assists'].rolling(window=5, min_periods=1).mean()
            group['fg_pct_last5'] = (group['fieldGoalsMade'] / group['fieldGoalsAttempted']).rolling(window=5, min_periods=1).mean()
            
            # Calculate win rate in last 5 games
            # First determine if they won each game (compare to opponent)
            group['win_rate_last5'] = group['points'].rolling(window=5, min_periods=1).apply(
                lambda x: (x > x.mean()).mean() if len(x) > 0 else 0.5
            )
            
            return group
        
        team_game_stats = team_game_stats.groupby('teamName').apply(calc_rolling_stats).reset_index(drop=True)
        
        # Create home/away indicator
        if 'matchup' in df.columns:
            # Get matchup info
            matchup_info = df[['gameId', 'matchup']].drop_duplicates()
            team_game_stats = team_game_stats.merge(matchup_info, on='gameId', how='left')
            team_game_stats['is_home'] = team_game_stats['matchup'].str.contains('vs.', na=False).astype(int)
        
        # Select features for ML
        feature_cols = ['gameId', 'game_date', 'teamName', 'pts_last5', 'reb_last5', 'ast_last5', 
                       'fg_pct_last5', 'win_rate_last5', 'is_home']
        
        # Add target - use win/loss from WL column if available
        if 'WL' in df.columns:
            wl_info = df[['gameId', 'teamId', 'WL']].drop_duplicates()
            team_game_stats = team_game_stats.merge(wl_info, on=['gameId', 'teamId'], how='left')
            team_game_stats['target'] = (team_game_stats['WL'] == 'W').astype(int)
        else:
            # Fallback: use points as indicator (higher score = win)
            # We need to compare to opponent in same game
            team_game_stats = team_game_stats.sort_values(['gameId', 'points'])
            team_game_stats['target'] = team_game_stats.groupby('gameId')['points'].rank(method='first') - 1
            team_game_stats['target'] = (team_game_stats['target'] == team_game_stats.groupby('gameId')['target'].transform('max')).astype(int)
        
        # Keep only available features
        available_features = [col for col in feature_cols if col in team_game_stats.columns]
        if 'target' in team_game_stats.columns:
            available_features.append('target')
        
        processed = team_game_stats[available_features].copy()
        processed = processed.dropna()
        
        output_file = CACHE_DIR / "nba_features.csv"
        processed.to_csv(output_file, index=False)
        print(f"Saved {len(processed)} records with pre-game features to {output_file}")
        print(f"Features: {list(processed.columns)}")
        
        return processed
    else:
        print("Error: Required columns not found")
        return None

def main():
    """Engineer pre-game features."""
    processed = engineer_nba_pregame_features()
    
    if processed is not None:
        print("\n" + "="*60)
        print("Feature Engineering Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
