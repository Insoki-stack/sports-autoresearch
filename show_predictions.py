import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "sports-autoresearch"

print("="*60)
print("PREDICTION LOGS FOR ALL SPORTS")
print("="*60)

for sport in ['mlb', 'nba', 'nhl', 'soccer']:
    file_path = CACHE_DIR / f"{sport}_predictions_current.csv"
    if file_path.exists():
        df = pd.read_csv(file_path)
        print(f"\n{sport.upper()} Prediction Logs:")
        print(f"  Total predictions: {len(df)}")
        print(f"  Edge range: {df['edge_vs_vegas'].min():.4f} to {df['edge_vs_vegas'].max():.4f}")
        print(f"  Average edge: {df['edge_vs_vegas'].mean():.4f}")
        print(f"  Positive edge rate: {(df['edge_vs_vegas'] > 0).sum() / len(df):.2%}")
        if 'bet_type' in df.columns:
            print(f"  Bet types: {df['bet_type'].unique().tolist()}")
        print(f"  Sample predictions:")
        cols = ['team', 'moneyline', 'edge_vs_vegas']
        if 'bet_type' in df.columns:
            cols.insert(2, 'bet_type')
        print(df[cols].head(5).to_string(index=False))
    else:
        print(f"\n{sport.upper()}: No predictions file found")

print("\n" + "="*60)
