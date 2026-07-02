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

setup_logging()
log = logging.getLogger(__name__)

STAGE_ORDER = {
    "Group Stage": 1,
    "Round of 32": 2,
    "Round of 16": 3,
    "Quarter Finals": 4,
    "Semi Finals": 5,
    "Third Place Match": 6,
    "Final": 7,
}

SCORE_CLIP_COLS = [
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
    log.info("Cleaning …")
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

    df["player_rating"] = df["player_rating"].clip(0, 10)
    df["tournament_rating"] = df["tournament_rating"].clip(0, 10)
    df["pass_accuracy"] = df["pass_accuracy"].clip(0, 1)
    df["save_percentage"] = df["save_percentage"].clip(0, 1)
    df["stamina_score"] = df["stamina_score"].clip(0, 100)
    df[SCORE_CLIP_COLS] = df[SCORE_CLIP_COLS].clip(0, 100)
    df["minutes_played"] = df["minutes_played"].clip(0, 120)
    df["top_speed_kmh"] = df["top_speed_kmh"].clip(0, 40)

    log.info("Cleaning done ✓")
    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Engineering features …")
    df = df.copy()

    df["stage_order"] = df["tournament_stage"].map(STAGE_ORDER)
    df["match_month"] = df["match_date"].dt.month
    df["match_dow"] = df["match_date"].dt.day_name()

    df["age_group"] = pd.cut(
        df["age"],
        bins=[16, 20, 24, 28, 32, 40],
        labels=["U21", "21-24", "25-28", "29-32", "33+"],
    )

    df["market_value_tier"] = pd.cut(
        df["market_value_eur"],
        bins=[0, 5e6, 20e6, 60e6, 150e6, 1e9],
        labels=["<€5M", "€5-20M", "€20-60M", "€60-150M", "€150M+"],
    )

    df["rating_tier"] = pd.cut(
        df["player_rating"],
        bins=[0, 4, 6, 7.5, 9, 10],
        labels=[
            "Poor (<4)",
            "Below Avg (4-6)",
            "Good (6-7.5)",
            "Excellent (7.5-9)",
            "World Class (9+)",
        ],
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
        df["tackles"] * 1.5
        + df["interceptions"] * 1.5
        + df["clearances"] * 1.0
        + df["blocks"] * 1.2
        + df["recoveries"] * 0.8
    ).round(2)

    df["is_knockout"] = (df["stage_order"] >= 2).astype(int)
    df["goal_diff"] = df["goals_team"] - df["goals_opponent"]

    df["km_per_minute"] = np.where(
        df["minutes_played"] > 0,
        (df["distance_covered_km"] / df["minutes_played"]).round(4),
        np.nan,
    )

    df["full_starter"] = (df["minutes_played"] >= 90).astype(int)

    log.info("Feature engineering done ✓")
    return df


def save(df: pd.DataFrame) -> None:
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    log.info("Saved processed fact table → %s  (%s rows)", PROCESSED_PATH, f"{len(df):,}")


def run_pipeline() -> pd.DataFrame:
    df = load_raw()
    df = clean(df)
    df = feature_engineering(df)
    save(df)
    return df


if __name__ == "__main__":
    run_pipeline()
