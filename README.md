# ⚽ FIFA World Cup 2026 — Player Performance Analysis

End-to-end data analysis pipeline on 54 600 player-match records from the FIFA World Cup 2026, covering 1 248 players across 1 050 matches and 48 nations. Includes a full star-schema data warehouse with 5 datamarts, SQL analytics, and Looker Studio dashboards.

---

## 📁 Project Structure

```
fifa-wc2026-analysis/
│
├── data/
│   ├── raw/                                        # Original CSV (do not modify)
│   ├── processed/                                  # Cleaned & enriched fact table
│   ├── exports/                                    # Aggregated CSVs for Looker
│   └── datamarts/
│       ├── dm_players/      player_dim.csv         # Player dimension
│       ├── dm_matches/      match_dim.csv          # Match dimension
│       ├── dm_teams/        team_dim.csv           # Team dimension
│       ├── dm_stadiums/     stadium_dim.csv        # Stadium dimension
│       └── dm_performance/  fact_performance.csv   # Central fact table
│
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning.ipynb
│   └── 03_analysis.ipynb
│
├── sql/
│   ├── ddl/
│   │   ├── create_dimensions.sql
│   │   └── create_fact.sql
│   └── queries/
│       ├── top_scorers.sql
│       ├── team_performance.sql
│       ├── position_analysis.sql
│       ├── stadium_analysis.sql
│       └── tournament_progression.sql
│
├── src/
│   ├── ingestion/load_data.py
│   ├── transformation/clean_transform.py
│   ├── datamarts/build_datamarts.py          # ★ Star-schema builder
│   └── analysis/metrics.py
│
├── looker/
│   ├── models/fifa_wc2026.model.lkml
│   ├── views/                                # One view per datamart
│   ├── explores/fifa_explore.lkml
│   └── dashboards/
│       ├── player_performance.dashboard.lookml
│       └── team_overview.dashboard.lookml
│
├── docs/
│   ├── data_dictionary.md
│   ├── datamart_architecture.md              # Star schema documentation
│   └── looker_setup.md
│
├── .github/workflows/ci.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🗂️ Dataset

**File:** `data/raw/fifa_wc2026_player_performance.csv`
**Rows:** 54 600 | **Columns:** 75
**Coverage:** 1 248 players · 1 050 matches · 48 nations · 16 stadiums · 7 tournament stages

### Key column groups

| Group | Columns |
|---|---|
| Player profile | `player_id`, `player_name`, `age`, `nationality`, `position`, `preferred_foot`, `club_name`, `market_value_eur` |
| Match context | `match_id`, `match_date`, `stadium`, `city`, `opponent_team`, `tournament_stage`, `match_result` |
| Attacking | `goals`, `assists`, `shots`, `shots_on_target`, `expected_goals_xg`, `expected_assists_xa`, `key_passes` |
| Passing | `total_passes`, `successful_passes`, `pass_accuracy`, `crosses`, `successful_crosses` |
| Defensive | `tackles`, `interceptions`, `clearances`, `blocks`, `aerial_duels_won`, `recoveries` |
| Discipline | `yellow_cards`, `red_cards`, `fouls_committed`, `fouls_suffered`, `offsides` |
| Goalkeeper | `saves`, `save_percentage`, `clean_sheet`, `goals_conceded`, `penalty_saves` |
| Physical | `distance_covered_km`, `sprint_distance_km`, `top_speed_kmh`, `stamina_score` |
| Composite scores | `player_rating`, `performance_score`, `offensive_contribution`, `defensive_contribution`, `creativity_score`, `clutch_performance_score` |
| Tournament totals | `total_goals_tournament`, `total_assists_tournament`, `total_minutes_tournament`, `tournament_rating` |

---

## ⭐ Data Architecture — Star Schema

```
                    ┌──────────────────┐
                    │  dim_players     │
                    │  (1 248 rows)    │
                    └────────┬─────────┘
                             │
┌──────────────┐    ┌────────▼─────────┐    ┌──────────────────┐
│  dim_matches │────│  fact_performance│────│   dim_teams      │
│ (1 050 rows) │    │  (54 600 rows)   │    │   (48 rows)      │
└──────────────┘    └────────┬─────────┘    └──────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  dim_stadiums    │
                    │  (16 rows)       │
                    └──────────────────┘
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/<your-username>/fifa-wc2026-analysis.git
cd fifa-wc2026-analysis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run full pipeline (clean → datamarts → exports)
python src/transformation/clean_transform.py
python src/datamarts/build_datamarts.py
python src/analysis/metrics.py

jupyter lab
```

---

## 📊 Looker Studio Dashboards

| Dashboard | Key charts |
|---|---|
| 🏆 Tournament Overview | Goals per stage, top scorers, match results |
| 👤 Player Performance | Rating heatmap, top performers by position |
| 🌍 Team Analysis | Team goals, cards, possession, passing accuracy |
| 🏟️ Stadium Analysis | Goals per stadium, attendance cities |
| ⚡ Physical Stats | Speed, distance, stamina by nationality |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11 |
| Data manipulation | pandas, numpy |
| Visualisation | matplotlib, seaborn, plotly |
| SQL | DuckDB (local) / BigQuery (cloud) |
| BI | Looker Studio |
| CI | GitHub Actions |

---

## 📄 License

Réalisé par Fouad MOUTAIROU
Portfolio : https://portfolio-fouad.netlify.app/

MIT