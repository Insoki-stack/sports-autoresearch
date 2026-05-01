# Sports Autoresearch

Autonomous sports betting research system using Cascade (Windsurf AI) to experiment with ML models and find betting edges for MLB, NBA, Golf, and Tennis.

## Overview

This system is inspired by Andrej Karpathy's autoresearch but adapted for sports betting:
- Cascade (the AI agent) autonomously modifies `train.py` to experiment with different ML models
- Each experiment runs for a fixed time budget (5 minutes per sport)
- The goal is to maximize edge vs Vegas odds
- Cascade keeps improvements and discards failures, advancing the git branch

## Setup

### Prerequisites

- Python 3.10+
- uv package manager (recommended) or pip
- Historical sports data and betting odds

### Installation

```bash
# Install dependencies
pip install -r requirements.txt  # or: uv sync if using pyproject.toml

# Set up data cache
python prepare.py
```

### Data Requirements

Place historical data in `~/.cache/sports-autoresearch/`:

```
~/.cache/sports-autoresearch/
├── mlb_historical.csv      # MLB game data with features
├── mlb_odds.csv            # MLB betting odds
├── nba_historical.csv      # NBA game data
├── nba_odds.csv            # NBA betting odds
├── golf_historical.csv     # Golf tournament data
├── golf_odds.csv           # Golf betting odds
├── tennis_historical.csv   # Tennis match data
└── tennis_odds.csv         # Tennis betting odds
```

## Usage

### Manual Experiment

```bash
python train.py
```

This will train models for all configured sports and print evaluation metrics.

### Autonomous Research (with Cascade)

1. Open this project in Windsurf
2. Point Cascade to `program.md` for instructions
3. Cascade will autonomously:
   - Modify `train.py` with experimental changes
   - Run training experiments
   - Evaluate results
   - Keep improvements, discard failures
   - Iterate overnight

## Project Structure

```
prepare.py      — Fixed constants, data prep, evaluation (DO NOT MODIFY)
train.py        — ML models, features, hyperparameters (Cascade modifies this)
program.md      — Agent instructions for Cascade
pyproject.toml  — Dependencies
README.md       — This file
```

## Key Metrics

- **accuracy**: Prediction accuracy on validation set
- **avg_edge_vs_vegas**: Average difference between model probability and implied Vegas probability (higher is better)
- **positive_edge_rate**: Percentage of predictions where model has positive edge

## Design Choices

- **Single file to modify**: Cascade only touches `train.py`. Keeps scope manageable.
- **Fixed time budget**: Each sport trains for exactly 5 minutes. Makes experiments comparable.
- **Multi-sport**: Supports MLB, NBA, Golf, Tennis simultaneously.
- **Self-contained**: Uses standard ML libraries (XGBoost, scikit-learn).

## Data Sources

Recommended data sources:
- **BALLDONTLIE API**: NBA, NFL, MLB, NHL (free tier available)
- **SportsDataIO**: Comprehensive APIs with historical betting odds
- **DataGolf**: PGA golf statistics
- **The Odds API**: Betting odds across sports

## Disclaimer

This is a research/educational project. Sports betting involves financial risk. Always gamble responsibly and within your means.

## License

MIT
