"""
process_nba_nbaapi.py - Process nba_api data for training
"""

import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def process_nba_data():
    """Process nba_api data into training format"""
    input_file = CACHE_DIR / "nba_historical_nbaapi.csv"
    
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} games")
        print(f"Columns: {list(df.columns)}")
        
        # Filter for 2022-2024 seasons
        df['SEASON_ID'] = df['SEASON_ID'].astype(str)
        df_filtered = df[df['SEASON_ID'].isin(['22022', '22023', '22024'])]
        print(f"Filtered to 2022-2024: {len(df_filtered)} games")
        
        # Create training features
        processed = []
        for _, row in df_filtered.iterrows():
            try:
                processed.append({
                    'date': row.get('GAME_DATE'),
                    'season': row.get('SEASON_ID'),
                    'home_team': row.get('MATCHUP').split(' @ ')[-1] if '@' in row.get('MATCHUP', '') else row.get('MATCHUP').split(' vs. ')[-1],
                    'away_team': row.get('MATCHUP').split(' @ ')[0] if '@' in row.get('MATCHUP', '') else row.get('MATCHUP').split(' vs. ')[0],
                    'home_score': row.get('PTS') if row.get('MATCHUP', '').startswith('vs.') else row.get('PTS'),  # Need to parse properly
                    'away_score': 0,  # Need to parse from matchup
                    'winner': 1 if row.get('WL') == 'W' else 0,
                    'points': row.get('PTS'),
                    'assists': row.get('AST'),
                    'rebounds': row.get('REB'),
                    'fg_pct': row.get('FG_PCT'),
                    'fg3_pct': row.get('FG3_PCT'),
                    'ft_pct': row.get('FT_PCT'),
                })
            except Exception as e:
                continue
        
        result_df = pd.DataFrame(processed)
        output_file = CACHE_DIR / "nba_features_nbaapi.csv"
        result_df.to_csv(output_file, index=False)
        print(f"Saved {len(result_df)} processed games to {output_file}")
        print(result_df.head())
        return result_df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    process_nba_data()
