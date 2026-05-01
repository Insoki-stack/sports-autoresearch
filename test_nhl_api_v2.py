"""
test_nhl_api_v2.py - Test NHL official API with correct endpoints
"""

import requests
import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def test_nhl_stats():
    """Test NHL stats endpoint"""
    url = "https://api.nhle.com/stats/rest/en/team/summary?isAggregate=true&isGame=false&sort=%5B%7B%22property%22%3A%22points%22%2C%22direction%22%3A%22DESC%22%7D%5D&factCayenneExp=gamesPlayed%3E%3D1&cayenneExp=gameTypeId%3D2%20and%20seasonId%3C%3D20232024%20and%20seasonId%3E%3D20222024"
    
    try:
        print("Testing NHL team stats API...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Data type: {type(data)}")
            if isinstance(data, list):
                print(f"Found {len(data)} teams")
                if data:
                    print(f"Sample: {str(data[0])[:500]}")
            else:
                print(f"Sample: {str(data)[:500]}")
            return data
        else:
            print(f"Error: {response.text[:500]}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_nhl_standings():
    """Test NHL standings endpoint"""
    url = "https://api.nhle.com/stats/rest/en/standings?season=20232024"
    
    try:
        print("\nTesting NHL standings API...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Data type: {type(data)}")
            if isinstance(data, list):
                print(f"Found {len(data)} teams")
                if data:
                    print(f"Sample: {str(data[0])[:500]}")
            else:
                print(f"Sample: {str(data)[:500]}")
            return data
        else:
            print(f"Error: {response.text[:500]}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    test_nhl_stats()
    test_nhl_standings()
