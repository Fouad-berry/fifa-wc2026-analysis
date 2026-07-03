import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def raw_df() -> pd.DataFrame:
    """Small synthetic DataFrame matching the raw CSV structure."""
    np.random.seed(42)
    n = 20
    players = [f"P{i:03d}" for i in range(1, 6)]
    matches = [f"M{i:03d}" for i in range(1, 5)]

    data = {
        "player_id": np.random.choice(players, n),
        "player_name": np.random.choice(["Alice", "Bob", "Carol", "Dave", "Eve"], n),
        "age": np.random.randint(19, 36, n),
        "nationality": np.random.choice(["Spain", "Brazil", "England"], n),
        "team": np.random.choice(["Spain", "Brazil", "England"], n),
        "jersey_number": np.random.randint(1, 23, n),
        "position": np.random.choice(["Goalkeeper", "Defender", "Midfielder", "Forward"], n),
        "height_cm": np.random.randint(165, 200, n),
        "weight_kg": np.random.randint(60, 95, n),
        "preferred_foot": np.random.choice(["Left", "Right"], n),
        "club_name": np.random.choice(["FC Barcelona", "Real Madrid", "Liverpool"], n),
        "market_value_eur": np.random.uniform(1e6, 100e6, n),
        "match_id": np.random.choice(matches, n),
        "match_date": pd.Timestamp("2026-06-14"),
        "stadium": np.random.choice(["Estadio Azteca", "Estadio BBVA", "MetLife Stadium"], n),
        "city": np.random.choice(["Mexico City", "Guadalajara", "New York"], n),
        "opponent_team": np.random.choice(["Spain", "Brazil", "England", "Qatar"], n),
        "tournament_stage": np.random.choice(
            ["Group Stage", "Round of 16", "Quarter Finals", "Final"], n
        ),
        "match_result": np.random.choice(["W", "D", "L"], n),
        "goals_team": np.random.randint(0, 5, n),
        "goals_opponent": np.random.randint(0, 5, n),
        "minutes_played": np.random.randint(0, 120, n),
        "goals": np.random.randint(0, 3, n),
        "assists": np.random.randint(0, 3, n),
        "shots": np.random.randint(0, 8, n),
        "shots_on_target": np.random.randint(0, 5, n),
        "expected_goals_xg": np.random.uniform(0, 3, n).round(2),
        "expected_assists_xa": np.random.uniform(0, 2, n).round(2),
        "key_passes": np.random.randint(0, 5, n),
        "successful_passes": np.random.randint(10, 80, n),
        "total_passes": np.random.randint(15, 100, n),
        "pass_accuracy": np.random.uniform(0.5, 1.0, n).round(3),
        "dribbles_attempted": np.random.randint(0, 10, n),
        "successful_dribbles": np.random.randint(0, 8, n),
        "crosses": np.random.randint(0, 6, n),
        "successful_crosses": np.random.randint(0, 4, n),
        "tackles": np.random.randint(0, 6, n),
        "interceptions": np.random.randint(0, 5, n),
        "clearances": np.random.randint(0, 8, n),
        "blocks": np.random.randint(0, 4, n),
        "aerial_duels_won": np.random.randint(0, 5, n),
        "aerial_duels_lost": np.random.randint(0, 5, n),
        "recoveries": np.random.randint(0, 10, n),
        "defensive_actions": np.random.randint(0, 15, n),
        "fouls_committed": np.random.randint(0, 4, n),
        "fouls_suffered": np.random.randint(0, 4, n),
        "yellow_cards": np.random.randint(0, 2, n),
        "red_cards": np.random.randint(0, 1, n),
        "offsides": np.random.randint(0, 3, n),
        "saves": np.random.randint(0, 8, n),
        "save_percentage": np.random.uniform(0, 1, n).round(3),
        "punches": np.random.randint(0, 3, n),
        "clean_sheet": np.random.randint(0, 2, n),
        "goals_conceded": np.random.randint(0, 5, n),
        "penalty_saves": np.random.randint(0, 1, n),
        "distance_covered_km": np.random.uniform(5, 14, n).round(2),
        "sprint_distance_km": np.random.uniform(0.5, 3, n).round(2),
        "top_speed_kmh": np.random.uniform(20, 36, n).round(1),
        "accelerations": np.random.randint(10, 50, n),
        "decelerations": np.random.randint(10, 45, n),
        "stamina_score": np.random.uniform(40, 100, n).round(1),
        "player_rating": np.random.uniform(3, 10, n).round(2),
        "performance_score": np.random.uniform(20, 100, n).round(2),
        "offensive_contribution": np.random.uniform(10, 100, n).round(2),
        "defensive_contribution": np.random.uniform(10, 100, n).round(2),
        "possession_impact": np.random.uniform(10, 100, n).round(2),
        "pressure_resistance": np.random.uniform(10, 100, n).round(2),
        "creativity_score": np.random.uniform(10, 100, n).round(2),
        "consistency_score": np.random.uniform(10, 100, n).round(2),
        "clutch_performance_score": np.random.uniform(10, 100, n).round(2),
        "total_goals_tournament": np.random.randint(0, 8, n),
        "total_assists_tournament": np.random.randint(0, 5, n),
        "total_minutes_tournament": np.random.randint(90, 600, n),
        "player_of_match_awards": np.random.randint(0, 3, n),
        "tournament_rating": np.random.uniform(3, 10, n).round(2),
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_csv(tmp_path, raw_df) -> str:
    """Write raw_df to a temporary CSV and return its path."""
    path = tmp_path / "test_data.csv"
    raw_df.to_csv(path, index=False)
    return str(path)


@pytest.fixture
def clean_df(raw_df) -> pd.DataFrame:
    """Apply clean() to raw_df to produce a cleaned DataFrame."""
    from src.transformation.clean_transform import clean, feature_engineering

    df = clean(raw_df)
    df = feature_engineering(df)
    return df
