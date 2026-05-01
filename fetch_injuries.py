"""
fetch_injuries.py - Fetch NBA injury data using BALLDONTLIE API
Gets injury reports using the existing API key.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

BALLDONTLIE_API_KEY = "52345b0b-d723-4ee4-a137-8da2f92e3cdc"

def fetch_nba_injuries():
    """Fetch NBA injury data using BALLDONTLIE API."""
    print("="*60)
    print("Fetching NBA Injury Data (BALLDONTLIE API)")
    print("="*60)
    
    try:
        headers = {"Authorization": BALLDONTLIE_API_KEY}
        
        # Fetch injuries for current season
        url = "https://api.balldontlie.io/nba/v1/injuries"
        print(f"Fetching injuries from {url}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data:
                injuries = data["data"]
                
                if injuries:
                    df = pd.DataFrame(injuries)
                    output_file = CACHE_DIR / "nba_injuries.csv"
                    df.to_csv(output_file, index=False)
                    print(f"Saved {len(df)} injury records to {output_file}")
                    print(f"Columns: {list(df.columns)}")
                    return df
                else:
                    print("No injury data in response")
                    return None
            else:
                print("No 'data' key in response")
                return None
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error fetching injury data: {e}")
        return None

def main():
    """Fetch injury data."""
    injuries_df = fetch_nba_injuries()
    
    if injuries_df is not None:
        print("\n" + "="*60)
        print("Injury Data Fetch Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
