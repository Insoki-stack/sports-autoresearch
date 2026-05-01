"""
test_sportsdb_explore.py - Explore TheSportsDB endpoints for all sports
"""

import requests

def test_all_sports():
    """Test all sports endpoints"""
    base_url = "https://www.thesportsdb.com/api/v1/json/3"
    
    endpoints = [
        "all_leagues.php",
        "all_sports.php",
        "search_all_teams.php?s=Basketball",
        "search_all_teams.php?s=Ice_Hockey",
        "search_all_teams.php?s=Soccer",
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}/{endpoint}"
        try:
            response = requests.get(url)
            print(f"\n{endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if 'leagues' in data:
                    print(f"  Found {len(data['leagues'])} leagues")
                elif 'sports' in data:
                    print(f"  Found {len(data['sports'])} sports")
                    for sport in data['sports'][:10]:
                        print(f"    - {sport.get('strSport')}")
                elif 'teams' in data:
                    print(f"  Found {len(data['teams'])} teams")
                    for team in data['teams'][:5]:
                        print(f"    - {team.get('strTeam')}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    print("Exploring TheSportsDB...")
    test_all_sports()
