"""
fetch_historical_balldontlie.py - Fetch historical sports data from BALLDONTLIE API
Covers: NBA, NFL, MLB, NHL, Soccer, Tennis, Golf, 20+ leagues
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# BALLDONTLIE API configuration
BDL_API_KEY = "52345b0b-d723-4ee4-a137-8da2f92e3cdc"
BDL_BASE_URL = "https://api.balldontlie.io"

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_nba_games(season=2024):
    """Fetch historical NBA games."""
    url = f"{BDL_BASE_URL}/nba/v1/games"
    headers = {"Authorization": f"Bearer {BDL_API_KEY}"}
    params = {
        "season": season,
        "per_page": 100
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            games = data.get('data', [])
            print(f"Fetched {len(games)} NBA games for {season}")
            return games
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return None

def fetch_nhl_games(season=2024):
    """Fetch historical NHL games."""
    url = f"{BDL_BASE_URL}/nhl/v1/games"
    headers = {"Authorization": f"Bearer {BDL_API_KEY}"}
    params = {
        "season": season
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            games = data.get('data', [])
            print(f"Fetched {len(games)} NHL games for {season}")
            return games
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching NHL data: {e}")
        return None

def fetch_soccer_games(league_id=39, season=2024):  # 39 = Premier League
    """Fetch historical soccer games."""
    url = f"{BDL_BASE_URL}/soccer/v1/games"
    headers = {"Authorization": f"Bearer {BDL_API_KEY}"}
    params = {
        "league": league_id,
        "season": season
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            games = data.get('data', [])
            print(f"Fetched {len(games)} Soccer games for {season}")
            return games
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Soccer data: {e}")
        return None

def save_sport_data(sport, games):
    """Save historical data to CSV."""
    if not games:
        return
    
    df = pd.DataFrame(games)
    output_file = CACHE_DIR / f"{sport}_historical_bdl.csv"
    
    if output_file.exists():
        existing_df = pd.read_csv(output_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} {sport} matches to {output_file}")

def main():
    print("Fetching historical sports data from BALLDONTLIE API...")
    
    # Fetch data for multiple seasons
    seasons = [2024, 2023, 2022]
    
    for season in seasons:
        print(f"\nFetching data for {season}...")
        
        # NBA
        nba_games = fetch_nba_games(season)
        if nba_games:
            save_sport_data("nba", nba_games)
        
        # Add delay5to avoid rate limiting
        time.sleep(2)
        
        # NHL
        nhl_games = fetch_nhl_games(season)
        if nhl_games:
            save_sport_data("nhl", nhl_games)
        
        time.sleep(2)
        
        # Soccer
        soccer_games = fetch_soccer_games(season=season)
        if soccer_games:
            save_sport_data("soccer", soccer_games)
        
        time.sleep(2)

if __name__ == "__main__":
    main()
