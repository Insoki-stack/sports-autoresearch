"""
process_premier_league.py - Process Premier League data for training
"""

import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def process_premier_league():
    """Process Premier League data into training format"""
    files = [
        CACHE_DIR / "soccer_premier_2223.csv",
        CACHE_DIR / "soccer_premier_2324.csv"
    ]
    
    all_data = []
    
    for file in files:
        try:
            df = pd.read_csv(file)
            print(f"Loaded {len(df)} games from {file.name}")
            
            processed = []
            for _, row in df.iterrows():
                try:
                    processed.append({
                        'date': row.get('Date'),
                        'home_team': row.get('HomeTeam'),
                        'away_team': row.get('AwayTeam'),
                        'home_score': row.get('FTHG'),
                        'away_score': row.get('FTAG'),
                        'winner': 1 if row.get('FTR') == 'H' else 0,
                        'home_shots': row.get('HS'),
                        'away_shots': row.get('AS'),
                        'home_shots_target': row.get('HST'),
                        'away_shots_target': row.get('AST'),
                        'home_corners': row.get('HC'),
                        'away_corners': row.get('AC'),
                    })
                except Exception:
                    continue
            
            all_data.extend(processed)
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    if all_data:
        result_df = pd.DataFrame(all_data)
        output_file = CACHE_DIR / "soccer_features.csv"
        result_df.to_csv(output_file, index=False)
        print(f"\nSaved {len(result_df)} total soccer games to {output_file}")
        print(result_df.head())
        return result_df
    else:
        print("No data processed")
        return None

if __name__ == "__main__":
    process_premier_league()
