# Rolling Insights Historical Data Guide

## Automated APIs Failed

BALLDONTLIE API issues:
- Rate limiting (429 errors)
- Wrong data (1946 instead of 2022-2024)
- 401 unauthorized errors
- Free tier too limited

iSports API issues:
- Invalid SSL certificate
- Security warning

## Recommended: Manual Download via Rolling Insights

Rolling Insights offers free historical NFL, NBA, MLB & NHL stats with CSV exports.

## Steps:

1. **Sign up for free**: https://sportwise.rolling-insights.com/register
2. **Browse DataSpaces**: Check featured DataSpaces or create your own
3. **Select data**: Choose the stats you need (games, scores, teams, players)
4. **Export as CSV File**: One-click export to CSV file

## Data Available:
- NFL: Historical game data, team stats, player stats (back to 2017)
- NBA: Historical game data, team stats, player stats (back to 2017)
- MLB: Historical game data, team stats, player stats (back to 2017)
- NHL: Historical game data, team stats, player stats (back to 2017)

## After Downloading CSVs:

1. Place CSV files in: `C:\Users\Boydb\.cache\sports-autoresearch\`
2. Rename files to match expected format:
   - `nba_historical_rolling.csv`
   - `nhl_historical_rolling.csv`
   - `mlb_historical_rolling.csv`
3. Contact me to train models with this data

## Recommended Data to Download:
- **NBA**: Game scores, team records, player stats for 2022-2024
- **NHL**: Game scores, team records, player stats for 2022-2024
- **MLB**: Game scores, team records, pitcher stats for 2022-2024

## Advantages:
- Free access
- No API key required
- Manual selection of specific data points
- Clean CSV format ready for analysis
- No rate limiting
