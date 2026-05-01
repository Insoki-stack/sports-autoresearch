"""
test_sportsdb_seasons.py - Explore TheSportsDB for historical seasons
"""

import requests
from pathlib import Path
import pandas as pd

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def fetch_nba_events():
    """Fetch NBA past events"""
    base_url = "https://www.thesportsdb.com/api/v1/json/3"
    url = f"{base_url}/eventspastleague.php?id=4387"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"Fetched {len(events)} NBA events")
            
            # Process events
            processed = []
            for event in events:
                try:
                    processed.append({
                        'id': event.get('idEvent'),
                        'date': event.get('strTimestamp'),
                        'event': event.get('strEvent'),
                        'home_team': event.get('strHomeTeam'),
                        'away_team': event.get('strAwayTeam'),
                        'home_score': int(event.get('intHomeScore', 0)),
                        'away_score': int(event.get('intAwayScore', 0)),
                        'season': event.get('strSeason'),
                        'league': event.get('strLeague')
                    })
                except Exception:
                    continue
            
            if processed:
                df = pd.DataFrame(processed)
                output_file = CACHE_DIR / "nba_sportsdb.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} NBA events to {output_file}")
                print(f"Date range: {df['date'].min()} to {df['date'].max()}")
                print(df.head())
                return df
    except Exception as e:
        print(f"Error: {e}")

def fetch_soccer_events():
    """Fetch Premier League past events"""
    base_url = "https://www.thesportsdb.com/api/v1/json/3"
    url = f"{base_url}/eventspastleague.php?id=4328"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"\nFetched {len(events)} Premier League events")
            
            processed = []
            for event in events:
                try:
                    processed.append({
                        'id': event.get('idEvent'),
                        'date': event.get('strTimestamp'),
                        'event': event.get('strEvent'),
                        'home_team': event.get('strHomeTeam'),
                        'away_team': event.get('strAwayTeam'),
                        'home_score': int(event.get('intHomeScore', 0)),
                        'away_score': int(event.get('intAwayScore', 0)),
                        'season': event.get('strSeason'),
                        'league': event.get('strLeague')
                    })
                except Exception:
                    continue
            
            if processed:
                df = pd.DataFrame(processed)
                output_file = CACHE_DIR / "soccer_sportsdb.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} soccer events to {output_file}")
                print(f"Date range: {df['date'].min()} to {df['date'].max()}")
                print(df.head())
                return df
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Fetching historical data from TheSportsDB...")
    fetch_nba_events()
    fetch_soccer_events()
