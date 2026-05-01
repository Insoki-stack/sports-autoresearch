"""
fetch_sbr_odds.py - Fetch historical odds from SBR (Sportsbook Review)
Based on the approach used in the GitHub NBA betting repo.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_sbr_nba_odds():
    """Fetch NBA odds from SBR (Sportsbook Review)."""
    print("="*60)
    print("Fetching NBA Odds from SBR")
    print("="*60)
    
    try:
        # SBR provides odds for various sportsbooks
        # This is a simplified approach - in production you'd need to scrape their pages
        url = "https://www.sportsbookreview.com/nba/odds/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Fetching from {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Parse the page to extract odds
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # SBR odds are in tables - this is a simplified extraction
            odds_data = []
            
            # Look for odds tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        odds_data.append({
                            'team': cols[0].get_text(strip=True) if cols[0] else '',
                            'bookmaker': 'SBR',
                            'moneyline': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                            'spread': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'total': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                            'date_fetched': datetime.now().strftime('%Y-%m-%d')
                        })
            
            if odds_data:
                df = pd.DataFrame(odds_data)
                output_file = CACHE_DIR / "nba_sbr_odds.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} odds records to {output_file}")
                return df
            else:
                print("No odds data extracted from page")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error fetching SBR odds: {e}")
        return None

def main():
    """Fetch odds from SBR."""
    odds_df = fetch_sbr_nba_odds()
    
    if odds_df is not None:
        print("\n" + "="*60)
        print("SBR Odds Fetch Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
