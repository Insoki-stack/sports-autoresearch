"""
database.py - SQLite database for bet tracking
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict

DB_PATH = Path.home() / ".cache" / "sports-autoresearch" / "bets.db"

def init_db():
    """Initialize the database with bets table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT,
            sport TEXT,
            away_team TEXT,
            home_team TEXT,
            selected_team TEXT,
            bet_type TEXT DEFAULT 'moneyline',
            amount_bet REAL,
            odds REAL,
            bookmaker TEXT DEFAULT 'BetOnline.ag',
            prediction_edge REAL,
            model_prob REAL,
            status TEXT DEFAULT 'pending',  -- pending, won, lost, push
            profit_loss REAL DEFAULT 0.0,
            placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            settled_at TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def add_bet(bet_data: Dict) -> int:
    """Add a new bet to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO bets (
            game_id, sport, away_team, home_team, selected_team,
            bet_type, amount_bet, odds, bookmaker, prediction_edge, model_prob
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        bet_data.get('game_id', ''),
        bet_data.get('sport', ''),
        bet_data.get('away_team', ''),
        bet_data.get('home_team', ''),
        bet_data.get('selected_team', ''),
        bet_data.get('bet_type', 'moneyline'),
        bet_data.get('amount_bet', 0),
        bet_data.get('odds', 0),
        bet_data.get('bookmaker', 'BetOnline.ag'),
        bet_data.get('prediction_edge', 0),
        bet_data.get('model_prob', 0)
    ))
    
    bet_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return bet_id

def get_bets(sport: str = None, status: str = None, bookmaker: str = None) -> List[Dict]:
    """Get bets from database with optional filters."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM bets WHERE 1=1"
    params = []
    
    if sport:
        query += " AND sport = ?"
        params.append(sport)
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if bookmaker:
        query += " AND bookmaker = ?"
        params.append(bookmaker)
    
    query += " ORDER BY placed_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    bets = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return bets

def update_bet_status(bet_id: int, status: str, profit_loss: float = 0.0):
    """Update bet status and profit/loss after game settles."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE bets 
        SET status = ?, profit_loss = ?, settled_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, profit_loss, bet_id))
    
    conn.commit()
    conn.close()

def get_betting_stats(bookmaker: str = None) -> Dict:
    """Get betting statistics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM bets"
    params = []
    
    if bookmaker:
        query += " WHERE bookmaker = ?"
        params.append(bookmaker)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    total_bets = len(rows)
    if total_bets == 0:
        return {
            'total_bets': 0,
            'wins': 0,
            'losses': 0,
            'pushes': 0,
            'win_rate': 0,
            'total_profit_loss': 0,
            'roi': 0
        }
    
    columns = [desc[0] for desc in cursor.description]
    bets = [dict(zip(columns, row)) for row in rows]
    
    wins = sum(1 for b in bets if b['status'] == 'won')
    losses = sum(1 for b in bets if b['status'] == 'lost')
    pushes = sum(1 for b in bets if b['status'] == 'push')
    settled = wins + losses + pushes
    
    win_rate = (wins / settled * 100) if settled > 0 else 0
    total_profit_loss = sum(b['profit_loss'] for b in bets if b['status'] in ['won', 'lost'])
    total_bet = sum(b['amount_bet'] for b in bets if b['status'] in ['won', 'lost'])
    roi = (total_profit_loss / total_bet * 100) if total_bet > 0 else 0
    
    conn.close()
    
    return {
        'total_bets': total_bets,
        'wins': wins,
        'losses': losses,
        'pushes': pushes,
        'win_rate': round(win_rate, 1),
        'total_profit_loss': round(total_profit_loss, 2),
        'roi': round(roi, 1)
    }

# Initialize database on import
init_db()
