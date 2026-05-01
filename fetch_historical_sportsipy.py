"""
fetch_historical_sportsipy.py - Fetch historical sports data using sportsipy library
Uses Sports Reference data via official sportsipy Python library
"""

from sportsipy.nba.schedule import Schedule as NBASchedule
from sportsipy.nhl.schedule import Schedule as NHLSchedule
from sportsipy.mlb.schedule import Schedule as MLBSchedule
import pandas as pd
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_nba_season(year):
    """Fetch NBA games for a specific season."""
    print(f"Fetching NBA {year} season...")
    try:
        schedule = NBASchedule(year)
        games_data = []
        
        for game in schedule.dataframe.itertuples():
            games_data.append({
                'date': getattr(game, 'datetime', ''),
                'away_team': getattr(game, 'away_abbr', ''),
                'home_team': getattr(game, 'home_abbr', ''),
                'away_score': getattr(game, 'away_score', 0),
                'home_score': getattr(game, 'home_score', 0),
                'winner': getattr(game, 'winner', ''),
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
        
        for game in schedule.dataframe.itertuples():
            games_data.append({
                'date': getattr(game, 'datetime', ''),
                'away_team': getattr(game, 'away_abbr', ''),
                'home_team': getattr(game, 'home_abbr', ''),
                'away_score': getattr(game, 'away_score', 0),
                'home_score': getattr(game, 'home_score', 0),
                'winner': getattr(game, 'winner', ''),
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
        
        for game in schedule.dataframe.itertuples():
            games_data.append({
                'date': getattr(game, 'datetime', ''),
                'away_team': getattr(game, 'away_abbr', ''),
                'home_team': getattr(game, 'home_abbr', ''),
                'away_score': getattr(game, 'away_score', 0),
                'home_score': getattr(game, 'home_score', 0),
                'winner': getattr(game, 'winner', ''),
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
    
    output_file = CACHE_DIR / f"{sport}_historical_sportsipy.csv"
    
    if output_file.exists():
        existing_df = pd.read_csv(output_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} {sport} matches to {output_file}")

def main():
    print("Fetching historical sports data from Sports Reference via sportsipy...")
    
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
