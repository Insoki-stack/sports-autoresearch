"""
fetch_nhl_official.py - Fetch NHL game data from official API
"""

import requests
import pandas as pd
from pathlib import Path
import time

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def fetch_nhl_games_by_season(season_id):
    """Fetch NHL games for a specific season"""
    url = f"https://api.nhle.com/stats/rest/en/game?seasonId={season_id}&gameTypeId=2"
    
    try:
        print(f"Fetching NHL games for {season_id}...")
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data:
                games = data['data']
                print(f"Found {len(games)} games")
                
                processed = []
                for game in games:
                    try:
                        # Filter for recent seasons only
                        game_date = game.get('gameDate', '')
                        if game_date.startswith('2022') or game_date.startswith('2023') or game_date.startswith('2024'):
                            processed.append({
                                'game_id': game.get('id'),
                                'date': game.get('gameDate'),
                                'season': season_id,
                                'home_team_id': game.get('homeTeamId'),
                                'away_team_id': game.get('awayTeamId'),
                                'home_score': game.get('homeScore', 0),
                                'away_score': game.get('visitingScore', 0),
                                'winner': 1 if game.get('homeScore', 0) > game.get('visitingScore', 0) else 0
                            })
                    except Exception:
                        continue
                
                if processed:
                    df = pd.DataFrame(processed)
                    output_file = CACHE_DIR / f"nhl_official_{season_id}.csv"
                    df.to_csv(output_file, index=False)
                    print(f"Saved {len(df)} games to {output_file}")
                    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
                    return df
                else:
                    print("No games from 2022-2024 found")
                    return None
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def main():
    """Fetch NHL data for 2022-2024 seasons"""
    seasons = ["20242025", "20232024", "20222023"]
    
    all_games = []
    for season in seasons:
        df = fetch_nhl_games_by_season(season)
        if df is not None:
            all_games.append(df)
        time.sleep(1)
    
    if all_games:
        combined_df = pd.concat(all_games, ignore_index=True)
        output_file = CACHE_DIR / "nhl_features.csv"
        combined_df.to_csv(output_file, index=False)
        print(f"\nSaved {len(combined_df)} total NHL games to {output_file}")
        return combined_df

if __name__ == "__main__":
    main()
