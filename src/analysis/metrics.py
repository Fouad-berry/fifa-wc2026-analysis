"""
metrics.py
----------
Top-level KPI summary printed after the pipeline runs.
"""

import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)

PROCESSED_PATH = Path(__file__).parents[2] / "data" / "processed" / "wc2026_clean.csv"
DM_BASE        = Path(__file__).parents[2] / "data" / "datamarts"


def run_all() -> None:
    df        = pd.read_csv(PROCESSED_PATH, parse_dates=["match_date"])
    players   = pd.read_csv(DM_BASE / "dm_players/player_dim.csv")
    teams     = pd.read_csv(DM_BASE / "dm_teams/team_dim.csv")
    stadiums  = pd.read_csv(DM_BASE / "dm_stadiums/stadium_dim.csv")

    print("\n" + "=" * 52)
    print("⚽  FIFA WC 2026 — KEY METRICS SUMMARY")
    print("=" * 52)
    print(f"Total records:             {len(df):>10,}")
    print(f"Unique players:            {df['player_id'].nunique():>10,}")
    print(f"Unique matches:            {df['match_id'].nunique():>10,}")
    print(f"Participating nations:     {df['team'].nunique():>10,}")
    print(f"Host stadiums:             {df['stadium'].nunique():>10,}")
    print()
    print(f"Total goals scored:        {df['goals'].sum():>10,}")
    print(f"Avg goals per match:       {df.groupby('match_id')['goals'].sum().mean():>10.2f}")
    print(f"Total yellow cards:        {df['yellow_cards'].sum():>10,}")
    print(f"Total red cards:           {df['red_cards'].sum():>10,}")
    print()
    print(f"Avg player rating:         {df['player_rating'].mean():>10.2f}")
    print(f"Avg distance covered:      {df['distance_covered_km'].mean():>9.1f} km")
    print(f"Avg top speed:             {df['top_speed_kmh'].mean():>9.1f} km/h")
    print()

    top_scorer = (
        players.sort_values("total_goals_tournament", ascending=False)
        .iloc[0]
    )
    print(f"Top scorer:                {top_scorer['player_name']} ({top_scorer['team']}) "
          f"— {int(top_scorer['total_goals_tournament'])} goals")

    top_team = teams.sort_values("total_goals", ascending=False).iloc[0]
    print(f"Most goals (team):         {top_team['team']} — {int(top_team['total_goals'])} goals")

    best_stadium = stadiums.sort_values("goals_per_match", ascending=False).iloc[0]
    print(f"Most goals/match stadium:  {best_stadium['stadium']} "
          f"({best_stadium['city']}) — {best_stadium['goals_per_match']:.1f} goals/match")


if __name__ == "__main__":
    run_all()