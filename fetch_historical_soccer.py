"""
fetch_historical_soccer.py - Fetch historical soccer data from iSports API
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# iSports API configuration
# Get free API key from: https://api.isportsapi.com (no credit card required)
# Free tier: 200 requests/day
ISPORTS_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
ISPORTS_BASE_URL = "https://api.isportsapi.com/sport/football"

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_historical_matches(year=2024):
    """Fetch historical soccer matches for a specific year."""
    url = f"{ISPORTS_BASE_URL}/matches"
    params = {
        "apikey": ISPORTS_API_KEY,
        "year": year,
        "league_id": 148  # Premier League as example, can expand
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched {len(data.get('data', []))} matches for {year}")
            return data.get('data', [])
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_historical_odds(match_id):
    """Fetch historical odds for a specific match."""
    url = f"{ISPORTS_BASE_URL}/odds"
    params = {
        "apikey": ISPORTS_API_KEY,
        "match_id": match_id
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('data', [])
        return None
    except Exception as e:
        print(f"Error fetching odds: {e}")
        return None

def save_historical_data(matches, odds_data):
    """Save historical data to CSV."""
    df = pd.DataFrame(matches)
    output_file = CACHE_DIR / "soccer_historical_full.csv"
    
    if output_file.exists():
        existing_df = pd.read_csv(output_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} historical soccer matches to {output_file}")

def main():
    print("Fetching historical soccer data from iSports API...")
    
    # Fetch data for multiple years
    all_matches = []
    years = [2022, 2023, 2024]  # Last 3 years
    
    for year in years:
        matches = fetch_historical_matches(year)
        if matches:
            all_matches.extend(matches)
    
    # Save data
    if all_matches:
        save_historical_data(all_matches, [])
        print(f"Total matches fetched: {len(all_matches)}")
    else:
        print("No matches fetched. Check API key and limits.")

if __name__ == "__main__":
    main()
