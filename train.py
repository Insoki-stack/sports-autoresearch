"""
train.py - ML models for sports betting.
THIS IS THE FILE CASCADE MODIFIES.
Everything is fair game: model architecture, features, hyperparameters, etc.
"""

import numpy as np
import pandas as pd
from typing import Tuple
from pathlib import Path
from xgboost import XGBClassifier, XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, brier_score_loss
import prepare
import time

# ==============================================================================
# MODEL CONFIGURATION - CASCADE CAN MODIFY THIS
# ==============================================================================

class SportsBettingModel:
    """
    Base class for sports betting models.
    Cascade can modify this class to experiment with different architectures.
    """
    
    def __init__(self, sport: str):
        self.sport = sport
        self.model = None
        self.scaler = StandardScaler()
        
        # Hyperparameters - Cascade can modify these
        self.params = {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "random_state": 42,
        }
    
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features and target from dataframe.
        Cascade can modify feature engineering here.
        """
        # Use only numeric columns as features
        feature_cols = [col for col in df.columns if col not in ['target', 'date'] and df[col].dtype in ['int64', 'float64']]
        
        if not feature_cols:
            # If no numeric columns, create simple numeric features
            print("Warning: No numeric columns found, creating simple features")
            feature_cols = [col for col in df.columns if col not in ['target', 'date']]
            X = pd.get_dummies(df[feature_cols], drop_first=True).values
        else:
            X = df[feature_cols].values
        
        y = df['target'].values if 'target' in df.columns else np.zeros(len(df))
        
        return X, y
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the model.
        Cascade can modify the training process.
        """
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        self.model = XGBClassifier(**self.params)
        self.model.fit(X_train_scaled, y_train)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        Cascade can modify prediction logic.
        """
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]

# ==============================================================================
# SPORT-SPECIFIC MODELS - CASCADE CAN MODIFY THESE
# ==============================================================================

class MLBModel(SportsBettingModel):
    """MLB-specific betting model."""
    
    def __init__(self):
        super().__init__("mlb")
        # MLB-specific hyperparameters
        self.params.update({
            "n_estimators": 200,  # Increased from 150
            "max_depth": 8,
            "learning_rate": 0.05,  # Lower learning rate
        })

class NBAModel(SportsBettingModel):
    """NBA-specific betting model."""
    
    def __init__(self):
        super().__init__("nba")
        # NBA-specific hyperparameters - tuned for larger dataset
        self.params.update({
            "n_estimators": 300,
            "max_depth": 8,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_alpha": 0.1,  # L1 regularization
            "reg_lambda": 1.0,  # L2 regularization
        })

class GolfModel(SportsBettingModel):
    """Golf-specific betting model."""
    
    def __init__(self):
        super().__init__("golf")
        # Golf-specific hyperparameters
        self.params.update({
            "n_estimators": 100,
            "max_depth": 5,
        })

class TennisModel(SportsBettingModel):
    """Tennis-specific betting model."""
    
    def __init__(self):
        super().__init__("tennis")
        # Tennis-specific hyperparameters
        self.params.update({
            "n_estimators": 180,
            "max_depth": 6,
        })

class SoccerModel(SportsBettingModel):
    """Soccer-specific betting model."""
    
    def __init__(self):
        super().__init__("soccer")
        # Soccer-specific hyperparameters
        self.params.update({
            "n_estimators": 250,
            "max_depth": 7,
            "learning_rate": 0.05,
        })

class NHLModel(SportsBettingModel):
    """NHL-specific betting model."""
    
    def __init__(self):
        super().__init__("nhl")
        # NHL-specific hyperparameters
        self.params.update({
            "n_estimators": 200,
            "max_depth": 6,
            "learning_rate": 0.05,
        })

# ==============================================================================
# TRAINING LOOP - CASCADE SHOULD NOT MODIFY TIME BUDGET
# ==============================================================================

def train_sport_model(sport: str, time_budget: int = 300):
    """
    Train a model for a specific sport with a fixed time budget.
    """
    print(f"\n{'='*60}")
    print(f"Training {sport.upper()} model")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    # Load data
    data = prepare.load_historical_data(sport)
    if data.empty:
        print(f"No data available for {sport}. Skipping.")
        return None
    
    odds = prepare.load_betting_odds(sport)
    
    # Get model instance
    model_map = {
        "mlb": MLBModel,
        "nba": NBAModel,
        "golf": GolfModel,
        "tennis": TennisModel,
    }
    
    if sport not in model_map:
        print(f"Unknown sport: {sport}")
        return None
    
    model = model_map[sport]()
    
    # Prepare data
    X, y = model.prepare_data(data)
    
    # Split data
    config = prepare.SPORTS_CONFIG[sport]
    X_train, X_val, y_train, y_val = train_test_split(
        X, y,
        train_size=config["train_split"],
        test_size=config["val_split"] + config["test_split"],
        random_state=42
    )
    
    # Train with time budget
    training_start = time.time()
    model.train(X_train, y_train)
    training_time = time.time() - training_start
    
    print(f"Training completed in {training_time:.2f}s")
    
    # Evaluate
    predictions = model.predict(X_val)
    
    # Load real odds if available (MLB, NBA), otherwise use mock odds
    odds_file = Path.home() / ".cache" / "sports-autoresearch" / f"{sport}_odds.csv"
    if odds_file.exists():
        try:
            odds_df = pd.read_csv(odds_file)
            # Use average odds from bookmakers
            if not odds_df.empty:
                real_odds = odds_df.groupby('outcome')['price'].mean().values
                # Pad or truncate to match predictions length
                if len(real_odds) >= len(predictions):
                    real_odds = real_odds[:len(predictions)]
                else:
                    real_odds = np.pad(real_odds, (0, len(predictions) - len(real_odds)), 'edge')
                print(f"Using real odds from {len(odds_df)} entries")
                mock_odds = real_odds
            else:
                mock_odds = np.random.uniform(-200, 200, len(predictions))
        except Exception as e:
            print(f"Error loading odds: {e}, using mock odds")
            mock_odds = np.random.uniform(-200, 200, len(predictions))
    else:
        mock_odds = np.random.uniform(-200, 200, len(predictions))
    
    metrics = prepare.evaluate_predictions(
        (predictions > 0.5).astype(int),
        y_val,
        mock_odds
    )
    
    prepare.print_evaluation_summary(metrics, sport)
    
    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f}s")
    
    return model, metrics

# ==============================================================================
# MAIN EXPERIMENT
# ==============================================================================

def train_all_sports():
    """Train models for all sports."""
    print("="*60)
    print("Training All Sports Models")
    print("="*60)
    
    sports = ['mlb', 'nba', 'golf', 'tennis']
    
    for sport in sports:
        try:
            train_sport_model(sport, time_budget=300)
        except Exception as e:
            print(f"Error training {sport}: {e}")
    
    print("\n" + "="*60)
    print("All Models Training Complete!")
    print("="*60)

if __name__ == "__main__":
    train_all_sports()
