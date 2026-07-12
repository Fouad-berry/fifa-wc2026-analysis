"""
build_datamarts.py
------------------
Builds the star-schema data warehouse from the processed fact table.

Architecture
────────────
fact_performance   (54 600 rows) — one row per player x match
  ├── dim_players  (1 248 rows)  — player profile & career attributes
  ├── dim_matches  (1 050 rows)  — match context & result
  ├── dim_teams    (  48 rows)   — national team attributes
  └── dim_stadiums (  16 rows)   — venue info

Each datamart also ships aggregated analytical tables for Looker.
"""

import logging

import pandas as pd
from rich.console import Console

from src.logging_config import get_console, get_progress, setup_logging
from src.paths import DM_BASE, EXPORTS_DIR, PROCESSED_PATH

log: logging.Logger = logging.getLogger(__name__)
console: Console = get_console()


def load_processed() -> pd.DataFrame:
    if not PROCESSED_PATH.exists():
        raise FileNotFoundError(
            f"Processed file not found at {PROCESSED_PATH}. "
            "Run 'python src/transformation/clean_transform.py' first."
        )
    return pd.read_csv(PROCESSED_PATH, parse_dates=["match_date"])


# ── DIMENSION TABLES ────────────────────────────────────────────────────────


def build_dim_players(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Building dim_players [yellow]…[/]")
    dim = (
        df.sort_values(["total_minutes_tournament", "match_date"], ascending=[False, False])
        .drop_duplicates(subset=["player_id"])[
            [
                "player_id",
                "player_name",
                "age",
                "age_group",
                "nationality",
                "team",
                "jersey_number",
                "position",
                "height_cm",
                "weight_kg",
                "preferred_foot",
                "club_name",
                "market_value_eur",
                "market_value_tier",
                "total_goals_tournament",
                "total_assists_tournament",
                "total_minutes_tournament",
                "player_of_match_awards",
                "tournament_rating",
            ]
        ]
        .copy()
    )
    dim["goal_involvement_tournament"] = (
        dim["total_goals_tournament"] + dim["total_assists_tournament"]
    )
    dim["bmi"] = (dim["weight_kg"] / ((dim["height_cm"] / 100) ** 2)).round(1)
    log.info("  [green]→ %s players[/]", f"{len(dim):,}")
    return dim


def build_dim_matches(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Building dim_matches [yellow]…[/]")
    match_cols = [
        "match_id",
        "match_date",
        "stadium",
        "city",
        "tournament_stage",
        "stage_order",
        "match_month",
        "match_dow",
        "is_knockout",
    ]
    dim = df[match_cols].drop_duplicates(subset=["match_id"]).copy()

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
    log.info("  [green]%s matches[/]", f"{len(dim):,}")
    return dim


def build_dim_teams(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Building dim_teams [yellow]…[/]")
    dim = (
        df.groupby("team")
        .agg(
            nationality=("nationality", "first"),
            squad_size=("player_id", "nunique"),
            avg_age=("age", "mean"),
            avg_height_cm=("height_cm", "mean"),
            avg_weight_kg=("weight_kg", "mean"),
            avg_market_value_eur=("market_value_eur", "mean"),
            total_market_value_eur=("market_value_eur", "sum"),
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
    log.info("  [green]%s teams[/]", f"{len(dim):,}")
    return dim


def build_dim_stadiums(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Building dim_stadiums [yellow]…[/]")
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
    dim["goals_per_match"] = (dim["total_goals_scored"] / dim["matches_hosted"]).round(2)
    log.info("  [green]%s stadiums[/]", f"{len(dim):,}")
    return dim


def build_fact_performance(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Building fact_performance [yellow]…[/]")
    fact_cols = [
        "player_id",
        "match_id",
        "team",
        "tournament_stage",
        "stage_order",
        "match_result",
        "is_knockout",
        "minutes_played",
        "full_starter",
        "goals",
        "assists",
        "shots",
        "shots_on_target",
        "expected_goals_xg",
        "expected_assists_xa",
        "key_passes",
        "goal_involvement",
        "goal_diff",
        "shot_efficiency",
        "total_passes",
        "successful_passes",
        "pass_accuracy",
        "pass_completion_pct",
        "crosses",
        "successful_crosses",
        "dribbles_attempted",
        "successful_dribbles",
        "dribble_success_pct",
        "tackles",
        "interceptions",
        "clearances",
        "blocks",
        "aerial_duels_won",
        "aerial_duels_lost",
        "recoveries",
        "defensive_actions",
        "defensive_index",
        "yellow_cards",
        "red_cards",
        "fouls_committed",
        "fouls_suffered",
        "offsides",
        "saves",
        "save_percentage",
        "clean_sheet",
        "goals_conceded",
        "penalty_saves",
        "distance_covered_km",
        "sprint_distance_km",
        "top_speed_kmh",
        "accelerations",
        "decelerations",
        "stamina_score",
        "km_per_minute",
        "player_rating",
        "rating_tier",
        "performance_score",
        "offensive_contribution",
        "defensive_contribution",
        "possession_impact",
        "pressure_resistance",
        "creativity_score",
        "consistency_score",
        "clutch_performance_score",
    ]
    fact = df[[c for c in fact_cols if c in df.columns]].copy()
    log.info("  [green]%s[/] rows, [green]%s[/] columns", f"{len(fact):,}", len(fact.columns))
    return fact


# ── ANALYTICAL EXPORT TABLES ────────────────────────────────────────────────


TOP_SCORERS_LIMIT: int = 50
KNOCKOUT_LIMIT: int = 30


def build_exports(df: pd.DataFrame) -> dict:
    log.info("Building export tables [yellow]…[/]")
    exports = {}

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
        .round(2)
        .reset_index()
        .sort_values("goals", ascending=False)
        .head(TOP_SCORERS_LIMIT)
    )

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
        .round(3)
        .reset_index()
    )

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
        .round(2)
        .reset_index()
        .sort_values("stage_order")
    )

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
        .round(2)
        .reset_index()
        .sort_values("total_goals", ascending=False)
    )

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
        .round(2)
        .reset_index()
        .sort_values("avg_defensive_index", ascending=False)
    )

    exports["agg_physical"] = (
        df.groupby(["nationality", "position"])
        .agg(
            avg_distance=("distance_covered_km", "mean"),
            avg_sprint_distance=("sprint_distance_km", "mean"),
            avg_top_speed=("top_speed_kmh", "mean"),
            avg_stamina=("stamina_score", "mean"),
            avg_accelerations=("accelerations", "mean"),
        )
        .round(2)
        .reset_index()
    )

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
        .round(2)
        .reset_index()
        .sort_values("total_saves", ascending=False)
    )

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
        .round(2)
        .reset_index()
        .sort_values("avg_clutch", ascending=False)
        .head(KNOCKOUT_LIMIT)
    )

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
        .round(2)
        .reset_index()
        .sort_values("total_goals", ascending=False)
    )

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
        .round(2)
        .reset_index()
    )

    log.info("Export tables done [green]OK[/]")
    return exports


