import numpy as np
import pytest

from src.transformation.clean_transform import STAGE_ORDER, clean, feature_engineering, save


class TestClean:
    def test_returns_copy(self, raw_df):
        result = clean(raw_df)
        assert result is not raw_df

    def test_strips_string_columns(self, raw_df):
        raw_df["position"] = "  Goalkeeper  "
        result = clean(raw_df)
        assert result["position"].iloc[0] == "Goalkeeper"

    def test_clips_player_rating(self, raw_df):
        raw_df["player_rating"] = 15.0
        result = clean(raw_df)
        assert result["player_rating"].max() == 10.0

    def test_clips_pass_accuracy(self, raw_df):
        raw_df["pass_accuracy"] = 1.5
        result = clean(raw_df)
        assert result["pass_accuracy"].max() == 1.0

    def test_clips_minutes_played(self, raw_df):
        raw_df["minutes_played"] = 200
        result = clean(raw_df)
        assert result["minutes_played"].max() == 120

    def test_clips_top_speed(self, raw_df):
        raw_df["top_speed_kmh"] = 99.0
        result = clean(raw_df)
        assert result["top_speed_kmh"].max() == 40.0

    def test_clips_stamina(self, raw_df):
        raw_df["stamina_score"] = 999.0
        result = clean(raw_df)
        assert result["stamina_score"].max() == 100.0

    def test_clips_all_score_cols(self, raw_df):
        score_cols = [
            "performance_score",
            "offensive_contribution",
            "defensive_contribution",
            "possession_impact",
            "pressure_resistance",
            "creativity_score",
            "consistency_score",
            "clutch_performance_score",
        ]
        for c in score_cols:
            raw_df[c] = -50.0
        result = clean(raw_df)
        for c in score_cols:
            assert result[c].min() >= 0.0, f"{c} not clipped above 0"


class TestFeatureEngineering:
    def test_stage_order_mapped(self, raw_df):
        df = clean(raw_df)
        result = feature_engineering(df)
        raw_stages = df["tournament_stage"].unique()
        for stage in raw_stages:
            mapped = result.loc[df["tournament_stage"] == stage, "stage_order"].iloc[0]
            assert mapped == STAGE_ORDER[stage]

    def test_age_group_present(self, raw_df):
        df = clean(raw_df)
        result = feature_engineering(df)
        assert "age_group" in result.columns
        assert result["age_group"].dtype.name == "category"

    def test_market_value_tier_present(self, raw_df):
        df = clean(raw_df)
        result = feature_engineering(df)
        assert "market_value_tier" in result.columns

    def test_shot_efficiency(self, raw_df):
        df = clean(raw_df)
        df["shots"] = 5
        df["goals"] = 2
        result = feature_engineering(df)
        assert result["shot_efficiency"].iloc[0] == pytest.approx(0.4)

    def test_shot_efficiency_nan_when_no_shots(self, raw_df):
        df = clean(raw_df)
        df["shots"] = 0
        result = feature_engineering(df)
        assert np.isnan(result["shot_efficiency"].iloc[0])

    def test_goal_involvement(self, raw_df):
        df = clean(raw_df)
        df["goals"] = 2
        df["assists"] = 1
        result = feature_engineering(df)
        assert result["goal_involvement"].iloc[0] == 3

    def test_defensive_index(self, raw_df):
        df = clean(raw_df)
        df["tackles"] = 2
        df["interceptions"] = 3
        df["clearances"] = 1
        df["blocks"] = 0
        df["recoveries"] = 5
        result = feature_engineering(df)
        expected = 2 * 1.5 + 3 * 1.5 + 1 * 1.0 + 0 * 1.2 + 5 * 0.8
        assert result["defensive_index"].iloc[0] == expected

    def test_is_knockout(self, raw_df):
        df = clean(raw_df)
        df["tournament_stage"] = "Group Stage"
        result = feature_engineering(df)
        assert result["is_knockout"].iloc[0] == 0

    def test_knockout_stage(self, raw_df):
        df = clean(raw_df)
        df["tournament_stage"] = "Round of 16"
        result = feature_engineering(df)
        assert result["is_knockout"].iloc[0] == 1

    def test_full_starter(self, raw_df):
        df = clean(raw_df)
        df["minutes_played"] = 90
        result = feature_engineering(df)
        assert result["full_starter"].iloc[0] == 1

    def test_not_full_starter(self, raw_df):
        df = clean(raw_df)
        df["minutes_played"] = 45
        result = feature_engineering(df)
        assert result["full_starter"].iloc[0] == 0

    def test_dribble_success_pct(self, raw_df):
        df = clean(raw_df)
        df["dribbles_attempted"] = 10
        df["successful_dribbles"] = 7
        result = feature_engineering(df)
        assert result["dribble_success_pct"].iloc[0] == 70.0

    def test_km_per_minute(self, raw_df):
        df = clean(raw_df)
        df["distance_covered_km"] = 10.0
        df["minutes_played"] = 90
        result = feature_engineering(df)
        expected = round(10.0 / 90, 4)
        assert result["km_per_minute"].iloc[0] == expected


class TestSave:
    def test_save_creates_file(self, clean_df, tmp_path, monkeypatch):
        fake_path = tmp_path / "processed" / "test.csv"
        monkeypatch.setattr("src.transformation.clean_transform.PROCESSED_PATH", fake_path)
        save(clean_df)
        assert fake_path.exists()
