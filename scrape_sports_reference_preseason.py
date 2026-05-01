"""
scrape_sports_reference_preseason.py - Scrape preseason championship odds from Sports Reference
"""

import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def scrape_preseason_odds(year: int):
    """Scrape preseason championship odds from Sports Reference."""
    print("="*60)
    print(f"Scraping Preseason Odds from Sports Reference ({year})")
    print("="*60)
    
    try:
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_preseason_odds.html"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            odds_data = []
            
            # Look for tables with odds data
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 3:
                        odds_data.append({
                            'team': cols[0].get_text(strip=True) if cols[0] else '',
                            'odds': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                            'wins_over_under': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'season': year,
                            'source': 'sports_reference_preseason',
                            'date_scraped': datetime.now().strftime('%Y-%m-%d')
                        })
            
            if odds_data:
                df = pd.DataFrame(odds_data)
                output_file = CACHE_DIR / f"nba_preseason_odds_{year}.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} odds records to {output_file}")
                print(f"Columns: {list(df.columns)}")
                return df
            else:
                print("No odds data extracted")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Scrape preseason odds for multiple seasons."""
    for year in [2024, 2023, 2022, 2021]:
        scrape_preseason_odds(year)
    
    print("\n" + "="*60)
    print("Preseason Odds Scraping Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
