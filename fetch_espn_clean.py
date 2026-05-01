"""
fetch_espn_clean.py - Fetch historical sports data from ESPN API
No authentication required - processes data directly
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
            
            processed_games = []
            for event in events:
                try:
                    competitions = event.get('competitions', [])
                    if competitions:
                        comp = competitions[0]
                        competitors = comp.get('competitors', [])
                        
                        if len(competitors) >= 2:
                            home = competitors[0]
                            away = competitors[1]
                            
                            game_data = {
                                'date': event.get('date', ''),
                                'season': season,
                                'home_team': home.get('team', {}).get('displayName', ''),
                                'away_team': away.get('team', {}).get('displayName', ''),
                                'home_score': int(home.get('score', 0)),
                                'away_score': int(away.get('score', 0)),
                                'winner': 1 if int(home.get('score', 0)) > int(away.get('score', 0)) else 0
                            }
                            processed_games.append(game_data)
                except Exception:
                    continue
            
            print(f"Fetched {len(processed_games)} NBA games for {season}")
            return processed_games
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
            
            processed_games = []
            for event in events:
                try:
                    competitions = event.get('competitions', [])
                    if competitions:
                        comp = competitions[0]
                        competitors = comp.get('competitors', [])
                        
                        if len(competitors) >= 2:
                            home = competitors[0]
                            away = competitors[1]
                            
                            game_data = {
                                'date': event.get('date', ''),
                                'season': season,
                                'home_team': home.get('team', {}).get('displayName', ''),
                                'away_team': away.get('team', {}).get('displayName', ''),
                                'home_score': int(home.get('score', 0)),
                                'away_score': int(away.get('score', 0)),
                                'winner': 1 if int(home.get('score', 0)) > int(away.get('score', 0)) else 0
                            }
                            processed_games.append(game_data)
                except Exception:
                    continue
            
            print(f"Fetched {len(processed_games)} NHL games for {season}")
            return processed_games
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
            
            processed_games = []
            for event in events:
                try:
                    competitions = event.get('competitions', [])
                    if competitions:
                        comp = competitions[0]
                        competitors = comp.get('competitors', [])
                        
                        if len(competitors) >= 2:
                            home = competitors[0]
                            away = competitors[1]
                            
                            game_data = {
                                'date': event.get('date', ''),
                                'season': season,
                                'home_team': home.get('team', {}).get('displayName', ''),
                                'away_team': away.get('team', {}).get('displayName', ''),
                                'home_score': int(home.get('score', 0)),
                                'away_score': int(away.get('score', 0)),
                                'winner': 1 if int(home.get('score', 0)) > int(away.get('score', 0)) else 0
                            }
                            processed_games.append(game_data)
                except Exception:
                    continue
            
            print(f"Fetched {len(processed_games)} MLB games for {season}")
            return processed_games
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
    output_file = CACHE_DIR / f"{sport}_features.csv"
    
    if output_file.exists():
        try:
            existing_df = pd.read_csv(output_file)
            if not existing_df.empty:
                df = pd.concat([existing_df, df], ignore_index=True)
        except Exception:
            # If file is corrupted, just overwrite it
            pass
    
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} {sport} matches to {output_file}")

def main():
    print("Fetching historical sports data from ESPN API (no authentication)...")
    
    seasons = [2024, 2023, 2022]
    
    for season in seasons:
        print(f"\nFetching data for {season}...")
        
        nba_games = fetch_nba_games(season)
        if nba_games:
            save_sport_data("nba", nba_games)
        
        time.sleep(2)
        
        nhl_games = fetch_nhl_games(season)
        if nhl_games:
            save_sport_data("nhl", nhl_games)
        
        time.sleep(2)
        
        mlb_games = fetch_mlb_games(season)
        if mlb_games:
            save_sport_data("mlb", mlb_games)
        
        time.sleep(2)

if __name__ == "__main__":
    main()
