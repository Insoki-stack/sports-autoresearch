"""
test_football_data.py - Test football-data.org for soccer data
"""

import requests

def test_football_data():
    """Test football-data.org API"""
    url = "https://api.football-data.org/v4/competitions"
    headers = {'X-Auth-Token': 'test'}  # Placeholder
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Football-data.org Status: {response.status_code}")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing football-data.org...")
    test_football_data()
