"""
process_nba_data.py - Process NBA data from player-level to game-level
Aggregates box score data to create features for ML training.
"""

import pandas as pd
import numpy as np
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def process_nba_game_data():
    """Process NBA data from player-level to game-level features."""
    print("="*60)
    print("Processing NBA Data")
    print("="*60)
    
    input_file = CACHE_DIR / "nba_historical_full.csv"
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return None
    
    print(f"Loading NBA data from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} player-level records")
    
    # Check columns
    print(f"Columns: {list(df.columns[:20])}...")
    
    # Group by game to create game-level features
    print("Aggregating to game-level...")
    
    # Extract game information
    game_cols = ['gameId', 'game_date', 'matchup', 'teamId', 'teamName', 'WL']
    available_game_cols = [col for col in game_cols if col in df.columns]
    
    if available_game_cols:
        game_data = df[available_game_cols].drop_duplicates()
        print(f"Found {len(game_data)} unique games")
    else:
        print("Warning: Expected game columns not found. Using available columns.")
        game_data = df[['gameId', 'game_date']].drop_duplicates() if 'gameId' in df.columns else df
    
    # Aggregate stats by team per game
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if 'gameId' in df.columns and 'teamId' in df.columns:
        game_stats = df.groupby(['gameId', 'teamId'], as_index=False)[numeric_cols].sum()
        
        # Merge back with game info
        if 'gameId' in game_data.columns:
            game_stats = game_stats.merge(game_data, on='gameId', how='left')
        
        # Create target: home team win (based on matchup)
        if 'matchup' in game_stats.columns:
            # Extract home/away from matchup (e.g., "NJN @ CLE" means NJN is away)
            game_stats['is_home'] = game_stats['matchup'].str.contains('vs.', na=False)
            
            # Create target based on WL column if available
            if 'WL' in game_stats.columns:
                game_stats['target'] = (game_stats['WL'] == 'W').astype(int)
            else:
                # Fallback: create simple target
                game_stats['target'] = 0
        
        # Select key features
        feature_cols = ['gameId', 'game_date', 'teamId', 'teamName', 'target', 'points', 'reboundsTotal', 'assists']
        available_features = [col for col in feature_cols if col in game_stats.columns]
        
        if not available_features:
            # Use whatever numeric columns we have
            available_features = ['gameId', 'target'] + [col for col in game_stats.columns if col not in ['gameId', 'target']][:10]
        
        processed = game_stats[available_features].copy()
        
        output_file = CACHE_DIR / "nba_processed.csv"
        processed.to_csv(output_file, index=False)
        print(f"Saved {len(processed)} game-level records to {output_file}")
        
        return processed
    else:
        print("Error: gameId or teamId not found in data")
        return None

def main():
    """Process NBA data."""
    processed = process_nba_game_data()
    
    if processed is not None:
        print("\n" + "="*60)
        print("NBA Data Processing Complete!")
        print("="*60)
        print(f"Final shape: {processed.shape}")
        print(f"Columns: {list(processed.columns)}")

if __name__ == "__main__":
    main()
