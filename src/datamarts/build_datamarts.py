"""
build_datamarts.py
------------------
Builds the star-schema data warehouse from the processed fact table.

Architecture
────────────
fact_performance   (54 600 rows) — one row per player × match
  ├── dim_players  (1 248 rows)  — player profile & career attributes
  ├── dim_matches  (1 050 rows)  — match context & result
  ├── dim_teams    (  48 rows)   — national team attributes
  └── dim_stadiums (  16 rows)   — venue info

Each datamart also ships aggregated analytical tables for Looker.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)

PROCESSED_PATH = Path(__file__).parents[2] / "data" / "processed" / "wc2026_clean.csv"
DM_BASE        = Path(__file__).parents[2] / "data" / "datamarts"
EXPORTS_DIR    = Path(__file__).parents[2] / "data" / "exports"


def load_processed() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_PATH, parse_dates=["match_date"])
    return df


# ══════════════════════════════════════════════════════════════════════════════
# DIMENSION TABLES
# ══════════════════════════════════════════════════════════════════════════════

def build_dim_players(df: pd.DataFrame) -> pd.DataFrame:
    """
    dim_players — one row per player_id.
    Includes profile, physical attributes, market value, and tournament totals.
    """
    log.info("Building dim_players …")
    dim = (
        df.sort_values("total_minutes_tournament", ascending=False)
        .drop_duplicates(subset=["player_id"])
        [[
            "player_id", "player_name", "age", "age_group", "nationality",
            "team", "jersey_number", "position", "height_cm", "weight_kg",
            "preferred_foot", "club_name", "market_value_eur", "market_value_tier",
            # Tournament career totals (same per player across rows)
            "total_goals_tournament", "total_assists_tournament",
            "total_minutes_tournament", "player_of_match_awards", "tournament_rating",
        ]]
        .copy()
    )
    dim["goal_involvement_tournament"] = (
        dim["total_goals_tournament"] + dim["total_assists_tournament"]
    )
    dim["bmi"] = (
        dim["weight_kg"] / ((dim["height_cm"] / 100) ** 2)
    ).round(1)
    log.info(f"  → {len(dim):,} players")
    return dim


def build_dim_matches(df: pd.DataFrame) -> pd.DataFrame:
    """
    dim_matches — one row per match_id.
    Includes date, stadium, city, teams, stage, and result context.
    """
    log.info("Building dim_matches …")
    # Build from one side of each match
    match_cols = [
        "match_id", "match_date", "stadium", "city",
        "tournament_stage", "stage_order", "match_month", "match_dow",
        "is_knockout",
    ]
    dim = df[match_cols].drop_duplicates(subset=["match_id"]).copy()

    # Add aggregate match stats
    match_agg = (
        df.groupby("match_id")
        .agg(
            total_goals_in_match=("goals", "sum"),
            total_shots=("shots", "sum"),
            total_cards=("yellow_cards", "sum"),
            avg_player_rating=("player_rating", "mean"),
            avg_distance_covered=("distance_covered_km", "mean"),
            players_in_match=("player_id", "nunique"),
        )
        .round(2)
        .reset_index()
    )
    dim = dim.merge(match_agg, on="match_id", how="left")
    log.info(f"  → {len(dim):,} matches")
    return dim


def build_dim_teams(df: pd.DataFrame) -> pd.DataFrame:
    """
    dim_teams — one row per team.
    Includes squad profile, tournament performance, and physical averages.
    """
    log.info("Building dim_teams …")
    dim = (
        df.groupby("team")
        .agg(
            nationality=("nationality", "first"),
            squad_size=("player_id", "nunique"),
            avg_age=("age", "mean"),
            avg_height_cm=("height_cm", "mean"),
            avg_weight_kg=("weight_kg", "mean"),
            avg_market_value_eur=("market_value_eur", "mean"),
            total_market_value_eur=("market_value_eur", lambda x: x.drop_duplicates().sum()),
            matches_played=("match_id", "nunique"),
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            total_shots=("shots", "sum"),
            avg_pass_accuracy=("pass_accuracy", "mean"),
            total_yellow_cards=("yellow_cards", "sum"),
            total_red_cards=("red_cards", "sum"),
            avg_player_rating=("player_rating", "mean"),
            avg_performance_score=("performance_score", "mean"),
            avg_distance_covered=("distance_covered_km", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            wins=("match_result", lambda x: (x == "W").sum()),
            draws=("match_result", lambda x: (x == "D").sum()),
            losses=("match_result", lambda x: (x == "L").sum()),
        )
        .round(2)
        .reset_index()
    )
    dim["win_rate"] = (dim["wins"] / dim["matches_played"] * 100).round(1)
    dim["goals_per_match"] = (dim["total_goals"] / dim["matches_played"]).round(2)
    log.info(f"  → {len(dim):,} teams")
    return dim


def build_dim_stadiums(df: pd.DataFrame) -> pd.DataFrame:
    """
    dim_stadiums — one row per stadium.
    Includes city, matches hosted, and aggregate performance stats.
    """
    log.info("Building dim_stadiums …")
    dim = (
        df.groupby(["stadium", "city"])
        .agg(
            matches_hosted=("match_id", "nunique"),
            total_goals_scored=("goals", "sum"),
            avg_player_rating=("player_rating", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            avg_distance_covered=("distance_covered_km", "mean"),
            total_yellow_cards=("yellow_cards", "sum"),
            total_red_cards=("red_cards", "sum"),
            unique_teams=("team", "nunique"),
        )
        .round(2)
        .reset_index()
    )
    dim["goals_per_match"] = (
        dim["total_goals_scored"] / dim["matches_hosted"]
    ).round(2)
    log.info(f"  → {len(dim):,} stadiums")
    return dim


def build_fact_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    fact_performance — the central fact table (grain: player × match).
    Contains all KPIs and foreign keys to dimensions.
    """
    log.info("Building fact_performance …")
    fact_cols = [
        # Keys
        "player_id", "match_id", "team",
        # Context
        "tournament_stage", "stage_order", "match_result", "is_knockout",
        "minutes_played", "full_starter",
        # Attacking
        "goals", "assists", "shots", "shots_on_target",
        "expected_goals_xg", "expected_assists_xa", "key_passes",
        "goal_involvement", "shot_efficiency",
        # Passing
        "total_passes", "successful_passes", "pass_accuracy",
        "pass_completion_pct", "crosses", "successful_crosses",
        "dribbles_attempted", "successful_dribbles", "dribble_success_pct",
        # Defensive
        "tackles", "interceptions", "clearances", "blocks",
        "aerial_duels_won", "aerial_duels_lost", "recoveries",
        "defensive_actions", "defensive_index",
        # Discipline
        "yellow_cards", "red_cards", "fouls_committed", "fouls_suffered", "offsides",
        # Goalkeeper
        "saves", "save_percentage", "clean_sheet", "goals_conceded", "penalty_saves",
        # Physical
        "distance_covered_km", "sprint_distance_km", "top_speed_kmh",
        "accelerations", "decelerations", "stamina_score",
        "km_per_minute",
        # Composite scores
        "player_rating", "rating_tier", "performance_score",
        "offensive_contribution", "defensive_contribution",
        "possession_impact", "pressure_resistance",
        "creativity_score", "consistency_score", "clutch_performance_score",
    ]
    fact = df[[c for c in fact_cols if c in df.columns]].copy()
    log.info(f"  → {len(fact):,} rows, {len(fact.columns)} columns")
    return fact


