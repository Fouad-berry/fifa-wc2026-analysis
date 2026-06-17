# Datamart Architecture — Star Schema

## Overview

The FIFA WC 2026 data warehouse follows a **star schema** with one central fact table and four dimension tables.

```
                         ┌──────────────────────────┐
                         │       dim_players         │
                         │  PK: player_id            │
                         │  1 248 rows               │
                         │  • Profile & physical     │
                         │  • Market value           │
                         │  • Tournament totals      │
                         └────────────┬─────────────┘
                                      │ many_to_one
                                      │
┌──────────────────┐    ┌─────────────▼──────────────┐    ┌──────────────────────┐
│   dim_matches    │    │      fact_performance        │    │      dim_teams        │
│  PK: match_id   │────│   Grain: player × match      │────│  PK: team             │
│  1 050 rows     │    │   54 600 rows                 │    │  48 rows              │
│  • Date & stage │    │                               │    │  • Squad stats        │
│  • Stadium/city │    │  FK: player_id                │    │  • Win/draw/loss      │
│  • Agg stats    │    │  FK: match_id                 │    │  • Avg market value   │
└──────────────────┘    │  FK: team                    │    └──────────────────────┘
         ▲              │  FK: stadium (via match)      │
         │              │                               │
         │              │  KPIs:                        │
         │              │  • goals, assists, xG, xA     │
         │              │  • pass_accuracy              │
         │              │  • defensive_index            │
         │              │  • player_rating              │
         │              │  • performance_score          │
         │              │  • distance_covered_km        │
         │              │  • top_speed_kmh              │
         │              │  • clutch_performance_score   │
         │              └─────────────┬─────────────────┘
         │                            │ many_to_one
         │                            ▼
         │               ┌────────────────────────┐
         └───────────────│      dim_stadiums       │
                         │  PK: stadium            │
                         │  16 rows                │
                         │  • City                 │
                         │  • Matches hosted       │
                         │  • Goals per match      │
                         └────────────────────────┘
```

---

## Datamart Files

| File | Rows | Grain | Description |
|---|---|---|---|
| `dm_performance/fact_performance.csv` | 54 600 | Player × Match | Central fact table — all KPIs |
| `dm_players/player_dim.csv` | 1 248 | Player | Profile, physical, market value, tournament totals |
| `dm_matches/match_dim.csv` | 1 050 | Match | Date, stage, stadium, aggregate match stats |
| `dm_teams/team_dim.csv` | 48 | Team | Squad profile, tournament record, avg stats |
| `dm_stadiums/stadium_dim.csv` | 16 | Stadium | Venue stats, goals per match, excitement index |

---

## Analytical Export Tables (for Looker Studio)

| Export CSV | Description |
|---|---|
| `top_scorers.csv` | Top 50 players by goals + xG overperformance |
| `agg_by_position.csv` | All KPIs averaged by playing position |
| `agg_by_stage.csv` | Stats evolution from group stage to final |
| `agg_team_attack.csv` | Attacking stats per team |
| `agg_team_defense.csv` | Defensive stats per team |
| `agg_physical.csv` | Physical performance by nationality & position |
| `agg_goalkeepers.csv` | Goalkeeper leaderboard |
| `knockout_performers.csv` | Top 30 KO-stage performers by clutch score |
| `agg_stadiums.csv` | Venue-level aggregates |
| `agg_age_performance.csv` | Performance by age group × position |

---

## Key Engineered Metrics

| Metric | Formula | Grain |
|---|---|---|
| `goal_involvement` | `goals + assists` | Per match |
| `shot_efficiency` | `goals / shots` | Per match |
| `defensive_index` | `tackles×1.5 + interceptions×1.5 + clearances + blocks×1.2 + recoveries×0.8` | Per match |
| `pass_completion_pct` | `pass_accuracy × 100` | Per match |
| `dribble_success_pct` | `successful_dribbles / dribbles_attempted × 100` | Per match |
| `km_per_minute` | `distance_covered_km / minutes_played` | Per match |
| `is_knockout` | `1 if stage_order >= 2` | Per match |
| `full_starter` | `1 if minutes_played >= 90` | Per match |
| `goal_diff` | `goals_team - goals_opponent` | Per match |
| `bmi` | `weight_kg / (height_cm/100)²` | Per player |
| `goal_involvement_tournament` | `total_goals_tournament + total_assists_tournament` | Per player |

---

## How to Load into DuckDB

```python
import duckdb
conn = duckdb.connect("fifa_wc2026.duckdb")

# Load all tables
tables = {
    "dim_players":      "data/datamarts/dm_players/player_dim.csv",
    "dim_matches":      "data/datamarts/dm_matches/match_dim.csv",
    "dim_teams":        "data/datamarts/dm_teams/team_dim.csv",
    "dim_stadiums":     "data/datamarts/dm_stadiums/stadium_dim.csv",
    "fact_performance": "data/datamarts/dm_performance/fact_performance.csv",
}
for table, path in tables.items():
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} AS
        SELECT * FROM read_csv_auto('{path}')
    """)
    print(f"Loaded {table}")

# Verify star schema
conn.execute("SELECT COUNT(*) FROM fact_performance").fetchone()
```

---

## How to Load into BigQuery

```python
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project="your-project")
dataset = "fifa_wc2026"

tables = {
    "dim_players":      "data/datamarts/dm_players/player_dim.csv",
    "dim_matches":      "data/datamarts/dm_matches/match_dim.csv",
    "dim_teams":        "data/datamarts/dm_teams/team_dim.csv",
    "dim_stadiums":     "data/datamarts/dm_stadiums/stadium_dim.csv",
    "fact_performance": "data/datamarts/dm_performance/fact_performance.csv",
}

for table_id, path in tables.items():
    df = pd.read_csv(path)
    job = client.load_table_from_dataframe(
        df,
        f"your-project.{dataset}.{table_id}",
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
    )
    job.result()
    print(f"Loaded {table_id}: {job.output_rows} rows")
```