"""
combine_historical_odds.py - Combine and align historical odds from Sports Reference
"""

import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def combine_sports_reference_odds():
    """Combine odds from multiple Sports Reference seasons."""
    print("="*60)
    print("Combining Historical Odds from Sports Reference")
    print("="*60)
    
    all_odds = []
    
    for year in [2021, 2022, 2023, 2024]:
        file_path = CACHE_DIR / f"nba_odds_sports_reference_{year}.csv"
        if file_path.exists():
            df = pd.read_csv(file_path)
            print(f"Loaded {len(df)} records from {year}")
            all_odds.append(df)
    
    if all_odds:
        combined = pd.concat(all_odds, ignore_index=True)
        output_file = CACHE_DIR / "nba_odds_historical_combined.csv"
        combined.to_csv(output_file, index=False)
        print(f"Saved {len(combined)} total records to {output_file}")
        print(f"Columns: {list(combined.columns)}")
        print(f"Date range: {combined['date'].min()} to {combined['date'].max()}")
        return combined
    else:
        print("No odds data found")
        return None

def main():
    """Combine historical odds."""
    combined_df = combine_sports_reference_odds()
    
    if combined_df is not None:
        print("\n" + "="*60)
        print("Historical Odds Combination Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
