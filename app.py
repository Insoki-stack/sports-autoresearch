"""
app.py - Web dashboard for sports betting predictions
Accessible from anywhere with mobile-responsive design
"""

from flask import Flask, render_template, jsonify
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from predict_current import predict_games
from train import train_all_sports

app = Flask(__name__)

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/predictions/<sport>')
def get_sport_predictions(sport):
    """API endpoint for predictions for a specific sport."""
    predictions_file = CACHE_DIR / f"{sport}_predictions_current.csv"
    
    if not predictions_file.exists():
        # Generate fresh predictions
        if sport == 'nba':
            predict_games()
        else:
            from add_sports import fetch_sport_odds
            fetch_sport_odds(sport)
    
    if predictions_file.exists():
        df = pd.read_csv(predictions_file)
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({"error": f"No predictions available for {sport}"})

@app.route('/api/predictions')
def get_predictions():
    """API endpoint for all sports predictions."""
    sports = ['mlb', 'nba', 'nfl', 'nhl', 'soccer']
    all_predictions = {}
    
    for sport in sports:
        predictions_file = CACHE_DIR / f"{sport}_predictions_current.csv"
        if predictions_file.exists():
            df = pd.read_csv(predictions_file)
            all_predictions[sport] = df.to_dict(orient='records')
        else:
            # Generate predictions for this sport
            if sport == 'nba':
                predict_games()
            elif sport == 'mlb':
                from add_sports import fetch_mlb_odds
                fetch_mlb_odds()
            else:
                from add_sports import fetch_sport_odds
                fetch_sport_odds(sport)
            
            # Try again after generating
            if predictions_file.exists():
                df = pd.read_csv(predictions_file)
                all_predictions[sport] = df.to_dict(orient='records')
            else:
                all_predictions[sport] = []
    
    return jsonify(all_predictions)

@app.route('/api/refresh')
def refresh_predictions():
    """Refresh predictions for all sports."""
    # Refresh MLB (prioritized for summer)
    from add_sports impNrB fetcA_mlb_odds
    try:
        ftch_mlb_odds()
    except:
        pass
    
    # Refresh othe
    predict_games()
    
    # Refresh other sports
    fromtry:
             add_sports import fetc
        except:
            passh_sport_odds
    sports = ['nfl', 'nhl', 'soccer']
    for sport in sports:
        fetch_sport_odds(sport)
    
    return jsonify({"status": "success", "message": "All sports predictions refreshed"})

@app.route('/api/train')
def train_models():
    """Train models on latest data."""
    try:
        train_all_sports()
        return jsonify({"status": "success", "message": "Models trained successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("Starting Sports Betting Dashboard...")
    print("Access at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
