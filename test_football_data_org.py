"""
test_football_data_org.py - Test football-data.org for historical soccer data
"""

import requests

def test_football_data():
    """Test football-data.org API"""
    # Try without auth first to see if it's free
    url = "https://api.football-data.org/v4/competitions/PL/matches"
    headers = {}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

def test_premier_league_2022():
    """Try to get 2022 Premier League data"""
    url = "https://api.football-data.org/v4/competitions/PL/matches?season=2022"
    headers = {}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\n2022 Status: {response.status_code}")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing football-data.org...")
    test_football_data()
    test_premier_league_2022()
