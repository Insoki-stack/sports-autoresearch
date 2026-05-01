"""
scrape_espn_odds.py - Scrape historical NBA odds from ESPN
"""

import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def scrape_espn_nba_odds():
    """Scrape NBA odds from ESPN."""
    print("="*60)
    print("Scraping NBA Odds from ESPN")
    print("="*60)
    
    try:
        # ESPN NBA odds page
        url = "https://www.espn.com/nba/odds"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            odds_data = []
            
            # ESPN uses specific classes for odds data
            # This will need adjustment based on actual page structure
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        odds_data.append({
                            'date': cols[0].get_text(strip=True) if cols[0] else '',
                            'team': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                            'spread': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'moneyline': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                            'source': 'espn',
                            'date_scraped': datetime.now().strftime('%Y-%m-%d')
                        })
            
            if odds_data:
                df = pd.DataFrame(odds_data)
                output_file = CACHE_DIR / "nba_odds_espn.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} odds records to {output_file}")
                return df
            else:
                print("No odds data extracted - page structure may have changed")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error scraping ESPN: {e}")
        return None

def main():
    """Scrape odds from ESPN."""
    odds_df = scrape_espn_nba_odds()
    
    if odds_df is not None:
        print("\n" + "="*60)
        print("ESPN Odds Scraping Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
