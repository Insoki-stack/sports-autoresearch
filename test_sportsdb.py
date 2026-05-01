"""
test_sportsdb.py - Test TheSportsDB for free sports data
"""

import requests

def test_sportsdb():
    """Test TheSportsDB API"""
    url = "https://www.thesportsdb.com/api/v1/json/3/all_leagues.php"
    
    try:
        response = requests.get(url)
        print(f"TheSportsDB Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('leagues', []))} leagues")
        # Find NBA, NHL, Soccer leagues
        for league in data.get('leagues', [])[:20]:
            print(f"- {league.get('strLeague')}: {league.get('strSport')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing TheSportsDB...")
    test_sportsdb()
