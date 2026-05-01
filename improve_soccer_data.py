"""
improve_soccer_data.py - Add advanced features to soccer data
"""

import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def improve_soccer_data():
    """Add advanced features to soccer data"""
    input_file = CACHE_DIR / "soccer_features.csv"
    
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} soccer games")
        
        # Calculate advanced features
        df['total_shots'] = df['home_shots'] + df['away_shots']
        df['total_shots_target'] = df['home_shots_target'] + df['away_shots_target']
        df['total_corners'] = df['home_corners'] + df['away_corners']
        df['shot_accuracy_home'] = (df['home_shots_target'] / df['home_shots']).fillna(0)
        df['shot_accuracy_away'] = (df['away_shots_target'] / df['away_shots']).fillna(0)
        df['corner_ratio'] = (df['home_corners'] / df['total_corners']).fillna(0)
        
        # Sort by date for rolling averages
        df = df.sort_values('date')
        
        # Calculate rolling averages
        df['rolling_home_score'] = df.groupby('home_team')['home_score'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
        df['rolling_away_score'] = df.groupby('away_team')['away_score'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
        df['rolling_total_shots'] = df['total_shots'].rolling(window=5, min_periods=1).mean()
        
        # Create target
        df['target'] = df['winner']
        
        output_file = CACHE_DIR / "soccer_features.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved improved soccer data to {output_file}")
        print(f"Features: {list(df.columns)}")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    improve_soccer_data()
