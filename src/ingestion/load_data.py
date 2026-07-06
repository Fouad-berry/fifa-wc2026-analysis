"""
load_data.py
------------
Load and validate the raw FIFA World Cup 2026 player performance CSV.
"""

import logging

import pandas as pd

from src.logging_config import setup_logging
from src.paths import RAW_PATH

log = logging.getLogger(__name__)

VALID_POSITIONS = {"Goalkeeper", "Defender", "Midfielder", "Forward"}
VALID_FEET = {"Left", "Right"}
VALID_STAGES = {
    "Group Stage",
    "Round of 32",
    "Round of 16",
    "Quarter Finals",
    "Semi Finals",
    "Third Place Match",
    "Final",
}
VALID_RESULTS = {"W", "L", "D"}

NUMERIC_COLS = [
    "age",
    "jersey_number",
    "height_cm",
    "weight_kg",
    "market_value_eur",
    "goals_team",
    "goals_opponent",
    "minutes_played",
    "goals",
    "assists",
    "shots",
    "shots_on_target",
    "expected_goals_xg",
    "expected_assists_xa",
    "key_passes",
    "successful_passes",
    "total_passes",
    "pass_accuracy",
    "dribbles_attempted",
    "successful_dribbles",
    "crosses",
    "successful_crosses",
    "tackles",
    "interceptions",
    "clearances",
    "blocks",
    "aerial_duels_won",
    "aerial_duels_lost",
    "recoveries",
    "defensive_actions",
    "fouls_committed",
    "fouls_suffered",
    "yellow_cards",
    "red_cards",
    "offsides",
    "saves",
    "save_percentage",
    "punches",
    "clean_sheet",
    "goals_conceded",
    "penalty_saves",
    "distance_covered_km",
    "sprint_distance_km",
    "top_speed_kmh",
    "accelerations",
    "decelerations",
    "stamina_score",
    "player_rating",
    "performance_score",
    "offensive_contribution",
    "defensive_contribution",
    "possession_impact",
    "pressure_resistance",
    "creativity_score",
    "consistency_score",
    "clutch_performance_score",
    "total_goals_tournament",
    "total_assists_tournament",
    "total_minutes_tournament",
    "player_of_match_awards",
    "tournament_rating",
]


def load_raw(path: str | None = None) -> pd.DataFrame:
    if path is None:
        path = str(RAW_PATH)
    log.info("Loading [cyan]%s[/]", path)
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    for col in NUMERIC_COLS:
        if col in df.columns:
            before = df[col].isna().sum()
            df[col] = pd.to_numeric(df[col], errors="coerce")
            after = df[col].isna().sum()
            coerced = after - before
            if coerced:
                log.warning("[yellow]%s[/] values coerced to NaN in [cyan]%s[/]", coerced, col)

    before = df["match_date"].isna().sum()
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    after = df["match_date"].isna().sum()
    if after - before:
        log.warning("[yellow]%s[/] dates coerced to NaT", after - before)

    log.info("Loaded [bold]%s[/] rows x [bold]%s[/] columns", f"{len(df):,}", len(df.columns))
    n_issues = validate(df)
    if n_issues:
        plural = "" if n_issues == 1 else "s"
        log.warning("[yellow]Validation reported %s issue%s[/]", n_issues, plural)
    return df


def validate(df: pd.DataFrame) -> int:
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        log.warning("Null values detected:\n%s", nulls)

    positions = df["position"].dropna()
    bad_pos = 0
    if len(positions) > 0:
        bad_pos = int((~positions.isin(VALID_POSITIONS)).sum())
        if bad_pos:
            log.warning("[yellow]%s[/] unexpected positions", bad_pos)

    stages = df["tournament_stage"].dropna()
    bad_stage = 0
    if len(stages) > 0:
        bad_stage = int((~stages.isin(VALID_STAGES)).sum())
        if bad_stage:
            log.warning("[yellow]%s[/] unexpected tournament stages", bad_stage)

    results = df["match_result"].dropna()
    bad_result = 0
    if len(results) > 0:
        bad_result = int((~results.isin(VALID_RESULTS)).sum())
        if bad_result:
            log.warning("[yellow]%s[/] unexpected match results", bad_result)

    total = bad_pos + bad_stage + bad_result
    log.info(
        "Validation complete — [yellow]%s[/] issue%s found",
        total,
        "" if total == 1 else "s",
    )
    return total


if __name__ == "__main__":
    setup_logging()
    df = load_raw()
    log.info("Shape: %s", df.shape)
    log.info("Dtypes:\n%s", df.dtypes)
