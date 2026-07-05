# Looker Studio Setup Guide

---

## Option A — Looker Studio (free, via Google Sheets)

### 1. Run the full pipeline

```bash
python src/transformation/clean_transform.py
python src/datamarts/build_datamarts.py
python src/analysis/metrics.py
```

### 2. Upload to Google Drive

Upload these files from `data/exports/` and `data/datamarts/`:

| File | Use in dashboard |
|---|---|
| `top_scorers.csv` | Player Performance — top scorers table |
| `agg_by_position.csv` | Player Performance — position comparison |
| `agg_by_stage.csv` | Tournament progression charts |
| `agg_team_attack.csv` | Team Overview — attacking stats |
| `agg_team_defense.csv` | Team Overview — defensive stats |
| `agg_physical.csv` | Physical stats by nationality |
| `agg_goalkeepers.csv` | Goalkeeper leaderboard |
| `knockout_performers.csv` | KO stage clutch performers |
| `agg_stadiums.csv` | Stadium analysis |
| `agg_age_performance.csv` | Age group × position matrix |
| `dm_teams/team_dim.csv` | Full team stats |
| `dm_stadiums/stadium_dim.csv` | Stadium dimension |

### 3. Suggested dashboard pages

| Page | Primary source | Key charts |
|---|---|---|
| 🏆 Tournament Overview | `agg_by_stage.csv` | Goals/stage line, rating progression, cards bar |
| 👤 Player Performance | `top_scorers.csv` | Ranked table, xG vs goals scatter |
| 🌍 Team Analysis | `agg_team_attack.csv` + `agg_team_defense.csv` | Goals bar, pass accuracy, defensive index |
| 🏟️ Stadiums | `agg_stadiums.csv` | Goals/match bar, geo map by city |
| ⚡ Physical Stats | `agg_physical.csv` | Speed/distance by nationality heatmap |
| 🥅 Goalkeepers | `agg_goalkeepers.csv` | Save % leaderboard, clean sheets bar |
| 🎯 Knockout Heroes | `knockout_performers.csv` | Clutch score ranking |

---

## Option B — Looker (enterprise) via BigQuery

### 1. Load all datamart tables

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
        df, f"your-project.{dataset}.{table_id}",
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
    )
    job.result()
    print(f"✓ {table_id}: {job.output_rows:,} rows")
```

### 2. Connect Looker
- Looker Admin → Connections → New → BigQuery
- Set connection name to `fifa_wc2026_bq` (matches the `.model.lkml`)
- Deploy `looker/` folder to your Looker project repository
- The `fifa_explore.lkml` automatically joins 3 dimensions (players, matches, teams) to the fact table; stadiums have a separate explore

---

## Key Metrics Reference

| Metric | Formula |
|---|---|
| Total goals | SUM(goals) |
| xG overperformance | SUM(goals) − SUM(xG) |
| Defensive index | tackles×1.5 + interceptions×1.5 + clearances + blocks×1.2 + recoveries×0.8 |
| Clutch score | AVG(clutch_performance_score) |
| Pass completion % | AVG(pass_completion_pct) |
| Goals per match | SUM(goals) / COUNT(DISTINCT match_id) |
| Win rate | wins / matches_played × 100 |
| Shot efficiency | goals / shots |
| Distance per minute | distance_covered_km / minutes_played |