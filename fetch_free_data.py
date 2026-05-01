"""
fetch_free_data.py - Fetch free historical sports data from internet sources
Downloads CSV files from GitHub and uses pybaseball for MLB data.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Free data sources
NBA_DATA_SOURCES = {
    "regular_season_part1": "https://raw.githubusercontent.com/NocturneBear/NBA-Data-2010-2024/main/regular_season_box_scores_2010_2024_part_1.csv",
    "regular_season_part2": "https://raw.githubusercontent.com/NocturneBear/NBA-Data-2010-2024/main/regular_season_box_scores_2010_2024_part_2.csv",
    "regular_season_part3": "https://raw.githubusercontent.com/NocturneBear/NBA-Data-2010-2024/main/regular_season_box_scores_2010_2024_part_3.csv",
    "regular_season_totals": "https://raw.githubusercontent.com/NocturneBear/NBA-Data-2010-2024/main/regular_season_totals_2010_2024.csv",
}

def download_csv(url: str, output_path: Path) -> bool:
    """Download a CSV file from URL."""
    try:
        print(f"Downloading {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded to {output_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def fetch_nba_data():
    """Fetch NBA historical data from GitHub."""
    print("="*60)
    print("Fetching NBA Data from GitHub (2010-2024)")
    print("="*60)
    
    downloaded = []
    for name, url in NBA_DATA_SOURCES.items():
        output_path = CACHE_DIR / f"nba_{name}.csv"
        if download_csv(url, output_path):
            downloaded.append(output_path)
    
    # Combine all parts if multiple were downloaded
    if len(downloaded) > 1:
        print("\nCombining NBA data files...")
        dfs = []
        for file in downloaded:
            try:
                df = pd.read_csv(file)
                dfs.append(df)
                print(f"Loaded {len(df)} rows from {file.name}")
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            output_file = CACHE_DIR / "nba_historical_full.csv"
            combined.to_csv(output_file, index=False)
            print(f"Saved {len(combined)} total NBA games to {output_file}")
            return combined
    
    return None

def fetch_mlb_data():
    """Fetch MLB historical data using pybaseball."""
    print("="*60)
    print("Fetching MLB Data (pybaseball)")
    print("="*60)
    
    try:
        import pybaseball as pyball
        
        # Use statcast to fetch game data
        print("Fetching MLB game data using statcast...")
        start_date = datetime(2023, 1, 1)
        end_date = datetime.now()
        
        # Fetch game-level data
        mlb_data = pyball.statcast(start_dt=start_date.strftime('%Y-%m-%d'), end_dt=end_date.strftime('%Y-%m-%d'))
        
        if not mlb_data.empty:
            output_file = CACHE_DIR / "mlb_historical_full.csv"
            mlb_data.to_csv(output_file, index=False)
            print(f"Saved {len(mlb_data)} MLB records to {output_file}")
            return mlb_data
        else:
            print("No MLB data fetched")
            return None
            
    except ImportError:
        print("pybaseball not installed. Install with: pip install pybaseball")
        return None
    except Exception as e:
        print(f"Error fetching MLB data: {e}")
        return None

def main():
    """Fetch all free data."""
    print("="*60)
    print("Free Sports Data Fetcher")
    print("="*60)
    
    # Fetch NBA data
    nba_df = fetch_nba_data()
    
    # Fetch MLB data
    mlb_df = fetch_mlb_data()
    
    print("\n" + "="*60)
    print("Data Fetch Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
