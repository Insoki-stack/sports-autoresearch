"""
test_nhl_api.py - Test NHL official API for historical data
"""

import requests
import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def test_nhl_official_api():
    """Test NHL official API"""
    # Test schedule endpoint for 2023-2024 season
    url = "https://api.nhle.com/stats/rest/en/schedule?seasonId=20232024"
    
    try:
        print("Testing NHL official API...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Data keys: {data.keys() if isinstance(data, dict) else type(data)}")
            print(f"Sample: {str(data)[:1000]}")
            return data
        else:
            print(f"Error: {response.text[:500]}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_nhl_games_2023():
    """Fetch NHL games for 2023-2024 season"""
    url = "https://api.nhle.com/stats/rest/en/schedule?seasonId=20232024"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            if 'games' in data:
                games = data['games']
                print(f"Found {len(games)} games")
                
                processed = []
                for game in games:
                    try:
                        processed.append({
                            'date': game.get('gameDate'),
                            'home_team': game.get('homeTeam', {}).get('default', ''),
                            'away_team': game.get('awayTeam', {}).get('default', ''),
                            'home_score': game.get('homeTeam', {}).get('score', 0),
                            'away_score': game.get('awayTeam', {}).get('score', 0),
                            'season': '20232024'
                        })
                    except Exception:
                        continue
                
                if processed:
                    df = pd.DataFrame(processed)
                    output_file = CACHE_DIR / "nhl_official_2023.csv"
                    df.to_csv(output_file, index=False)
                    print(f"Saved {len(df)} games to {output_file}")
                    print(df.head())
                    return df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    test_nhl_official_api()
    fetch_nhl_games_2023()
