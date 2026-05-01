"""
scrape_sports_reference.py - Scrape historical NBA odds from Sports Reference
"""

import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def scrape_sports_reference_nba_odds(year: int = 2024):
    """Scrape NBA odds from Sports Reference for a specific season."""
    print("="*60)
    print(f"Scraping NBA Odds from Sports Reference ({year})")
    print("="*60)
    
    try:
        # Sports Reference NBA odds page - correct URL structure
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games.html"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            odds_data = []
            
            # Sports Reference uses tables with specific IDs
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 4:
                        odds_data.append({
                            'date': cols[0].get_text(strip=True) if cols[0] else '',
                            'team': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'opp': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                            'result': cols[6].get_text(strip=True) if len(cols) > 6 else '',
                            'season': year,
                            'source': 'sports_reference',
                            'date_scraped': datetime.now().strftime('%Y-%m-%d')
                        })
            
            if odds_data:
                df = pd.DataFrame(odds_data)
                output_file = CACHE_DIR / f"nba_odds_sports_reference_{year}.csv"
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
        print(f"Error scraping Sports Reference: {e}")
        return None

def main():
    """Scrape odds from Sports Reference for multiple seasons."""
    print("Scraping multiple seasons...")
    
    for year in [2024, 2023, 2022, 2021]:
        print(f"\nSeason {year}:")
        scrape_sports_reference_nba_odds(year)
    
    print("\n" + "="*60)
    print("Sports Reference Odds Scraping Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
