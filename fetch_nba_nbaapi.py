"""
fetch_nba_nbaapi.py - Fetch historical NBA data using nba_api
"""

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
from pathlib import Path
import time

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def fetch_all_nba_games():
    """Fetch historical games for all NBA teams"""
    # Get all NBA teams
    nba_teams = teams.get_teams()
    print(f"Found {len(nba_teams)} NBA teams")
    
    all_games = []
    
    for team in nba_teams:
        try:
            print(f"Fetching games for {team['full_name']}...")
            
            # Get games for this team
            gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team['id'])
            games = gamefinder.get_data_frames()[0]
            
            # Filter for 2022-2024 seasons (seasons are in format 22022, 22023, 22024)
            games['SEASON_ID'] = games['SEASON_ID'].astype(str)
            games = games[games['SEASON_ID'].str.startswith('2')]
            
            all_games.append(games)
            
            # Rate limiting
            time.sleep(0.6)
            
        except Exception as e:
            print(f"Error fetching {team['full_name']}: {e}")
            continue
    
    if all_games:
        combined_df = pd.concat(all_games, ignore_index=True)
        output_file = CACHE_DIR / "nba_historical_nbaapi.csv"
        combined_df.to_csv(output_file, index=False)
        print(f"\nSaved {len(combined_df)} total games to {output_file}")
        print(f"Date range: {combined_df['GAME_DATE'].min()} to {combined_df['GAME_DATE'].max()}")
        print(f"Seasons: {combined_df['SEASON_ID'].unique()}")
        return combined_df
    else:
        print("No games fetched")
        return None

if __name__ == "__main__":
    fetch_all_nba_games()
