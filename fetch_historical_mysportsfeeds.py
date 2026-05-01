"""
fetch_historical_mysportsfeeds.py - Fetch historical sports data from MySportsFeeds API
Covers: NFL, MLB, NBA, NHL with free tier
"""

import requests
import pandas as pd
from pathlib import Path
import time

# MySportsFeeds API configuration
# Get free API key from: https://www.mysportsfeeds.com/login1/
# Free tier available for personal/private use
MSF_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
MSF_API_VERSION = "v3.1"
MSF_BASE_URL = f"https://api.mysportsfeeds.com/{MSF_API_VERSION}"

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_nba_games(season="2024-regular"):
    """Fetch NBA games for a specific season."""
    url = f"{MSF_BASE_URL}/pull/nba/{season}/games.json"
    headers = {"Authorization": f"Bearer {MSF_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            games = data.get('games', [])
            print(f"Fetched {len(games)} NBA games for {season}")
            return games
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return None

def fetch_nhl_games(season="2024-regular"):
    """Fetch NHL games for a specific season."""
    url = f"{MSF_BASE_URL}/pull/nhl/{season}/games.json"
    headers = {"Authorization": f"Bearer {MSF_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            games = data.get('games', [])
            print(f"Fetched {len(games)} NHL games for {season}")
            return games
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching NHL data: {e}")
        return None

def fetch_mlb_games(season="2024-regular"):
    """Fetch MLB games for a specific season."""
    url = f"{MSF_BASE_URL}/pull/mlb/{season}/games.json"
    headers = {"Authorization": f"Bearer {MSF_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            games = data.get('games', [])
            print(f"Fetched {len(games)} MLB games for {season}")
            return games
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching MLB data: {e}")
        return None

def save_sport_data(sport, games):
    """Save historical data to CSV."""
    if not games:
        return
    
    df = pd.DataFrame(games)
    output_file = CACHE_DIR / f"{sport}_historical_msf.csv"
    
    if output_file.exists():
        existing_df = pd.read_csv(output_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} {sport} matches to {output_file}")

def main():
    print("Fetching historical sports data from MySportsFeeds API...")
    
    # Fetch data for multiple seasons
    seasons = ["2024-regular", "2023-regular", "2022-regular"]
    
    for season in seasons:
        print(f"\nFetching data for {season}...")
        
        # NBA
        nba_games = fetch_nba_games(season)
        if nba_games:
            save_sport_data("nba", nba_games)
        
        time.sleep(3)
        
        # NHL
        nhl_games = fetch_nhl_games(season)
        if nhl_games:
            save_sport_data("nhl", nhl_games)
        
        time.sleep(3)
        
        # MLB
        mlb_games = fetch_mlb_games(season)
        if mlb_games:
            save_sport_data("mlb", mlb_games)
        
        time.sleep(3)

if __name__ == "__main__":
    main()