# ── MAIN ────────────────────────────────────────────────────────────────────


def run_all() -> dict:
    progress = get_progress()
    task = progress.add_task("Building datamarts …", total=6)
    with progress:
        df = load_processed()
        progress.update(task, advance=1)

        dimensions = {
            "dm_players/player_dim.csv": build_dim_players(df),
            "dm_matches/match_dim.csv": build_dim_matches(df),
            "dm_teams/team_dim.csv": build_dim_teams(df),
            "dm_stadiums/stadium_dim.csv": build_dim_stadiums(df),
            "dm_performance/fact_performance.csv": build_fact_performance(df),
        }
        progress.update(task, advance=3)

        for rel_path, table in dimensions.items():
            out = DM_BASE / rel_path
            out.parent.mkdir(parents=True, exist_ok=True)
            table.to_csv(out, index=False)
        progress.update(task, advance=1)

        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        exports = build_exports(df)
        for fname, table in exports.items():
            out = EXPORTS_DIR / f"{fname}.csv"
            table.to_csv(out, index=False)
        progress.update(task, advance=1)

    console.print("\n" + "=" * 50)
    console.print("⚽  DATAMART BUILD SUMMARY")
    console.print("=" * 50)
    console.print(f"Fact rows:      {len(df):>10,}")
    console.print(f"Players:        {df['player_id'].nunique():>10,}")
    console.print(f"Matches:        {df['match_id'].nunique():>10,}")
    console.print(f"Teams:          {df['team'].nunique():>10,}")
    console.print(f"Stadiums:       {df['stadium'].nunique():>10,}")
    console.print(f"Datamarts:      {len(dimensions):>10}")
    console.print(f"Export tables:  {len(exports):>10}")

    return {
        "fact_rows": len(df),
        "players": int(df["player_id"].nunique()),
        "matches": int(df["match_id"].nunique()),
        "teams": int(df["team"].nunique()),
        "stadiums": int(df["stadium"].nunique()),
        "datamarts": len(dimensions),
        "export_tables": len(exports),
    }


if __name__ == "__main__":
    setup_logging()
    run_all()
