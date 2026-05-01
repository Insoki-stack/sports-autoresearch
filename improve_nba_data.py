"""
improve_nba_data.py - Add team names and advanced features to NBA data
"""

import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

# NBA team ID to name mapping
NBA_TEAMS = {
    1610612737: 'Atlanta Hawks',
    1610612738: 'Boston Celtics',
    1610612739: 'Cleveland Cavaliers',
    1610612740: 'New Orleans Pelicans',
    1610612741: 'Chicago Bulls',
    1610612742: 'Dallas Mavericks',
    1610612743: 'Denver Nuggets',
    1610612744: 'Golden State Warriors',
    1610612745: 'Houston Rockets',
    1610612746: 'Los Angeles Clippers',
    1610612747: 'Los Angeles Lakers',
    1610612748: 'Miami Heat',
    1610612749: 'Milwaukee Bucks',
    1610612750: 'Minnesota Timberwolves',
    1610612751: 'Brooklyn Nets',
    1610612752: 'New York Knicks',
    1610612753: 'Orlando Magic',
    1610612754: 'Indiana Pacers',
    1610612755: 'Philadelphia 76ers',
    1610612756: 'Phoenix Suns',
    1610612757: 'Portland Trail Blazers',
    1610612758: 'Sacramento Kings',
    1610612759: 'San Antonio Spurs',
    1610612760: 'Oklahoma City Thunder',
    1610612761: 'Toronto Raptors',
    1610612762: 'Utah Jazz',
    1610612763: 'Memphis Grizzlies',
    1610612764: 'Washington Wizards',
    1610612765: 'Detroit Pistons',
    1610612766: 'Charlotte Hornets',
}

def improve_nba_data():
    """Add team names and advanced features to NBA data"""
    input_file = CACHE_DIR / "nba_features.csv"
    
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} NBA games")
        print(f"Columns: {list(df.columns)}")
        
        # The data already has home_team and away_team from processing
        # Add advanced features
        df['points_per_game'] = df['points']
        df['assists_per_game'] = df['assists']
        df['rebounds_per_game'] = df['rebounds']
        df['fg_efficiency'] = df['fg_pct'] * 100
        df['three_pt_efficiency'] = df['fg3_pct'] * 100
        df['ft_efficiency'] = df['ft_pct'] * 100
        
        # Calculate rolling averages (window of 10 games)
        df = df.sort_values('date')
        df['rolling_points'] = df['points'].rolling(window=10, min_periods=1).mean()
        df['rolling_assists'] = df['assists'].rolling(window=10, min_periods=1).mean()
        df['rolling_rebounds'] = df['rebounds'].rolling(window=10, min_periods=1).mean()
        
        # Create target (1 if won, 0 if lost)
        df['target'] = df['winner']
        
        output_file = CACHE_DIR / "nba_features.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved improved NBA data to {output_file}")
        print(f"Features: {list(df.columns)}")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    improve_nba_data()
