"""
test_api_sports.py - Test API-Sports for NBA/NHL data
"""

import requests
import json

# API-Sports requires an API key - let's try without first to see if they have a free tier
API_KEY = "test"  # Placeholder

def test_nba():
    """Test NBA data from API-Sports"""
    url = "https://v1.basketball.api-sports.io/games"
    headers = {'x-rapidapi-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"NBA Status: {response.status_code}")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

def test_nhl():
    """Test NHL data from API-Sports"""
    url = "https://v1.hockey.api-sports.io/games"
    headers = {'x-rapidapi-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\nNHL Status: {response.status_code}")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing API-Sports...")
    test_nba()
    test_nhl()
