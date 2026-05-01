# Sports Autoresearch - User Guide

Autonomous sports betting research system using AI to find betting edges for MLB, NBA, Golf, and Tennis.

## 🚀 Quick Start - How to Use This System

### Access the Dashboard
```bash
# Start the web dashboard
uv run python app.py

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

## Cloud Deployment (Recommended - Run 24/7)

**Easiest way to keep bot running when you close your laptop:**

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin autoresearch/may1
```

2. **Deploy to Render.com (FREE)**
- Go to render.com (free account)
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Use `render.yaml` configuration (already in project)
- Click "Deploy"

3. **Access from Anywhere**
- Your dashboard: `https://your-app.onrender.com`
- Works on phone, tablet, laptop - anywhere
- Bot runs 24/7, no need to keep laptop open

**Other Options:** See `BACKGROUND_RUNNING.md` for Windows Service, tmux, or VPS options.

## How Much to Bet

**The dashboard now includes a Bankroll Management section:**
- Enter your bankroll (e.g., $1000)
- System calculates recommended bet sizes:
  - **Conservative (1%)**: $10 per bet
  - **Moderate (2-3%)**: $25 per bet
  - **Aggressive (5%)**: $50 per bet

**Recommended:**
- Start with **1-2%** of bankroll per bet
- Never bet more than **5%** per game
- Kelly Criterion: Bet = (Edge / Odds) × Bankroll

**How Many Bets:**
- **3-5 bets per day** maximum
- Only bet on edges > 2%
- Spread bets across multiple games to reduce variance
- Quality over quantity - better to miss a good bet than make a bad one

**Example with $1000 bankroll:**
- Conservative: $10 per bet, 3-5 bets = $30-50 total daily
- Moderate: $25 per bet, 3-5 bets = $75-125 total daily
- Aggressive: $50 per bet, 3-5 bets = $150-250 total daily

## Technical Overview

This system is inspired by Andrej Karpathy's autoresearch but adapted for sports betting:
- Cascade (the AI agent) autonomously modifies `train.py` to experiment with different ML models
- Each experiment runs for a fixed time budget (5 minutes per sport)
- The goal is to maximize edge vs Vegas odds
- Cascade keeps improvements and discards failures, advancing the git branch
- **NEW**: Web dashboard for live predictions accessible from anywhere

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

## Key Metrics

- **accuracy**: Prediction accuracy on validation set
- **avg_edge_vs_vegas**: Average difference between model probability and implied Vegas probability (higher is better)
- **positive_edge_rate**: Percentage of predictions where model has positive edge

## Data Sources

- **BALLDONTLIE API**: NBA, NFL, MLB, NHL (free tier available)
- **SportsDataIO**: Comprehensive APIs with historical betting odds
- **The Odds API**: Betting odds across sports
- **CBS Sports**: Injury reports (scraped daily)

## Disclaimer

This is a research/educational project. Sports betting involves financial risk. Always gamble responsibly and within your means.

## License

MIT
