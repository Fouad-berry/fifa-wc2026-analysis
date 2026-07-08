from unittest.mock import patch

import pandas as pd
import pytest

from src.cli_runner import (
    all_cmds,
    datamarts,
    ingest,
    metrics,
    pipeline,
    profile,
    sql,
    transform,
    visualize,
)


def test_dispatch_all_keys_present() -> None:
    dispatch = {
        "ingest": ingest,
        "transform": transform,
        "datamarts": datamarts,
        "metrics": metrics,
        "visualize": visualize,
        "profile": profile,
        "sql": sql,
        "pipeline": pipeline,
        "all": all_cmds,
    }
    for name, func in dispatch.items():
        assert callable(func), f"{name} is not callable"
    assert len(dispatch) == 9


@pytest.fixture
def mock_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "goals": [1, 2],
            "match_id": [1, 1],
            "player_id": [10, 20],
            "team": ["A", "A"],
            "stadium": ["X", "X"],
        }
    )


@patch("src.cli_runner.datamarts")
@patch("src.cli_runner.metrics")
@patch("src.cli_runner.ingest")
@patch("src.transformation.clean_transform.run_pipeline")
def test_pipeline_runs_all_steps(
    mock_run_pipeline, mock_ingest, mock_metrics, mock_datamarts
) -> None:
    pipeline()
    mock_ingest.assert_called_once()
    mock_run_pipeline.assert_called_once()
    mock_datamarts.assert_called_once()
    mock_metrics.assert_called_once()


@patch("src.cli_runner.pipeline")
@patch("src.cli_runner.visualize")
@patch("src.cli_runner.profile")
@patch("src.cli_runner.sql")
def test_all_cmds_runs_everything(mock_sql, mock_profile, mock_visualize, mock_pipeline) -> None:
    all_cmds()
    mock_pipeline.assert_called_once()
    mock_visualize.assert_called_once()
    mock_profile.assert_called_once()
    mock_sql.assert_called_once()


@patch("src.analysis.profiling.run_all")
def test_profile_dispatches(mock_run) -> None:
    profile()
    mock_run.assert_called_once()


@patch("src.analysis.viz.run_all")
def test_visualize_dispatches(mock_run) -> None:
    visualize()
    mock_run.assert_called_once()


@patch("src.analysis.run_sql.run_all")
def test_sql_dispatches(mock_run) -> None:
    sql()
    mock_run.assert_called_once()


@patch("src.datamarts.build_datamarts.run_all")
def test_datamarts_dispatches(mock_run) -> None:
    datamarts()
    mock_run.assert_called_once()


@patch("src.transformation.clean_transform.run_pipeline")
def test_transform_dispatches(mock_run) -> None:
    transform()
    mock_run.assert_called_once()


@patch("src.analysis.metrics.run_all")
def test_metrics_dispatches(mock_run) -> None:
    metrics()
    mock_run.assert_called_once()


def test_main_registers_commands() -> None:
    from src.cli_runner import main
    with patch("src.cli_runner.fire.Fire") as mock_fire:
        main()
        assert mock_fire.called
        cmd_dict = mock_fire.call_args[0][0]
        expected = {"ingest", "transform", "datamarts", "metrics",
                    "visualize", "profile", "sql", "pipeline", "all"}
        assert set(cmd_dict.keys()) == expected


@patch("src.ingestion.load_data.load_raw")
def test_ingest_returns_dataframe(mock_load_raw, mock_df) -> None:
    mock_load_raw.return_value = mock_df
    result = ingest()
    pd.testing.assert_frame_equal(result, mock_df)
