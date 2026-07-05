from unittest.mock import patch

import pandas as pd
import pytest

from src.analysis.metrics import run_all


@patch("src.analysis.metrics.PROCESSED_PATH")
def test_run_all_returns_empty_when_no_processed_file(mock_processed_path):
    mock_processed_path.exists.return_value = False
    result = run_all()
    assert result == {}


@pytest.fixture
def metrics_datamarts(tmp_path):
    processed = tmp_path / "processed"
    processed.mkdir()
    processed_csv = processed / "wc2026_clean.csv"

    player_dir = tmp_path / "dm_players"
    player_dir.mkdir()
    player_csv = player_dir / "player_dim.csv"

    team_dir = tmp_path / "dm_teams"
    team_dir.mkdir()
    team_csv = team_dir / "team_dim.csv"

    stadium_dir = tmp_path / "dm_stadiums"
    stadium_dir.mkdir()
    stadium_csv = stadium_dir / "stadium_dim.csv"

    df = pd.DataFrame(
        {
            "player_id": ["P1", "P1", "P2"],
            "match_id": ["M1", "M2", "M1"],
            "team": ["Spain", "Spain", "Brazil"],
            "stadium": ["Azteca", "BBVA", "Azteca"],
            "goals": [1, 2, 0],
            "yellow_cards": [0, 1, 0],
            "red_cards": [0, 0, 0],
            "player_rating": [7.5, 8.0, 6.0],
            "distance_covered_km": [10.5, 11.2, 9.8],
            "top_speed_kmh": [32.0, 31.5, 30.0],
            "match_date": pd.to_datetime(["2026-06-14", "2026-06-20", "2026-06-14"]),
        }
    )
    df.to_csv(processed_csv, index=False)

    players = pd.DataFrame(
        {
            "player_id": ["P1", "P2"],
            "player_name": ["Alice", "Bob"],
            "team": ["Spain", "Brazil"],
            "total_goals_tournament": [3, 0],
        }
    )
    players.to_csv(player_csv, index=False)

    teams = pd.DataFrame(
        {
            "team": ["Spain", "Brazil"],
            "total_goals": [3, 0],
        }
    )
    teams.to_csv(team_csv, index=False)

    stadiums = pd.DataFrame(
        {
            "stadium": ["Azteca", "BBVA"],
            "city": ["Mexico City", "Guadalajara"],
            "goals_per_match": [2.0, 1.0],
        }
    )
    stadiums.to_csv(stadium_csv, index=False)

    return tmp_path, processed_csv, player_csv, team_csv, stadium_csv


def test_run_all_happy_path(metrics_datamarts, monkeypatch):
    tmp_path, processed_csv, _player_csv, _team_csv, _stadium_csv = metrics_datamarts
    monkeypatch.setattr("src.analysis.metrics.PROCESSED_PATH", processed_csv)
    monkeypatch.setattr("src.analysis.metrics.DM_BASE", tmp_path)

    result = run_all()
    assert result["total_records"] == 3
    assert result["unique_players"] == 2
    assert result["unique_matches"] == 2
    assert result["nations"] == 2
    assert result["stadiums"] == 2
    assert result["total_goals"] == 3
    assert result["avg_goals_per_match"] == 1.5
