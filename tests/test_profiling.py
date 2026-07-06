import logging
import warnings
from unittest.mock import MagicMock, patch

import pandas as pd

from src.analysis.profiling import describe_distribution, run_all


def test_describe_distribution_returns_stats() -> None:
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], name="test")
    result = describe_distribution(s)
    assert result["count"] == 5
    assert result["mean"] == 3.0
    assert result["min"] == 1.0
    assert result["max"] == 5.0
    assert "skew" in result
    assert "kurtosis" in result


def test_describe_distribution_too_few_values() -> None:
    s = pd.Series([1.0], name="test")
    assert describe_distribution(s) == {}


def test_describe_distribution_all_nan() -> None:
    s = pd.Series([float("nan"), float("nan")], name="test")
    assert describe_distribution(s) == {}


def test_describe_distribution_constant() -> None:
    s = pd.Series([5.0, 5.0, 5.0], name="test")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        result = describe_distribution(s)
    assert result["mean"] == 5.0
    assert result["std"] == 0.0
    assert pd.isna(result["skew"])


@patch("src.analysis.profiling.PROCESSED_PATH")
def test_run_all_returns_early_when_no_file(mock_path, caplog) -> None:
    mock_path.exists.return_value = False
    with caplog.at_level(logging.ERROR):
        run_all()
    assert "not found" in caplog.text


@patch("src.analysis.profiling.PROCESSED_PATH")
def test_run_all_profiles_numeric_columns(mock_path) -> None:
    df = pd.DataFrame({
        "rating": [1.0, 2.0, 3.0, 4.0, 5.0],
        "goals": [0, 1, 0, 2, 0],
        "name": ["A", "B", "C", "D", "E"],
    })
    mock_path.exists.return_value = True
    mock_path.__fspath__ = MagicMock(return_value="/fake/path")
    with patch("pandas.read_csv", return_value=df):
        run_all()
