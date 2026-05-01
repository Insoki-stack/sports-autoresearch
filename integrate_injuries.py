"""
integrate_injuries.py - Integrate injury data with NBA features
Adds injury count per team as a feature.
"""

import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

def integrate_injuries():
    """Integrate injury data with NBA features."""
    print("="*60)
    print("Integrating Injury Data with NBA Features")
    print("="*60)
    
    # Load injury data
    injury_file = CACHE_DIR / "nba_injuries_cbs.csv"
    if not injury_file.exists():
        print("No injury data found")
        return None
    
    injuries_df = pd.read_csv(injury_file)
    print(f"Loaded {len(injuries_df)} injury records")
    
    # Load NBA features
    features_file = CACHE_DIR / "nba_features.csv"
    if not features_file.exists():
        print("No NBA features found")
        return None
    
    features_df = pd.read_csv(features_file)
    print(f"Loaded {len(features_df)} feature records")
    
    # Count injuries per team
    injuries_df['team_clean'] = injuries_df['team'].str.extract(r'([A-Z]{2,3})')
    injury_counts = injuries_df.groupby('team_clean').size().reset_index(name='injury_count')
    
    # Map team abbreviations to full team names
    team_mapping = {
        'LAL': 'Los Angeles Lakers',
        'BOS': 'Boston Celtics',
        'GSW': 'Golden State Warriors',
        'MIA': 'Miami Heat',
        'BKN': 'Brooklyn Nets',
        'NYK': 'New York Knicks',
        'MIL': 'Milwaukee Bucks',
        'PHI': 'Philadelphia 76ers',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        # Add more mappings as needed
    }
    
    injury_counts['team_full'] = injury_counts['team_clean'].map(team_mapping)
    
    # Merge with features
    if 'teamName' in features_df.columns:
        # Try to match by full team name
        features_df = features_df.merge(injury_counts[['team_full', 'injury_count']], 
                                       left_on='teamName', right_on='team_full', how='left')
        features_df['injury_count'] = features_df['injury_count'].fillna(0)
        features_df = features_df.drop(columns=['team_full'], errors='ignore')
    else:
        print("teamName column not found in features")
        return None
    
    # Save integrated features
    output_file = CACHE_DIR / "nba_features_with_injuries.csv"
    features_df.to_csv(output_file, index=False)
    print(f"Saved {len(features_df)} records with injury features to {output_file}")
    print(f"Features: {list(features_df.columns)}")
    
    return features_df

def main():
    """Integrate injury data."""
    integrated_df = integrate_injuries()
    
    if integrated_df is not None:
        print("\n" + "="*60)
        print("Injury Integration Complete!")
        print("="*60)

if __name__ == "__main__":
    main()
