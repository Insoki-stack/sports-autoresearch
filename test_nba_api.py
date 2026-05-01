"""
test_nba_api.py - Test nba_api Python library for historical NBA data
"""

import sys

try:
    import nba_api
    from nba_api.stats.static import teams
    from nba_api.stats.endpoints import leaguegamefinder
    import pandas as pd
    from pathlib import Path
    
    CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
    
    print("Testing nba_api...")
    print(f"nba_api version: {nba_api.__version__}")
    
    # Get all NBA teams
    nba_teams = teams.get_teams()
    print(f"Found {len(nba_teams)} NBA teams")
    
    # Get games for a team (e.g., Lakers)
    lakers = [team for team in nba_teams if team['full_name'] == 'Los Angeles Lakers'][0]
    print(f"Testing with {lakers['full_name']}")
    
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=lakers['id'])
    games = gamefinder.get_data_frames()[0]
    print(f"Found {len(games)} games for Lakers")
    print(games.head())
    print(f"Date range: {games['GAME_DATE'].min()} to {games['GAME_DATE'].max()}")
    
    # Save to CSV
    output_file = CACHE_DIR / "nba_nbaapi_sample.csv"
    games.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")
    
except ImportError as e:
    print(f"nba_api not installed: {e}")
    print("Installing nba_api...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nba_api"])
    print("Installed. Please run script again.")
except Exception as e:
    print(f"Error: {e}")
