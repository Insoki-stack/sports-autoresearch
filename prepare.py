"""
prepare.py - Fixed constants, data preparation, and runtime utilities.
DO NOT MODIFY THIS FILE - It contains the evaluation harness and training constants.
"""

import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# ==============================================================================
# FIXED CONSTANTS - DO NOT MODIFY
# ==============================================================================

# Data cache directory
CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Sports configuration
SPORTS_CONFIG = {
    "mlb": {
        "name": "MLB",
        "api_base": "https://api.sportsdata.io/v3/mlb",
        "time_budget_seconds": 300,  # 5 minutes per experiment
        "train_split": 0.8,
        "val_split": 0.1,
        "test_split": 0.1,
    },
    "nba": {
        "name": "NBA",
        "api_base": "https://api.balldontlie.io/v1",
        "time_budget_seconds": 300,
        "train_split": 0.8,
        "val_split": 0.1,
        "test_split": 0.1,
    },
    "golf": {
        "name": "PGA Golf",
        "api_base": "https://api.datagolf.com",
        "time_budget_seconds": 300,
        "train_split": 0.8,
        "val_split": 0.1,
        "test_split": 0.1,
    },
    "tennis": {
        "name": "Tennis",
        "api_base": None,  # Will use historical datasets
        "time_budget_seconds": 300,
        "train_split": 0.8,
        "val_split": 0.1,
        "test_split": 0.1,
    },
}

# Evaluation metrics
METRICS = {
    "edge_vs_vegas": "Difference between model probability and implied Vegas probability",
    "roi": "Return on investment if bets were placed",
    "accuracy": "Prediction accuracy on validation set",
    "calibration": "Brier score for probability calibration",
}

# ==============================================================================
# DATA LOADING FUNCTIONS
# ==============================================================================

def load_historical_data(sport: str) -> pd.DataFrame:
    """
    Load historical data for a sport from cache.
    Try processed data, then full data, then raw data.
    """
    # Try processed data first
    processed_file = CACHE_DIR / f"{sport}_processed.csv"
    if processed_file.exists():
        print(f"Loading processed data for {sport}")
        return pd.read_csv(processed_file)
    
    # Try full data (from free internet sources)
    full_file = CACHE_DIR / f"{sport}_historical_full.csv"
    if full_file.exists():
        print(f"Loading full data for {sport}")
        return pd.read_csv(full_file)
    
    # Fall back to raw data
    cache_file = CACHE_DIR / f"{sport}_historical.csv"
    if cache_file.exists():
        print(f"Loading cached data for {sport}")
        return pd.read_csv(cache_file)
    
    print(f"No cached data found for {sport}. Expected location: {cache_file}")
    return pd.DataFrame()

def load_betting_odds(sport: str) -> pd.DataFrame:
    """
    Load betting odds data for a sport.
    """
    cache_file = CACHE_DIR / f"{sport}_odds.csv"
    
    if cache_file.exists():
        return pd.read_csv(cache_file)
    
    print(f"No odds data found for {sport}. Expected location: {cache_file}")
    return pd.DataFrame()

def prepare_features(sport: str, data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare features for ML model.
    This is a placeholder - actual implementation will sport-specific.
    """
    return data

# ==============================================================================
# EVALUATION HARNESS - DO NOT MODIFY
# ==============================================================================

def calculate_edge_vs_vegas(
    model_prob: float,
    vegas_odds: float,
    bet_type: str = "moneyline"
) -> float:
    """
    Calculate the edge between model probability and implied Vegas probability.
    
    Args:
        model_prob: Model's predicted probability (0-1)
        vegas_odds: Vegas odds in American format (e.g., +150, -110)
        bet_type: Type of bet (moneyline, spread, total)
    
    Returns:
        Edge as a percentage (positive = model thinks it's a good bet)
    """
    # Convert American odds to implied probability
    if vegas_odds > 0:
        vegas_prob = 100 / (vegas_odds + 100)
    else:
        vegas_prob = -vegas_odds / (-vegas_odds + 100)
    
    # Account for vig (typically ~5%)
    vegas_prob *= 0.95
    
    edge = model_prob - vegas_prob
    return edge

def evaluate_predictions(
    predictions: np.ndarray,
    actuals: np.ndarray,
    vegas_odds: np.ndarray
) -> Dict[str, float]:
    """
    Evaluate model predictions against actual outcomes.
    
    Returns:
        Dictionary with evaluation metrics
    """
    accuracy = np.mean(predictions == actuals)
    
    # Calculate edge for each prediction
    edges = []
    for i, (pred, actual, odds) in enumerate(zip(predictions, actuals, vegas_odds)):
        edge = calculate_edge_vs_vegas(pred, odds)
        edges.append(edge)
    
    avg_edge = np.mean(edges)
    positive_edge_rate = np.mean([e > 0 for e in edges])
    
    return {
        "accuracy": float(accuracy),
        "avg_edge_vs_vegas": float(avg_edge),
        "positive_edge_rate": float(positive_edge_rate),
    }

def print_evaluation_summary(metrics: Dict[str, float], sport: str):
    """
    Print evaluation summary in a fixed format.
    """
    print("---")
    print(f"sport:              {sport}")
    print(f"accuracy:           {metrics['accuracy']:.6f}")
    print(f"avg_edge_vs_vegas:  {metrics['avg_edge_vs_vegas']:.6f}")
    print(f"positive_edge_rate: {metrics['positive_edge_rate']:.6f}")
    print("---")

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def setup_data_cache():
    """Create data cache directory and placeholder files."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Data cache directory: {CACHE_DIR}")
    print("\nTo use this system, you need to download historical data for each sport:")
    for sport in SPORTS_CONFIG:
        print(f"  - {sport.upper()}: Place data in {CACHE_DIR / f'{sport}_historical.csv'}")
        print(f"  - {sport.upper()} odds: Place data in {CACHE_DIR / f'{sport}_odds.csv'}")

def get_sports_list() -> List[str]:
    """Return list of supported sports."""
    return list(SPORTS_CONFIG.keys())

if __name__ == "__main__":
    setup_data_cache()
