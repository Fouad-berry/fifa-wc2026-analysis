"""
clean_transform.py
------------------
Clean and feature-engineer the FIFA WC 2026 dataset.
Produces the enriched fact table used by all datamarts.
"""

import logging

import numpy as np
import pandas as pd

from src.ingestion.load_data import load_raw
from src.logging_config import setup_logging
from src.paths import PROCESSED_PATH

log: logging.Logger = logging.getLogger(__name__)

STAGE_ORDER: dict[str, int] = {
    "Group Stage": 1,
    "Round of 32": 2,
    "Round of 16": 3,
    "Quarter Finals": 4,
    "Semi Finals": 5,
    "Third Place Match": 6,
    "Final": 7,
}

RATING_MIN: int = 0
RATING_MAX: int = 10
PCT_MIN: int = 0
PCT_MAX: int = 1
SCORE_MIN: int = 0
SCORE_MAX: int = 100
MINUTES_MIN: int = 0
MINUTES_MAX: int = 120
SPEED_MIN: int = 0
SPEED_MAX: int = 40

AGE_BINS: list[int] = [0, 20, 24, 28, 32, 40]
AGE_LABELS: list[str] = ["U21", "21-24", "25-28", "29-32", "33+"]

MV_BINS: list[float] = [-1, 5e6, 20e6, 60e6, 150e6, 1e9]
MV_LABELS: list[str] = ["<€5M", "€5-20M", "€20-60M", "€60-150M", "€150M+"]

RTG_BINS: list[float] = [0, 4, 6, 7.5, 9, 10]
RTG_LABELS: list[str] = [
    "Poor (<4)",
    "Below Avg (4-6)",
    "Good (6-7.5)",
    "Excellent (7.5-9)",
    "World Class (9+)",
]

DEF_TACKLE_W: float = 1.5
DEF_INTERCEPT_W: float = 1.5
DEF_CLEAR_W: float = 1.0
DEF_BLOCK_W: float = 1.2
DEF_RECOVERY_W: float = 0.8

KNOCKOUT_THRESHOLD: int = 2
FULL_STARTER_MINUTES: int = 90

SCORE_CLIP_COLS: list[str] = [
    "performance_score",
    "offensive_contribution",
    "defensive_contribution",
    "possession_impact",
    "pressure_resistance",
    "creativity_score",
    "consistency_score",
    "clutch_performance_score",
]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Cleaning [yellow]…[/]")
    df = df.copy()

    str_cols = [
        "position",
        "preferred_foot",
        "match_result",
        "tournament_stage",
        "nationality",
        "team",
    ]
    for col in str_cols:
        df[col] = df[col].str.strip()

    df["player_rating"] = df["player_rating"].clip(RATING_MIN, RATING_MAX)
    df["tournament_rating"] = df["tournament_rating"].clip(RATING_MIN, RATING_MAX)
    df["pass_accuracy"] = df["pass_accuracy"].clip(PCT_MIN, PCT_MAX)
    df["save_percentage"] = df["save_percentage"].clip(PCT_MIN, PCT_MAX)
    df["stamina_score"] = df["stamina_score"].clip(SCORE_MIN, SCORE_MAX)
    df[SCORE_CLIP_COLS] = df[SCORE_CLIP_COLS].clip(SCORE_MIN, SCORE_MAX)
    df["minutes_played"] = df["minutes_played"].clip(MINUTES_MIN, MINUTES_MAX)
    df["top_speed_kmh"] = df["top_speed_kmh"].clip(SPEED_MIN, SPEED_MAX)

    log.info("Cleaning done [green]OK[/]")
    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Feature engineering [yellow]…[/]")
    df = df.copy()

    df["stage_order"] = df["tournament_stage"].map(STAGE_ORDER)
    df["match_month"] = df["match_date"].dt.month
    df["match_dow"] = df["match_date"].dt.day_name()

    df["age_group"] = pd.cut(
        df["age"],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        include_lowest=True,
    )

    df["market_value_tier"] = pd.cut(
        df["market_value_eur"],
        bins=MV_BINS,
        labels=MV_LABELS,
        include_lowest=True,
    )

    df["rating_tier"] = pd.cut(
        df["player_rating"],
        bins=RTG_BINS,
        labels=RTG_LABELS,
    )

    df["shot_efficiency"] = np.where(
        df["shots"] > 0,
        (df["goals"] / df["shots"]).round(3),
        np.nan,
    )

    df["pass_completion_pct"] = (df["pass_accuracy"] * 100).round(1)

    df["dribble_success_pct"] = np.where(
        df["dribbles_attempted"] > 0,
        (df["successful_dribbles"] / df["dribbles_attempted"] * 100).round(1),
        np.nan,
    )

    df["goal_involvement"] = df["goals"] + df["assists"]

    df["defensive_index"] = (
        df["tackles"] * DEF_TACKLE_W
        + df["interceptions"] * DEF_INTERCEPT_W
        + df["clearances"] * DEF_CLEAR_W
        + df["blocks"] * DEF_BLOCK_W
        + df["recoveries"] * DEF_RECOVERY_W
    ).round(2)

    unmapped = df["stage_order"].isna().sum()
    if unmapped:
        log.warning(
            "[yellow]%s[/] rows have unmapped tournament_stage — classified as non-knockout",
            unmapped,
        )

    df["is_knockout"] = (df["stage_order"] >= KNOCKOUT_THRESHOLD).astype(int)
    df["goal_diff"] = df["goals_team"] - df["goals_opponent"]

    df["km_per_minute"] = np.where(
        df["minutes_played"] > 0,
        (df["distance_covered_km"] / df["minutes_played"]).round(4),
        np.nan,
    )

    df["full_starter"] = (df["minutes_played"] >= FULL_STARTER_MINUTES).astype(int)

    log.info("Feature engineering done [green]OK[/]")
    return df


def save(df: pd.DataFrame) -> None:
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    log.info(
        "Saved [cyan]%s[/]  ([green]%s[/] rows)",
        PROCESSED_PATH,
        f"{len(df):,}",
    )


def run_pipeline(df: pd.DataFrame | None = None) -> pd.DataFrame:
    if df is None:
        df = load_raw()
    df = clean(df)
    df = feature_engineering(df)
    save(df)
    return df


if __name__ == "__main__":
    setup_logging()
    run_pipeline()
