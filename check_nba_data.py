import pandas as pd

df = pd.read_csv('C:/Users/Boydb/.cache/sports-autoresearch/nba_historical_bdl.csv')
print(f'Total games: {len(df)}')
print(f'Seasons: {df["season"].unique() if "season" in df.columns else "N/A"}')
print(f'Date range: {df["date"].min() if "date" in df.columns else "N/A"} to {df["date"].max() if "date" in df.columns else "N/A"}')
print(df.head())
