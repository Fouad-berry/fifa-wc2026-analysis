"""
load_data.py
------------
Load and validate the raw FIFA World Cup 2026 player performance CSV.
"""

import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)

RAW_PATH = Path(__file__).parents[2] / "data" / "raw" / "fifa_wc2026_player_performance.csv"

VALID_POSITIONS     = {"Goalkeeper", "Defender", "Midfielder", "Forward"}
VALID_FEET          = {"Left", "Right"}
VALID_STAGES        = {"Group Stage", "Round of 32", "Round of 16",
                       "Quarter Finals", "Semi Finals", "Third Place Match", "Final"}
VALID_RESULTS       = {"W", "L", "D"}

NUMERIC_COLS = [
    "age", "jersey_number", "height_cm", "weight_kg", "market_value_eur",
    "goals_team", "goals_opponent", "minutes_played", "goals", "assists",
    "shots", "shots_on_target", "expected_goals_xg", "expected_assists_xa",
    "key_passes", "successful_passes", "total_passes", "pass_accuracy",
    "dribbles_attempted", "successful_dribbles", "crosses", "successful_crosses",
    "tackles", "interceptions", "clearances", "blocks", "aerial_duels_won",
    "aerial_duels_lost", "recoveries", "defensive_actions", "fouls_committed",
    "fouls_suffered", "yellow_cards", "red_cards", "offsides", "saves",
    "save_percentage", "punches", "clean_sheet", "goals_conceded", "penalty_saves",
    "distance_covered_km", "sprint_distance_km", "top_speed_kmh",
    "accelerations", "decelerations", "stamina_score", "player_rating",
    "performance_score", "offensive_contribution", "defensive_contribution",
    "possession_impact", "pressure_resistance", "creativity_score",
    "consistency_score", "clutch_performance_score", "total_goals_tournament",
    "total_assists_tournament", "total_minutes_tournament",
    "player_of_match_awards", "tournament_rating",
]


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    log.info(f"Loading {path}")
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # Cast numerics
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse date
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")

    log.info(f"Loaded {len(df):,} rows × {len(df.columns)} columns")
    _validate(df)
    return df


def _validate(df: pd.DataFrame) -> None:
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        log.warning(f"Null values detected:\n{nulls}")

    bad_pos = (~df["position"].isin(VALID_POSITIONS)).sum()
    if bad_pos:
        log.warning(f"{bad_pos} unexpected positions")

    bad_stage = (~df["tournament_stage"].isin(VALID_STAGES)).sum()
    if bad_stage:
        log.warning(f"{bad_stage} unexpected tournament stages")

    bad_result = (~df["match_result"].isin(VALID_RESULTS)).sum()
    if bad_result:
        log.warning(f"{bad_result} unexpected match results")

    log.info("Validation complete ✓")


if __name__ == "__main__":
    df = load_raw()
    print(df.shape)
    print(df.dtypes)