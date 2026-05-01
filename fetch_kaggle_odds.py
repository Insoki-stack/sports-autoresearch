"""
fetch_kaggle_odds.py - Fetch historical betting odds from direct CSV sources
Downloads NBA betting odds from GitHub and other free sources.
"""

import requests
import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Direct CSV sources for historical odds
ODDS_SOURCES = {
    "nba_historical_odds": "https://raw.githubusercontent.com/erikvdven/nba_historical_betting_data/master/nba_historical_betting_data.csv",
}

def fetch_historical_odds():
    """Fetch historical odds from direct CSV sources."""
    print("="*60)
    print("Fetching Historical Odds from Direct Sources")
    print("="*60)
    
    for name, url in ODDS_SOURCES.items():
        try:
            print(f"Downloading {name} from {url}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            output_file = CACHE_DIR / f"{name}.csv"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            # Load and check
            df = pd.read_csv(output_file)
            print(f"Saved {len(df)} odds records to {output_file}")
            print(f"Columns: {list(df.columns)[:10]}...")
            return df
            
        except Exception as e:
            print(f"Error downloading {name}: {e}")
    
    return None

def main():
    """Fetch historical odds."""
    odds_df = fetch_historical_odds()
    
    if odds_df is not None:
        print("\n" + "="*60)
        print("Historical Odds Fetch Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
