"""
test_sportsdb_matches.py - Explore TheSportsDB for historical match data
"""

import requests

def test_event_last():
    """Test last events endpoint"""
    base_url = "https://www.thesportsdb.com/api/v1/json/3"
    
    # Try to get last events for basketball
    url = f"{base_url}/eventspastleague.php?id=4387"  # NBA league ID
    try:
        response = requests.get(url)
        print(f"NBA Past Events: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Results: {str(data)[:500]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Try soccer
    url = f"{base_url}/eventspastleague.php?id=4328"  # Premier League
    try:
        response = requests.get(url)
        print(f"\nPremier League Past Events: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Results: {str(data)[:500]}")
    except Exception as e:
        print(f"Error: {e}")

def test_search_league():
    """Search for specific leagues"""
    base_url = "https://www.thesportsdb.com/api/v1/json/3"
    
    # Search for NBA
    url = f"{base_url}/search_all_leagues.php?l=NBA"
    try:
        response = requests.get(url)
        print(f"\nSearch NBA: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Results: {str(data)[:800]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing TheSportsDB match data...")
    test_event_last()
    test_search_league()
