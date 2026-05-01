# Sports Autoresearch

Autonomous sports betting research system using Cascade (Windsurf AI) to experiment with ML models and find betting edges for MLB, NBA, Golf, and Tennis.

## 🚀 Quick Start - How to Use This System

### Access the Dashboard
```bash
# Start the web dashboard
uv run python app.py

- **NEW**: Web dashboard for live predictions accessible from anywhere

## Cloud Deployment

To access the dashboard from anywhere (while out and about):

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin autoresearch/may1
```

2. **Deploy to Render.com**
- Sign up at render.com (free tier available)
- Connect your GitHub repository
- Use `render.yaml` configuration
- Dashboard will be live at your Render URL

3. **Access from Anywhere**
- Use your Render URL on phone/tablet
- Mobile-responsive design works on all devices
- Check predictions while out and about
# Open in browser
http://localhost:5000
```

The dashboard is **mobile-friendly** - you can access it from your phone while out and about.

### When to Bet
- **Green Edge**: System shows positive edge (green color in dashboard)
- **Edge > 2%**: Only bet when edge is significant
- **Multiple Bookmakers**: When several books show similar positive edges

### Where to Bet
Recommended sportsbooks:
- DraftKings (best for NBA/NFL)
- FanDuel (good mobile app)
- BetMGM (competitive odds)
- Caesars (good promos)

**Strategy**: Always line shop - compare odds across multiple books and bet the best line.

### What Type of Bets

**Moneyline Bets (Primary - What the system tells you):**
- Pick which team wins the game
- Example: Lakers -150 vs Celtics +130
- System tells you which side has positive edge
- This is the main bet type to use

**Spread & Total Bets (Coming Soon):**
- Point spread bets
- Over/under totals
- Currently in development

### Injury Information
- **Scraped Daily**: System scrapes injury reports from CBS Sports
- **Integrated**: Injury count per team added to model predictions
- **Impact**: Teams with more injuries get lower win probabilities
- **Display**: Dashboard shows injury data for each team

### How to Read the Dashboard

**Best Betting Opportunities Section:**
```
San Antonio Spurs @ Minnesota Timberwolves
Minnesota Timberwolves +610
Edge: 44.6%
```
- Game: Spurs vs Timberwolves
- Bet: Timberwolves at +610 odds
- Edge: Model thinks Timberwolves have 44.6% better chance than Vegas
- Action: Consider betting on Timberwolves

**All Predictions Table:**
- Game: Matchup
- Team: Which team the odds are for
- Moneyline: Odds (positive = underdog, negative = favorite)
- Model Prob: System's win probability
- Edge: Difference between model and Vegas (green = bet, red = avoid)
- Bookmaker: Which sportsbook

### Daily Workflow

**Morning (8:00 AM):**
1. Open dashboard (http://localhost:5000)
2. Click "Train Models" - updates with latest data
3. Click "Refresh Predictions" - gets today's odds
4. Review "Best Betting Opportunities"
5. Place bets before games start

**Evening (6:00 PM):**
1. Refresh predictions for evening games
2. Check for line movements
3. Place additional bets if needed

**Automated Option:**
```bash
python schedule_daily.py
```
Predictions refresh automatically at 8:00 AM and 6:00 PM daily.

### Bankroll Management

**Recommended:**
- Start small: 1-2% of bankroll per bet
- Kelly Criterion: Bet = (Edge / Odds) × Bankroll
- Stop loss: Stop if down 10% in a day
- Take profit: Stop if up 20% in a day

**Example:**
- Bankroll: $1,000
- Edge: 5%
- Bet size: $50 (5% of bankroll)
- Never bet more than $100 per game

### Risk Management

**Don't:**
- Chase losses
- Bet more than 5% of bankroll
- Bet on games with negative edge
- Ignore injury reports
- Bet on unfamiliar teams

**Do:**
- Track all bets
- Review performance weekly
- Adjust based on results
- Stay disciplined
- Take breaks when losing

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
