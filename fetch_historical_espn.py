"""
fetch_historical_espn.py - Fetch historical sports data from ESPN hidden API
No authentication required
"""

import requests
import pandas as pd
from pathlib import Path
import time

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_nba_games(season=2024):
    """Fetch NBA games for a specific season from ESPN."""
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={season}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"Fetched {len(events)} NBA games for {season}")
            return events
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return None

def fetch_nhl_games(season=2024):
    """Fetch NHL games for a specific season from ESPN."""
    url = f"https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard?dates={season}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"Fetched {len(events)} NHL games for {season}")
            return events
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching NHL data: {e}")
        return None

def fetch_mlb_games(season=2024):
    """Fetch MLB games for a specific season from ESPN."""
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={season}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"Fetched {len(events)} MLB games for {season}")
            return events
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
    output_file = CACHE_DIR / f"{sport}_historical_espn.csv"
    
    if output_file.exists():
        existing_df = pd.read_csv(output_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} {sport} matches to {output_file}")

def main():
    print("Fetching historical sports data from ESPN API (no authentication)...")
    
    # Fetch data for multiple seasons
    seasons = [2024, 2023, 2022]
    
    for season in seasons:
        print(f"\nFetching data for {season}...")
        
        # NBA
        nba_games = fetch_nba_games(season)
        if nba_games:
            save_sport_data("nba", nba_games)
        
        time.sleep(2)
        
        # NHL
        nhl_games = fetch_nhl_games(season)
        if nhl_games:
            save_sport_data("nhl", nhl_games)
        
        time.sleep(2)
        
        # MLB
        mlb_games = fetch_mlb_games(season)
        if mlb_games:
            save_sport_data("mlb", mlb_games)
        
        time.sleep(2)
        
        # Soccer
        soccer_games = fetch_soccer_games(season=season)
        if soccer_games:
            save_sport_data("soccer", soccer_games)
        
        time.sleep(2)

if __name__ == "__main__":
    main()
        time.sleep(2)
        
        # NHL
        nhl_games = fetch_nhl_games(season)
        if nhl_games:
            save_sport_data("nhl", nhl_games)
        
        time.sleep(2)
        
        # MLB
        mlb_games = fetch_mlb_games(season)
        if mlb_games:
            save_sport_data("mlb", mlb_games)
        
        time.sleep(2)

if __name__ == "__main__":
    main()
        # NHL
        nhl_games = fetch_nhl_games(season)
        if nhl_games:
            save_sport_data("nhl", nhl_games)
        
        time.sleep(2)
        
        # MLB
        mlb_games = fetch_mlb_games(season)
        if mlb_games:
            save_sport_data("mlb", mlb_games)
        
        time.sleep(2)

if __name__ == "__main__":
    main()
