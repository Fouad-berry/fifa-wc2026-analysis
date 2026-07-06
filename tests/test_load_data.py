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
