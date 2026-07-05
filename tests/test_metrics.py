from unittest.mock import patch

from src.analysis.metrics import run_all


@patch("src.analysis.metrics.PROCESSED_PATH")
def test_run_all_returns_empty_when_no_processed_file(mock_processed_path):
    mock_processed_path.exists.return_value = False
    result = run_all()
    assert result == {}