# ══════════════════════════════════════════════════════════════════════════════
# ANALYTICAL EXPORT TABLES (for Looker)
# ══════════════════════════════════════════════════════════════════════════════

def build_exports(df: pd.DataFrame) -> dict:
    """Build aggregated tables ready to import into Looker Studio."""
    exports = {}

    # 1. Top scorers (tournament level)
    exports["top_scorers"] = (
        df.groupby(["player_id", "player_name", "team", "position", "nationality"])
        .agg(
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            goal_involvement=("goal_involvement", "sum"),
            xg=("expected_goals_xg", "sum"),
            shots=("shots", "sum"),
            matches=("match_id", "nunique"),
            avg_rating=("player_rating", "mean"),
            minutes=("minutes_played", "sum"),
        )
        .round(2).reset_index()
        .sort_values("goals", ascending=False)
        .head(50)
    )

    # 2. Performance by position
    exports["agg_by_position"] = (
        df.groupby("position")
        .agg(
            player_count=("player_id", "nunique"),
            avg_rating=("player_rating", "mean"),
            avg_goals=("goals", "mean"),
            avg_assists=("assists", "mean"),
            avg_pass_acc=("pass_accuracy", "mean"),
            avg_distance=("distance_covered_km", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            avg_defensive_index=("defensive_index", "mean"),
            avg_offensive_contribution=("offensive_contribution", "mean"),
            avg_defensive_contribution=("defensive_contribution", "mean"),
        )
        .round(3).reset_index()
    )

    # 3. Performance by tournament stage
    exports["agg_by_stage"] = (
        df.groupby(["tournament_stage", "stage_order"])
        .agg(
            total_goals=("goals", "sum"),
            avg_goals_per_player=("goals", "mean"),
            avg_rating=("player_rating", "mean"),
            avg_performance=("performance_score", "mean"),
            avg_distance=("distance_covered_km", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
            total_shots=("shots", "sum"),
        )
        .round(2).reset_index()
        .sort_values("stage_order")
    )

    # 4. Team attacking stats
    exports["agg_team_attack"] = (
        df.groupby("team")
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            total_shots=("shots", "sum"),
            total_shots_on_target=("shots_on_target", "sum"),
            total_xg=("expected_goals_xg", "sum"),
            avg_offensive_contribution=("offensive_contribution", "mean"),
            avg_creativity=("creativity_score", "mean"),
        )
        .round(2).reset_index()
        .sort_values("total_goals", ascending=False)
    )

    # 5. Team defensive stats
    exports["agg_team_defense"] = (
        df.groupby("team")
        .agg(
            total_tackles=("tackles", "sum"),
            total_interceptions=("interceptions", "sum"),
            total_clearances=("clearances", "sum"),
            total_blocks=("blocks", "sum"),
            avg_defensive_contribution=("defensive_contribution", "mean"),
            avg_defensive_index=("defensive_index", "mean"),
            total_yellow_cards=("yellow_cards", "sum"),
            total_red_cards=("red_cards", "sum"),
            goals_conceded=("goals_conceded", "sum"),
        )
        .round(2).reset_index()
        .sort_values("avg_defensive_index", ascending=False)
    )

    # 6. Physical performance by nationality
    exports["agg_physical"] = (
        df.groupby(["nationality", "position"])
        .agg(
            avg_distance=("distance_covered_km", "mean"),
            avg_sprint_distance=("sprint_distance_km", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            avg_stamina=("stamina_score", "mean"),
            avg_accelerations=("accelerations", "mean"),
        )
        .round(2).reset_index()
    )

    # 7. Goalkeeper stats
    exports["agg_goalkeepers"] = (
        df[df["position"] == "Goalkeeper"]
        .groupby(["player_id", "player_name", "team"])
        .agg(
            matches=("match_id", "nunique"),
            total_saves=("saves", "sum"),
            avg_save_pct=("save_percentage", "mean"),
            clean_sheets=("clean_sheet", "sum"),
            goals_conceded=("goals_conceded", "sum"),
            penalty_saves=("penalty_saves", "sum"),
            avg_rating=("player_rating", "mean"),
        )
        .round(2).reset_index()
        .sort_values("total_saves", ascending=False)
    )

    # 8. Knockout stage performers
    exports["knockout_performers"] = (
        df[df["is_knockout"] == 1]
        .groupby(["player_id", "player_name", "team", "position"])
        .agg(
            matches=("match_id", "nunique"),
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            avg_clutch=("clutch_performance_score", "mean"),
            avg_rating=("player_rating", "mean"),
            avg_pressure_resistance=("pressure_resistance", "mean"),
        )
        .round(2).reset_index()
        .sort_values("avg_clutch", ascending=False)
        .head(30)
    )

    # 9. Stadium analysis
    exports["agg_stadiums"] = (
        df.groupby(["stadium", "city"])
        .agg(
            matches_hosted=("match_id", "nunique"),
            total_goals=("goals", "sum"),
            avg_player_rating=("player_rating", "mean"),
            avg_distance_covered=("distance_covered_km", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            total_yellow_cards=("yellow_cards", "sum"),
        )
        .round(2).reset_index()
        .sort_values("total_goals", ascending=False)
    )

    # 10. Age group vs performance
    exports["agg_age_performance"] = (
        df.groupby(["age_group", "position"], observed=True)
        .agg(
            player_count=("player_id", "nunique"),
            avg_rating=("player_rating", "mean"),
            avg_goals=("goals", "mean"),
            avg_distance=("distance_covered_km", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            avg_stamina=("stamina_score", "mean"),
            avg_market_value=("market_value_eur", "mean"),
        )
        .round(2).reset_index()
    )

    return exports


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def run_all() -> None:
    df = load_processed()

    # ── Dimensions ────────────────────────────────────────────────────────────
    dimensions = {
        "dm_players/player_dim.csv":    build_dim_players(df),
        "dm_matches/match_dim.csv":     build_dim_matches(df),
        "dm_teams/team_dim.csv":        build_dim_teams(df),
        "dm_stadiums/stadium_dim.csv":  build_dim_stadiums(df),
        "dm_performance/fact_performance.csv": build_fact_performance(df),
    }

    for rel_path, table in dimensions.items():
        out = DM_BASE / rel_path
        out.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(out, index=False)
        log.info(f"Saved datamart → {out}  ({len(table):,} rows)")

    # ── Export tables for Looker ───────────────────────────────────────────────
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    exports = build_exports(df)
    for fname, table in exports.items():
        out = EXPORTS_DIR / f"{fname}.csv"
        table.to_csv(out, index=False)
        log.info(f"Exported {fname}.csv ({len(table)} rows)")

    print("\n" + "=" * 50)
    print("⚽  DATAMART BUILD SUMMARY")
    print("=" * 50)
    print(f"Fact rows:      {len(df):>10,}")
    print(f"Players:        {df['player_id'].nunique():>10,}")
    print(f"Matches:        {df['match_id'].nunique():>10,}")
    print(f"Teams:          {df['team'].nunique():>10,}")
    print(f"Stadiums:       {df['stadium'].nunique():>10,}")
    print(f"Datamarts:      {len(dimensions):>10}")
    print(f"Export tables:  {len(exports):>10}")


if __name__ == "__main__":
    run_all()