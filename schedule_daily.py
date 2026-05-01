"""
schedule_daily.py - Set up automated daily predictions
Uses schedule library to run predictions daily at specified times
"""

import schedule
import time
from pathlib import Path
import subprocess
from datetime import datetime

def run_daily_predictions():
    """Run daily prediction workflow."""
    print("="*60)
    print("Running Daily Predictions")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Train models
        print("\n1. Training models...")
        subprocess.run(["uv", "run", "python", "train.py"], cwd=Path(__file__).parent)
        
        # Generate predictions
        print("\n2. Generating predictions...")
        subprocess.run(["uv", "run", "python", "predict_current.py"], cwd=Path(__file__).parent)
        
        print("\n" + "="*60)
        print("Daily Predictions Complete!")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main scheduling loop."""
    print("="*60)
    print("Starting Daily Prediction Scheduler")
    print("="*60)
    print("Predictions will run daily at 8:00 AM and 6:00 PM")
    print("Press Ctrl+C to stop")
    
    # Schedule predictions for 8:00 AM and 6:00 PM
    schedule.every().day.at("08:00").do(run_daily_predictions)
    schedule.every().day.at("18:00").do(run_daily_predictions)
    
    # Run immediately on start
    run_daily_predictions()
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
