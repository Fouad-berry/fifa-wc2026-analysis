import numpy as np
import pandas as pd
import pytest

from src.ingestion.load_data import NUMERIC_COLS, load_raw, validate


class TestLoadRaw:
    def test_load_returns_dataframe(self, sample_csv) -> None:
        df = load_raw(sample_csv)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_numeric_cols_are_numeric(self, sample_csv) -> None:
        df = load_raw(sample_csv)
        for col in NUMERIC_COLS:
            if col in df.columns:
                assert np.issubdtype(df[col].dtype, np.number), f"{col} is not numeric"

    def test_match_date_is_datetime(self, sample_csv) -> None:
        df = load_raw(sample_csv)
        assert np.issubdtype(df["match_date"].dtype, np.datetime64)

    def test_column_names_stripped(self, tmp_path) -> None:
        path = tmp_path / "spaces.csv"
        pd.DataFrame(
            {
                "  player_id  ": ["P1"],
                "  match_date  ": ["2026-06-14"],
                "  position  ": ["Goalkeeper"],
                "  tournament_stage  ": ["Group Stage"],
                "  match_result  ": ["W"],
            }
        ).to_csv(path, index=False)
        df = load_raw(str(path))
        assert list(df.columns) == [
            "player_id",
            "match_date",
            "position",
            "tournament_stage",
            "match_result",
        ]

    def test_missing_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_raw("/nonexistent/path.csv")


class TestLoadRawEdgeCases:
    def test_load_raw_default_path(self, sample_csv, monkeypatch):
        monkeypatch.setattr("src.ingestion.load_data.RAW_PATH", sample_csv)
        df = load_raw()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_numeric_coercion_warns(self, raw_df, caplog, tmp_path):
        raw_df["goals"] = raw_df["goals"].astype(object)
        raw_df.loc[0, "goals"] = "not_a_number"
        path = tmp_path / "bad_numeric.csv"
        raw_df.to_csv(path, index=False)
        import logging

        with caplog.at_level(logging.WARNING):
            load_raw(str(path))
        assert any("coerced to NaN" in msg for msg in caplog.messages)

    def test_multiple_validation_issues_plural(self, raw_df, caplog, tmp_path):
        raw_df.loc[0, "position"] = "Alien"
        raw_df.loc[1, "position"] = "Alien2"
        path = tmp_path / "multi_issue.csv"
        raw_df.to_csv(path, index=False)
        import logging

        with caplog.at_level(logging.WARNING):
            load_raw(str(path))
        assert any("issues" in msg for msg in caplog.messages)

    def test_date_coercion_warns(self, raw_df, caplog, tmp_path):
        raw_df["match_date"] = raw_df["match_date"].astype(object)
        raw_df.loc[0, "match_date"] = "not_a_date"
        path = tmp_path / "bad_date.csv"
        raw_df.to_csv(path, index=False)
        import logging

        with caplog.at_level(logging.WARNING):
            load_raw(str(path))
        assert any("dates coerced to NaT" in msg for msg in caplog.messages)


class TestValidate:
    def test_valid_data_passes(self, raw_df) -> None:
        validate(raw_df)

    def test_bad_position_warns(self, raw_df, caplog) -> None:
        raw_df.loc[0, "position"] = "Alien"
        validate(raw_df)
        assert any("unexpected positions" in msg for msg in caplog.messages)

    def test_bad_stage_warns(self, raw_df, caplog) -> None:
        raw_df.loc[0, "tournament_stage"] = "Prequarter"
        validate(raw_df)
        assert any("unexpected tournament stages" in msg for msg in caplog.messages)

    def test_bad_result_warns(self, raw_df, caplog) -> None:
        raw_df.loc[0, "match_result"] = "X"
        validate(raw_df)
        assert any("unexpected match results" in msg for msg in caplog.messages)

    def test_null_values_warns(self, raw_df, caplog) -> None:
        raw_df.loc[0, "goals"] = float("nan")
        import logging

        with caplog.at_level(logging.WARNING):
            validate(raw_df)
        assert any("Null values" in msg for msg in caplog.messages)

    def test_validation_returns_count(self, raw_df) -> None:
        raw_df.loc[0, "position"] = "Alien"
        raw_df.loc[1, "position"] = "Alien2"
        raw_df.loc[0, "tournament_stage"] = "BadStage"
        raw_df.loc[0, "match_result"] = "X"
        n = validate(raw_df)
        assert n > 1
