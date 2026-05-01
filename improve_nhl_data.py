"""
improve_nhl_data.py - Add team names and advanced features to NHL data
"""

import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

# NHL team ID to name mapping
NHL_TEAMS = {
    1: 'New Jersey Devils',
    2: 'New York Islanders',
    3: 'New York Rangers',
    4: 'Philadelphia Flyers',
    5: 'Pittsburgh Penguins',
    6: 'Boston Bruins',
    7: 'Buffalo Sabres',
    8: 'Montreal Canadiens',
    9: 'Ottawa Senators',
    10: 'Toronto Maple Leafs',
    12: 'Carolina Hurricanes',
    13: 'Florida Panthers',
    14: 'Tampa Bay Lightning',
    15: 'Washington Capitals',
    16: 'Chicago Blackhawks',
    17: 'Detroit Red Wings',
    18: 'Nashville Predators',
    19: 'St. Louis Blues',
    20: 'Calgary Flames',
    21: 'Colorado Avalanche',
    22: 'Edmonton Oilers',
    23: 'Vancouver Canucks',
    24: 'Anaheim Ducks',
    25: 'Dallas Stars',
    26: 'Los Angeles Kings',
    28: 'San Jose Sharks',
    29: 'Columbus Blue Jackets',
    30: 'Minnesota Wild',
    52: 'Winnipeg Jets',
    53: 'Arizona Coyotes',
    54: 'Vegas Golden Knights',
    55: 'Seattle Kraken',
}

def improve_nhl_data():
    """Add team names and advanced features to NHL data"""
    input_file = CACHE_DIR / "nhl_features.csv"
    
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} NHL games")
        
        # Add team names from team IDs
        df['home_team_name'] = df['home_team_id'].map(NHL_TEAMS)
        df['away_team_name'] = df['away_team_id'].map(NHL_TEAMS)
        
        # Calculate advanced features
        df['total_goals'] = df['home_score'] + df['away_score']
        df['goal_difference'] = df['home_score'] - df['away_score']
        df['home_win'] = (df['home_score'] > df['away_score']).astype(int)
        
        # Sort by date for rolling averages
        df = df.sort_values('date')
        
        # Calculate rolling averages
        df['rolling_home_score'] = df.groupby('home_team_id')['home_score'].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
        df['rolling_away_score'] = df.groupby('away_team_id')['away_score'].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
        df['rolling_total_goals'] = df['total_goals'].rolling(window=10, min_periods=1).mean()
        
        # Create target
        df['target'] = df['winner']
        
        output_file = CACHE_DIR / "nhl_features.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved improved NHL data to {output_file}")
        print(f"Features: {list(df.columns)}")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    improve_nhl_data()
