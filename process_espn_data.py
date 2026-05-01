"""
process_espn_data.py - Convert ESPN API data to training format
"""

import pandas as pd
from pathlib import Path
import json

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def process_nba_espn_data():
    """Process ESPN NBA data for training."""
    espn_file = CACHE_DIR / "nba_historical_espn.csv"
    output_file = CACHE_DIR / "nba_features.csv"
    
    df = pd.read_csv(espn_file)
    
    # Extract relevant features from ESPN JSON structure
    processed_data = []
    
    for _, row in df.iterrows():
        try:
            # Extract basic info
            game_data = {
                'date': row.get('date', ''),
                'season': 2024 if '2024' in str(row.get('date', '')) else 2023,
            }
            
            # Parse competitors if available
            if 'competitions' in df.columns:
                comps_str = row['competitions']
                if isinstance(comps_str, str) and comps_str:
                    competitions = json.loads(comps_str)
                    if competitions and len(competitions) > 0:
                        comp = competitions[0]
                        competitors = comp.get('competitors', [])
                        
                        if len(competitors) >= 2:
                            home = competitors[0]
                            away = competitors[1]
                            
                            game_data['home_team'] = home.get('team', {}).get('displayName', '')
                            game_data['away_team'] = away.get('team', {}).get('displayName', '')
                            game_data['home_score'] = int(home.get('score', 0))
                            game_data['away_score'] = int(away.get('score', 0))
                            game_data['winner'] = 1 if game_data['home_score'] > game_data['away_score'] else 0
            
            processed_data.append(game_data)
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    result_df = pd.DataFrame(processed_data)
    result_df.to_csv(output_file, index=False)
    print(f"Processed {len(result_df)} NBA games to {output_file}")
    return result_df

def process_nhl_espn_data():
    """Process ESPN NHL data for training."""
    espn_file = CACHE_DIR / "nhl_historical_espn.csv"
    output_file = CACHE_DIR / "nhl_features.csv"
    
    df = pd.read_csv(espn_file)
    
    processed_data = []
    
    for _, row in df.iterrows():
        try:
            game_data = {
                'date': row.get('date', ''),
                'season': 2024 if '2024' in str(row.get('date', '')) else 2023,
            }
            
            if 'competitions' in df.columns:
                comps_str = row['competitions']
                if isinstance(comps_str, str) and comps_str:
                    competitions = json.loads(comps_str)
                    if competitions and len(competitions) > 0:
                        comp = competitions[0]
                        competitors = comp.get('competitors', [])
                        
                        if len(competitors) >= 2:
                            home = competitors[0]
                            away = competitors[1]
                            
                            game_data['home_team'] = home.get('team', {}).get('displayName', '')
                            game_data['away_team'] = away.get('team', {}).get('displayName', '')
                            game_data['home_score'] = int(home.get('score', 0))
                            game_data['away_score'] = int(away.get('score', 0))
                            game_data['winner'] = 1 if game_data['home_score'] > game_data['away_score'] else 0
            
            processed_data.append(game_data)
        except Exception as e:
            continue
    
    result_df = pd.DataFrame(processed_data)
    result_df.to_csv(output_file, index=False)
    print(f"Processed {len(result_df)} NHL games to {output_file}")
    return result_df

if __name__ == "__main__":
    print("Processing ESPN data for training...")
    process_nba_espn_data()
    process_nhl_espn_data()
    print("Processing complete!")
