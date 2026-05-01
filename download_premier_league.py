"""
download_premier_league.py - Download Premier League data from datahub.io
"""

import requests
import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def download_premier_league():
    """Download Premier League data from datahub.io"""
    # Try to get the CSV directly
    url = "https://datahub.io/core/english-premier-league/r/season-2223.csv"
    
    try:
        print("Downloading Premier League 2022-23 data...")
        response = requests.get(url)
        
        if response.status_code == 200:
            output_file = CACHE_DIR / "soccer_premier_2223.csv"
            
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"Saved to {output_file}")
            
            df = pd.read_csv(output_file)
            print(f"Total rows: {len(df)}")
            print(f"Columns: {list(df.columns)}")
            print(df.head())
            return df
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def download_premier_league_2324():
    """Download Premier League 2023-24 data"""
    url = "https://datahub.io/core/english-premier-league/r/season-2324.csv"
    
    try:
        print("\nDownloading Premier League 2023-24 data...")
        response = requests.get(url)
        
        if response.status_code == 200:
            output_file = CACHE_DIR / "soccer_premier_2324.csv"
            
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"Saved to {output_file}")
            
            df = pd.read_csv(output_file)
            print(f"Total rows: {len(df)}")
            print(df.head())
            return df
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    download_premier_league()
    download_premier_league_2324()
