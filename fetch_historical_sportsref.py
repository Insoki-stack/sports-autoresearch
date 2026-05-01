"""
fetch_historical_sportsref.py - Fetch historical sports data using sportsreference library
Uses official Python library for Sports Reference data
"""

from sportsreference.nba.schedule import Schedule
from sportsreference.nhl.schedule import Schedule as NHLSchedule
from sportsreference.mlb.schedule import Schedule as MLBSchedule
import pandas as pd
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_nba_season(year):
    """Fetch NBA games for a specific season."""
    print(f"Fetching NBA {year} season...")
    try:
        schedule = Schedule(year)
        games_data = []
        
        for game in schedule:
            games_data.append({
                'date': game.datetime,
                'away_team': game.away_name,
                'home_team': game.home_name,
                'away_score': game.away_score,
                'home_score': game.home_score,
                'winner': game.winner,
                'attendance': game.attendance,
                'season': year
            })
        
        df = pd.DataFrame(games_data)
        print(f"Fetched {len(df)} NBA games for {year}")
        return df
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return None

def fetch_nhl_season(year):
    """Fetch NHL games for a specific season."""
    print(f"Fetching NHL {year} season...")
    try:
        schedule = NHLSchedule(year)
        games_data = []
        
        for game in schedule:
            games_data.append({
                'date': game.datetime,
                'away_team': game.away_name,
                'home_team': game.home_name,
                'away_score': game.away_score,
                'home_score': game.home_score,
                'winner': game.winner,
                'season': year
            })
        
        df = pd.DataFrame(games_data)
        print(f"Fetched {len(df)} NHL games for {year}")
        return df
    except Exception as e:
        print(f"Error fetching NHL data: {e}")
        return None

def fetch_mlb_season(year):
    """Fetch MLB games for a specific season."""
    print(f"Fetching MLB {year} season...")
    try:
        schedule = MLBSchedule(year)
        games_data = []
        
        for game in schedule:
            games_data.append({
                'date': game.datetime,
                'away_team': game.away_name,
                'home_team': game.home_name,
                'away_score': game.away_score,
                'home_score': game.home_score,
                'winner': game.winner,
                'season': year
            })
        
        df = pd.DataFrame(games_data)
        print(f"Fetched {len(df)} MLB games for {year}")
        return df
    except Exception as e:
        print(f"Error fetching MLB data: {e}")
        return None

def save_sport_data(sport, df):
    """Save historical data to CSV."""
    if df is None or df.empty:
        return
    
    output_file = CACHE_DIR / f"{sport}_historical_sportsref.csv"
    
    if output_file.exists():
        existing_df = pd.read_csv(output_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} {sport} matches to {output_file}")

def main():
    print("Fetching historical sports data from Sports Reference...")
    
    # Fetch data for multiple seasons
    seasons = [2022, 2023, 2024]
    
    for season in seasons:
        print(f"\n=== Season {season} ===")
        
        # NBA
        nba_df = fetch_nba_season(season)
        if nba_df is not None:
            save_sport_data("nba", nba_df)
        
        # NHL
        nhl_df = fetch_nhl_season(season)
        if nhl_df is not None:
            save_sport_data("nhl", nhl_df)
        
        # MLB
        mlb_df = fetch_mlb_season(season)
        if mlb_df is not None:
            save_sport_data("mlb", mlb_df)

if __name__ == "__main__":
    main()
