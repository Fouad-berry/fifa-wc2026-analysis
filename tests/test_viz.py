import pandas as pd
import pytest

from src.analysis.viz import (
    goals_by_stage,
    physical_correlation,
    position_profile,
    run_all,
    team_goals,
    top_scorers_bar,
    tournament_heatmap,
)


@pytest.fixture
def top_scorers_csv(tmp_path):
    p = tmp_path / "top_scorers.csv"
    pd.DataFrame(
        {
            "player_name": [f"Player {i}" for i in range(5)],
            "team": ["Spain"] * 5,
            "goals": [10, 8, 6, 4, 2],
        }
    ).to_csv(p, index=False)
    return p


@pytest.fixture
def agg_by_stage_csv(tmp_path):
    p = tmp_path / "agg_by_stage.csv"
    pd.DataFrame(
        {
            "tournament_stage": ["Group Stage", "Round of 16", "Final"],
            "stage_order": [1, 3, 7],
            "total_goals": [100, 50, 20],
            "avg_rating": [7.0, 7.5, 8.0],
        }
    ).to_csv(p, index=False)
    return p


@pytest.fixture
def agg_by_position_csv(tmp_path):
    p = tmp_path / "agg_by_position.csv"
    pd.DataFrame(
        {
            "position": ["Forward", "Midfielder", "Defender", "Goalkeeper"],
            "avg_rating": [7.5, 7.0, 6.8, 6.5],
            "avg_goals": [0.5, 0.2, 0.1, 0.0],
            "avg_assists": [0.3, 0.4, 0.1, 0.0],
            "avg_defensive_index": [10, 30, 50, 60],
        }
    ).to_csv(p, index=False)
    return p


@pytest.fixture
def team_dim_csv(tmp_path):
    d = tmp_path / "dm_teams"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "team_dim.csv"
    pd.DataFrame(
        {
            "team": ["Spain", "Brazil", "England", "France"],
            "total_goals": [15, 12, 10, 8],
        }
    ).to_csv(p, index=False)
    return p


@pytest.fixture
def processed_csv(tmp_path):
    p = tmp_path / "wc2026_clean.csv"
    pd.DataFrame(
        {
            "tournament_stage": ["Group Stage", "Group Stage", "Final", "Final"],
            "position": ["Forward", "Defender", "Forward", "Midfielder"],
            "player_rating": [8.0, 7.0, 9.0, 7.5],
            "distance_covered_km": [10.0, 11.0, 9.5, 12.0],
            "sprint_distance_km": [2.0, 1.5, 2.5, 1.8],
            "top_speed_kmh": [32.0, 30.0, 34.0, 31.0],
            "stamina_score": [80.0, 85.0, 75.0, 90.0],
            "accelerations": [30, 25, 35, 28],
        }
    ).to_csv(p, index=False)
    return p


class TestTopScorersBar:
    def test_saves_png(self, top_scorers_csv, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path)
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        top_scorers_bar(top_n=5)
        assert (tmp_path / "top_scorers.png").exists()

    def test_returns_none_when_missing_file(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path / "nonexistent")
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        result = top_scorers_bar()
        assert result is None


class TestGoalsByStage:
    def test_saves_png(self, agg_by_stage_csv, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path)
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        goals_by_stage()
        assert (tmp_path / "goals_by_stage.png").exists()

    def test_returns_none_when_missing_file(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path / "nonexistent")
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        result = goals_by_stage()
        assert result is None


class TestPositionProfile:
    def test_saves_png(self, agg_by_position_csv, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path)
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        position_profile()
        assert (tmp_path / "position_profile.png").exists()

    def test_returns_none_when_missing_file(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path / "nonexistent")
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        result = position_profile()
        assert result is None


class TestTeamGoals:
    def test_saves_png(self, team_dim_csv, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.DM_BASE", tmp_path)
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        team_goals(top_n=4)
        assert (tmp_path / "team_goals.png").exists()

    def test_returns_none_when_missing_file(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.DM_BASE", tmp_path / "nonexistent")
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        result = team_goals()
        assert result is None


class TestTournamentHeatmap:
    def test_saves_png_with_dataframe(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        df = pd.DataFrame(
            {
                "tournament_stage": ["Group Stage", "Final"],
                "position": ["Forward", "Defender"],
                "player_rating": [8.0, 7.0],
            }
        )
        tournament_heatmap(df)
        assert (tmp_path / "tournament_heatmap.png").exists()

    def test_loads_from_processed(self, processed_csv, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.PROCESSED_PATH", processed_csv)
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        tournament_heatmap()
        assert (tmp_path / "tournament_heatmap.png").exists()

    def test_returns_none_when_no_data(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.PROCESSED_PATH", tmp_path / "nonexistent.csv")
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        result = tournament_heatmap()
        assert result is None


class TestPhysicalCorrelation:
    def test_saves_png_with_dataframe(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        df = pd.DataFrame(
            {
                "distance_covered_km": [10.0, 11.0, 9.5],
                "sprint_distance_km": [2.0, 1.5, 2.5],
                "top_speed_kmh": [32.0, 30.0, 34.0],
                "stamina_score": [80.0, 85.0, 75.0],
                "accelerations": [30, 25, 35],
                "player_rating": [8.0, 7.0, 9.0],
            }
        )
        physical_correlation(df)
        assert (tmp_path / "physical_correlation.png").exists()

    def test_loads_from_processed(self, processed_csv, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.PROCESSED_PATH", processed_csv)
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        physical_correlation()
        assert (tmp_path / "physical_correlation.png").exists()

    def test_returns_none_when_no_data(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.viz.PROCESSED_PATH", tmp_path / "nonexistent.csv")
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        result = physical_correlation()
        assert result is None


class TestRunAll:
    def test_run_all_creates_all_figures(
        self, top_scorers_csv, agg_by_stage_csv, agg_by_position_csv,
        team_dim_csv, processed_csv, monkeypatch, tmp_path
    ):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path)
        monkeypatch.setattr("src.analysis.viz.DM_BASE", tmp_path)
        monkeypatch.setattr("src.analysis.viz.PROCESSED_PATH", processed_csv)
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        run_all()
        expected = [
            "top_scorers.png",
            "goals_by_stage.png",
            "position_profile.png",
            "team_goals.png",
            "tournament_heatmap.png",
            "physical_correlation.png",
        ]
        for f in expected:
            assert (tmp_path / f).exists(), f"Missing {f}"

    def test_run_all_skips_heatmap_when_no_processed(
        self, top_scorers_csv, agg_by_stage_csv, agg_by_position_csv,
        team_dim_csv, monkeypatch, tmp_path
    ):
        monkeypatch.setattr("src.analysis.viz.EXPORTS_DIR", tmp_path)
        monkeypatch.setattr("src.analysis.viz.DM_BASE", tmp_path)
        monkeypatch.setattr("src.analysis.viz.PROCESSED_PATH", tmp_path / "nonexistent.csv")
        monkeypatch.setattr("src.analysis.viz.FIGS_DIR", tmp_path)
        run_all()
        assert (tmp_path / "top_scorers.png").exists()
        assert (tmp_path / "goals_by_stage.png").exists()
        assert not (tmp_path / "tournament_heatmap.png").exists()
