import subprocess
import sys

from src.paths import PROJECT_ROOT


def _run_as_main(module: str) -> int:
    result = subprocess.run(
        [sys.executable, "-m", module],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    return result.returncode


class TestMainBlocks:
    def test_metrics_main_block(self) -> None:
        assert _run_as_main("src.analysis.metrics") == 0

    def test_profiling_main_block(self) -> None:
        assert _run_as_main("src.analysis.profiling") == 0

    def test_run_sql_main_block(self) -> None:
        assert _run_as_main("src.analysis.run_sql") == 0

    def test_load_data_main_block(self) -> None:
        assert _run_as_main("src.ingestion.load_data") == 0

    def test_cli_runner_main_block(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "src.cli_runner", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0

    def test_clean_transform_main_block(self) -> None:
        assert _run_as_main("src.transformation.clean_transform") == 0

    def test_build_datamarts_main_block(self) -> None:
        assert _run_as_main("src.datamarts.build_datamarts") == 0

    def test_viz_main_block(self) -> None:
        assert _run_as_main("src.analysis.viz") == 0
