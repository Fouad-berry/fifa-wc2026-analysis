"""
metrics.py
----------
Top-level KPI summary printed after the pipeline runs.
"""

import logging

import pandas as pd

from src.logging_config import setup_logging
from src.paths import DM_BASE, PROCESSED_PATH

setup_logging()
log = logging.getLogger(__name__)


def run_all() -> dict:
    if not PROCESSED_PATH.exists():
        log.error("Processed file not found at %s", PROCESSED_PATH)
        print("Run 'python src/transformation/clean_transform.py' first.")
        return {}

    df = pd.read_csv(PROCESSED_PATH, parse_dates=["match_date"])

    player_path = DM_BASE / "dm_players/player_dim.csv"
    team_path = DM_BASE / "dm_teams/team_dim.csv"
    stadium_path = DM_BASE / "dm_stadiums/stadium_dim.csv"

    if not all(p.exists() for p in [player_path, team_path, stadium_path]):
        log.error("Datamarts not found. Run 'python src/datamarts/build_datamarts.py' first.")
        return {}

    players = pd.read_csv(player_path)
    teams = pd.read_csv(team_path)
    stadiums = pd.read_csv(stadium_path)

    total_goals = int(df["goals"].sum())
    avg_goals_per_match = round(df.groupby("match_id")["goals"].sum().mean(), 2)

    top_scorer = players.sort_values("total_goals_tournament", ascending=False).iloc[0]
    top_team = teams.sort_values("total_goals", ascending=False).iloc[0]
    best_stadium = stadiums.sort_values("goals_per_match", ascending=False).iloc[0]

    print("\n" + "=" * 52)
    print("⚽  FIFA WC 2026 — KEY METRICS SUMMARY")
    print("=" * 52)
    print(f"Total records:             {len(df):>10,}")
    print(f"Unique players:            {df['player_id'].nunique():>10,}")
    print(f"Unique matches:            {df['match_id'].nunique():>10,}")
    print(f"Participating nations:     {df['team'].nunique():>10,}")
    print(f"Host stadiums:             {df['stadium'].nunique():>10,}")
    print()
    print(f"Total goals scored:        {total_goals:>10,}")
    print(f"Avg goals per match:       {avg_goals_per_match:>10.2f}")
    print(f"Total yellow cards:        {int(df['yellow_cards'].sum()):>10,}")
    print(f"Total red cards:            {int(df['red_cards'].sum()):>10,}")
    print()
    print(f"Avg player rating:         {df['player_rating'].mean():>10.2f}")
    print(f"Avg distance covered:      {df['distance_covered_km'].mean():>9.1f} km")
    print(f"Avg top speed:             {df['top_speed_kmh'].mean():>9.1f} km/h")
    print()
    print(
        f"Top scorer:                {top_scorer['player_name']} ({top_scorer['team']}) "
        f"— {int(top_scorer['total_goals_tournament'])} goals"
    )
    print(f"Most goals (team):         {top_team['team']} — {int(top_team['total_goals'])} goals")
    print(
        f"Most goals/match stadium:  {best_stadium['stadium']} "
        f"({best_stadium['city']}) — {best_stadium['goals_per_match']:.1f} goals/match"
    )

    return {
        "total_records": len(df),
        "unique_players": int(df["player_id"].nunique()),
        "unique_matches": int(df["match_id"].nunique()),
        "nations": int(df["team"].nunique()),
        "stadiums": int(df["stadium"].nunique()),
        "total_goals": total_goals,
        "avg_goals_per_match": avg_goals_per_match,
    }


if __name__ == "__main__":
    run_all()
