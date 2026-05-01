"""
scrape_injuries.py - Scrape NBA injury data from ESPN/CBS Sports
Web scraping for free injury data without API keys.
"""

import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def scrape_espn_injuries():
    """Scrape NBA injury data from ESPN."""
    print("="*60)
    print("Scraping NBA Injury Data from ESPN")
    print("="*60)
    
    try:
        url = "https://www.espn.com/nba/injuries"
        print(f"Scraping {url}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse injury table
        injuries = []
        
        # ESPN injury data is in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header
                cols = row.find_all('td')
                if len(cols) >= 3:
                    injury_data = {
                        'player': cols[0].get_text(strip=True) if cols[0] else '',
                        'team': cols[1].get_text(strip=True) if cols[1] else '',
                        'status': cols[2].get_text(strip=True) if cols[2] else '',
                        'description': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                        'date_scraped': datetime.now().strftime('%Y-%m-%d')
                    }
                    if injury_data['player']:
                        injuries.append(injury_data)
        
        if injuries:
            df = pd.DataFrame(injuries)
            output_file = CACHE_DIR / "nba_injuries.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved {len(df)} injury records to {output_file}")
            return df
        else:
            print("No injuries found in page")
            return None
            
    except Exception as e:
        print(f"Error scraping ESPN: {e}")
        return None

def scrape_cbs_injuries():
    """Scrape NBA injury data from CBS Sports."""
    print("="*60)
    print("Scraping NBA Injury Data from CBS Sports")
    print("="*60)
    
    try:
        url = "https://www.cbssports.com/nba/injuries/"
        print(f"Scraping {url}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        injuries = []
        
        # CBS injury data structure
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                injury_data = {
                    'player': cols[0].get_text(strip=True) if cols[0] else '',
                    'team': cols[1].get_text(strip=True) if cols[1] else '',
                    'position': cols[2].get_text(strip=True) if cols[2] else '',
                    'status': cols[3].get_text(strip=True) if cols[3] else '',
                    'date_scraped': datetime.now().strftime('%Y-%m-%d')
                }
                if injury_data['player'] and injury_data['status'] not in ['-', '']:
                    injuries.append(injury_data)
        
        if injuries:
            df = pd.DataFrame(injuries)
            output_file = CACHE_DIR / "nba_injuries_cbs.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved {len(df)} injury records to {output_file}")
            return df
        else:
            print("No injuries found in page")
            return None
            
    except Exception as e:
        print(f"Error scraping CBS: {e}")
        return None

def main():
    """Scrape injury data from multiple sources."""
    espn_injuries = scrape_espn_injuries()
    cbs_injuries = scrape_cbs_injuries()
    
    print("\n" + "="*60)
    print("Injury Scraping Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
