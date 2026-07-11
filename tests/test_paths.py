from src import __version__ as src_version
from src.paths import (
    DM_BASE,
    EXPORTS_DIR,
    FIGS_DIR,
    PROCESSED_PATH,
    PROJECT_ROOT,
    QUERIES_DIR,
    RAW_PATH,
)


def test_project_root() -> None:
    assert PROJECT_ROOT.is_dir()
    assert (PROJECT_ROOT / "src").is_dir()


def test_raw_path() -> None:
    assert RAW_PATH.is_absolute()
    assert RAW_PATH.parent.name == "raw"
    assert RAW_PATH.name == "fifa_wc2026_player_performance.csv"


def test_processed_path() -> None:
    assert PROCESSED_PATH.is_absolute()
    assert PROCESSED_PATH.parent.name == "processed"
    assert PROCESSED_PATH.name == "wc2026_clean.csv"


def test_dm_base() -> None:
    assert DM_BASE.is_absolute()
    assert DM_BASE.name == "datamarts"


def test_exports_dir() -> None:
    assert EXPORTS_DIR.is_absolute()
    assert EXPORTS_DIR.name == "exports"


def test_figs_dir() -> None:
    assert FIGS_DIR.is_absolute()
    assert FIGS_DIR.name == "figures"


def test_queries_dir() -> None:
    assert QUERIES_DIR.is_absolute()
    assert QUERIES_DIR.name == "queries"
    assert QUERIES_DIR.parent.name == "sql"


def test_queries_dir_contains_sql_files() -> None:
    sql_files = list(QUERIES_DIR.glob("*.sql"))
    assert len(sql_files) > 0


def test_version_is_string() -> None:
    assert isinstance(src_version, str)
    assert src_version.count(".") >= 2


def test_main_dot_py_runs_without_error() -> None:
    import subprocess
    result = subprocess.run(
        ["python", "src/__main__.py", "--help"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert len(result.stderr) > 0


def test_cli_dot_py_version() -> None:
    import subprocess
    result = subprocess.run(
        ["python", "cli.py", "--version"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "1.0.0"


def test_version_fallback_when_package_not_installed() -> None:
    import subprocess
    result = subprocess.run(
        [
            "python", "-c",
            "import sys; sys.path.insert(0, '.'); "
            "import importlib; importlib.invalidate_caches(); "
            "from src import __version__; print(__version__)",
        ],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "1.0.0"
