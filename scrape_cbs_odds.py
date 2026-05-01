"""
scrape_cbs_odds.py - Scrape historical NBA odds from CBS Sports
"""

import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def scrape_cbs_nba_odds():
    """Scrape NBA odds from CBS Sports."""
    print("="*60)
    print("Scraping NBA Odds from CBS Sports")
    print("="*60)
    
    try:
        url = "https://www.cbssports.com/nba/odds/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            odds_data = []
            
            # CBS Sports odds structure - look for odds tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 5:
                        odds_data.append({
                            'date': cols[0].get_text(strip=True) if cols[0] else '',
                            'team': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                            'spread': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'moneyline': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                            'total': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                            'source': 'cbs_sports',
                            'date_scraped': datetime.now().strftime('%Y-%m-%d')
                        })
            
            if odds_data:
                df = pd.DataFrame(odds_data)
                output_file = CACHE_DIR / "nba_odds_cbs.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} odds records to {output_file}")
                print(f"Columns: {list(df.columns)}")
                return df
            else:
                print("No odds data extracted - may need to inspect page structure")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error scraping CBS Sports: {e}")
        return None

def main():
    """Scrape odds from CBS Sports."""
    odds_df = scrape_cbs_nba_odds()
    
    if odds_df is not None:
        print("\n" + "="*60)
        print("CBS Sports Odds Scraping Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
