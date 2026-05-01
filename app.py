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

@app.route('/api/predictions')
def get_predictions():
    """API endpoint for current predictions."""
    predictions_file = CACHE_DIR / "nba_predictions_current.csv"
    
    if not predictions_file.exists():
        # Generate fresh predictions
        predict_games()
    
    if predictions_file.exists():
        df = pd.read_csv(predictions_file)
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({"error": "No predictions available"})

@app.route('/api/refresh')
def refresh_predictions():
    """Refresh predictions by fetching latest odds."""
    predictions_df = predict_games()
    
    if predictions_df is not None:
        return jsonify({"status": "success", "count": len(predictions_df)})
    else:
        return jsonify({"status": "error", "message": "Failed to fetch predictions"})

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
