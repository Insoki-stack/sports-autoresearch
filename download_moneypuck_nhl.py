"""
download_moneypuck_nhl.py - Download free NHL data from MoneyPuck.com
"""

import requests
import pandas as pd
from pathlib import Path
import io

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def download_nhl_game_data():
    """Download NHL game data from MoneyPuck"""
    url = "https://moneypuck.com/moneypuck/playerData/careers/gameByGame/all_teams.csv"
    
    try:
        print("Downloading NHL game data from MoneyPuck...")
        response = requests.get(url)
        
        if response.status_code == 200:
            output_file = CACHE_DIR / "nhl_moneypuck_games.csv"
            
            # Try different encodings
            content = response.content
            
            # Try to decode as utf-8 first
            try:
                text = content.decode('utf-8')
                df = pd.read_csv(io.StringIO(text))
            except:
                # Try latin-1
                try:
                    text = content.decode('latin-1')
                    df = pd.read_csv(io.StringIO(text))
                except:
                    # Try with error handling
                    text = content.decode('utf-8', errors='ignore')
                    df = pd.read_csv(io.StringIO(text))
            
            df.to_csv(output_file, index=False)
            print(f"Saved NHL game data to {output_file}")
            print(f"Total rows: {len(df)}")
            print(f"Columns: {list(df.columns[:20])}")
            
            if 'season' in df.columns:
                print(f"Seasons: {sorted(df['season'].unique())}")
            
            print(df.head())
            return df
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading NHL data: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    download_nhl_game_data()
