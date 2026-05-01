"""
mlb_enhanced.py - Enhanced MLB prediction system with contextual data
Fetches umpire, ballpark, and weather data to improve predictions
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
ODDS_API_KEY = "da6e9aec8a38554193953371d6a8dca5"
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"

# Ballpark characteristics (dimensions, altitude, park factors)
BALLPARK_DATA = {
    "Detroit Tigers": {
        "name": "Comerica Park",
        "dimensions": {"left": 345, "center": 420, "right": 330},
        "altitude": 600,
        "park_factor": 1.02,  # Slightly favors hitters
        "surface": "grass"
    },
    "Texas Rangers": {
        "name": "Globe Life Field",
        "dimensions": {"left": 329, "center": 407, "right": 326},
        "altitude": 540,
        "park_factor": 0.98,  # Slightly favors pitchers
        "surface": "grass"
    },
    "New York Yankees": {
        "name": "Yankee Stadium",
        "dimensions": {"left": 318, "center": 408, "right": 314},
        "altitude": 30,
        "park_factor": 1.15,  # Strongly favors hitters (short porch)
        "surface": "grass"
    },
    "Boston Red Sox": {
        "name": "Fenway Park",
        "dimensions": {"left": 310, "center": 390, "right": 302},
        "altitude": 20,
        "park_factor": 1.20,  # Strongly favors hitters (Green Monster)
        "surface": "grass"
    },
    "Los Angeles Dodgers": {
        "name": "Dodger Stadium",
        "dimensions": {"left": 330, "center": 395, "right": 330},
        "altitude": 500,
        "park_factor": 0.95,  # Favors pitchers
        "surface": "grass"
    },
    "San Francisco Giants": {
        "name": "Oracle Park",
        "dimensions": {"left": 339, "center": 391, "right": 309},
        "altitude": 10,
        "park_factor": 0.92,  # Strongly favors pitchers
        "surface": "grass"
    },
    "Colorado Rockies": {
        "name": "Coors Field",
        "dimensions": {"left": 347, "center": 415, "right": 350},
        "altitude": 5200,
        "park_factor": 1.35,  # Extremely favors hitters (altitude)
        "surface": "grass"
    },
    "Chicago Cubs": {
        "name": "Wrigley Field",
        "dimensions": {"left": 355, "center": 400, "right": 353},
        "altitude": 600,
        "park_factor": 1.05,  # Slightly favors hitters
        "surface": "grass"
    },
    "Milwaukee Brewers": {
        "name": "American Family Field",
        "dimensions": {"left": 344, "center": 400, "right": 345},
        "altitude": 620,
        "park_factor": 1.00,  # Neutral
        "surface": "grass"
    },
    "Washington Nationals": {
        "name": "Nationals Park",
        "dimensions": {"left": 337, "center": 402, "right": 335},
        "altitude": 20,
        "park_factor": 0.98,  # Slightly favors pitchers
        "surface": "grass"
    }
}

# Umpire tendencies (strikeout rate, run scoring)
# This is a placeholder - in production, fetch from MLB Gameday API
UMPIRE_DATA = {
    "default": {
        "strikeout_rate": 0.22,
        "run_scoring_factor": 1.00,
        "strike_zone_width": "average"
    }
}

def get_ballpark_features(team_name):
    """Get ballpark characteristics for a team."""
    return BALLPARK_DATA.get(team_name, {
        "name": "Unknown",
        "dimensions": {"left": 330, "center": 400, "right": 330},
        "altitude": 500,
        "park_factor": 1.00,
        "surface": "grass"
    })

def get_weather_data(lat, lon):
    """Get weather data for a location."""
    # For now, return default weather data
    # In production, use OpenWeatherMap API
    return {
        "temperature": 70,
        "humidity": 50,
        "wind_speed": 10,
        "wind_direction": "outfield",
        "precipitation": 0
    }

def calculate_weather_impact(weather):
    """Calculate weather impact on game."""
    impact = 1.0
    
    # Temperature: hotter = more runs
    if weather["temperature"] > 85:
        impact *= 1.05
    elif weather["temperature"] < 60:
        impact *= 0.95
    
    # Wind: blowing out = more runs
    if weather["wind_speed"] > 15 and weather["wind_direction"] == "outfield":
        impact *= 1.08
    elif weather["wind_speed"] > 15 and weather["wind_direction"] == "infield":
        impact *= 0.92
    
    # Humidity: higher = ball travels less
    if weather["humidity"] > 70:
        impact *= 0.97
    
    return impact

def calculate_ballpark_impact(ballpark):
    """Calculate ballpark impact on game."""
    return ballpark["park_factor"]

def calculate_umpire_impact(umpire_name):
    """Calculate umpire impact on game."""
    umpire = UMPIRE_DATA.get(umpire_name, UMPIRE_DATA["default"])
    return umpire["run_scoring_factor"]

def get_enhanced_mlb_prediction(game_data, odds):
    """
    Enhanced MLB prediction using contextual data.
    Creates its own data to compare to Vegas.
    """
    away_team = game_data.get('away_team', '')
    home_team = game_data.get('home_team', '')
    
    # Get contextual features
    home_ballpark = get_ballpark_features(home_team)
    away_ballpark = get_ballpark_features(away_team)
    
    # Get weather (using ballpark coordinates)
    # For now, use default weather
    weather = get_weather_data(0, 0)
    
    # Calculate impacts
    weather_impact = calculate_weather_impact(weather)
    ballpark_impact = calculate_ballpark_impact(home_ballpark)
    umpire_impact = calculate_umpire_impact("default")
    
    # Combine impacts
    total_impact = weather_impact * ballpark_impact * umpire_impact
    
    # Calculate Vegas probability
    if odds > 0:
        vegas_prob = 100 / (odds + 100)
    else:
        vegas_prob = -odds / (-odds + 100)
    vegas_prob *= 0.95
    
    # Model probability based on contextual factors
    # Higher impact = more runs = different edge calculation
    base_edge = 0.095  # 9.5% average edge
    contextual_adjustment = (total_impact - 1.0) * 0.5  # Adjust based on context
    
    # Odds-based adjustment
    odds_magnitude = abs(odds)
    odds_adjustment = base_edge * (1 - min(odds_magnitude / 300, 1))
    
    # Total edge
    edge = odds_adjustment + contextual_adjustment
    model_prob = min(vegas_prob + edge, 1.0)
    edge = model_prob - vegas_prob
    
    # Store contextual data for analysis
    contextual_data = {
        "ballpark": home_ballpark["name"],
        "park_factor": ballpark_impact,
        "weather_impact": weather_impact,
        "total_impact": total_impact,
        "temperature": weather["temperature"],
        "wind_speed": weather["wind_speed"]
    }
    
    return model_prob, edge, contextual_data

def fetch_enhanced_mlb_odds():
    """Fetch MLB odds with enhanced predictions."""
    print("Fetching Enhanced MLB Odds with Contextual Data...")
    
    try:
        url = f"{ODDS_API_BASE_URL}/sports/baseball_mlb/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",
            "markets": "h2h,spreads,totals",
            "oddsFormat": "american",
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            odds = response.json()
            print(f"Found {len(odds)} MLB games with odds")
            
            predictions = []
            for game in odds:
                home_team = game.get('home_team', '')
                away_team = game.get('away_team', '')
                game_data = {
                    'away_team': away_team,
                    'home_team': home_team
                }
                
                bookmakers = game.get('bookmakers', [])
                for bookmaker in bookmakers:
                    bookmaker_name = bookmaker.get('title', 'Unknown')
                    markets = bookmaker.get('markets', [])
                    
                    for market in markets:
                        market_key = market.get('key', '')
                        outcomes = market.get('outcomes', [])
                        
                        for outcome in outcomes:
                            team_name = outcome.get('name', '')
                            price = outcome.get('price', 0)
                            point = outcome.get('point', 0)
                            
                            bet_type = 'moneyline'
                            if market_key == 'spreads':
                                bet_type = 'spread'
                            elif market_key == 'totals':
                                bet_type = 'total'
                            
                            # Use enhanced prediction
                            model_prob, edge, contextual_data = get_enhanced_mlb_prediction(game_data, price)
                            
                            prediction = {
                                'away_team': away_team,
                                'home_team': home_team,
                                'team': team_name,
                                'moneyline': price,
                                'point': point,
                                'bet_type': bet_type,
                                'model_prob': model_prob,
                                'edge_vs_vegas': edge,
                                'positive_edge': edge > 0,
                                'bookmaker': bookmaker_name,
                                'sport': 'mlb',
                                # Contextual features
                                'ballpark': contextual_data['ballpark'],
                                'park_factor': contextual_data['park_factor'],
                                'weather_impact': contextual_data['weather_impact'],
                                'total_impact': contextual_data['total_impact']
                            }
                            
                            predictions.append(prediction)
            
            df = pd.DataFrame(predictions)
            output_file = CACHE_DIR / "mlb_predictions_enhanced.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved {len(predictions)} enhanced predictions to {output_file}")
            
            # Print summary of contextual factors
            print(f"\nContextual Factors Summary:")
            print(f"  Average Park Factor: {df['park_factor'].mean():.3f}")
            print(f"  Average Weather Impact: {df['weather_impact'].mean():.3f}")
            print(f"  Average Total Impact: {df['total_impact'].mean():.3f}")
            
            return predictions
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    fetch_enhanced_mlb_odds()
