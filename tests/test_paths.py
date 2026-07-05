from src.paths import (
    DM_BASE,
    EXPORTS_DIR,
    FIGS_DIR,
    PROCESSED_PATH,
    PROJECT_ROOT,
    QUERIES_DIR,
    RAW_PATH,
)


def test_project_root():
    assert PROJECT_ROOT.is_dir()
    assert (PROJECT_ROOT / "src").is_dir()


def test_raw_path():
    assert RAW_PATH.is_absolute()
    assert RAW_PATH.parent.name == "raw"
    assert RAW_PATH.name == "fifa_wc2026_player_performance.csv"


def test_processed_path():
    assert PROCESSED_PATH.is_absolute()
    assert PROCESSED_PATH.parent.name == "processed"
    assert PROCESSED_PATH.name == "wc2026_clean.csv"


def test_dm_base():
    assert DM_BASE.is_absolute()
    assert DM_BASE.name == "datamarts"


def test_exports_dir():
    assert EXPORTS_DIR.is_absolute()
    assert EXPORTS_DIR.name == "exports"


def test_figs_dir():
    assert FIGS_DIR.is_absolute()
    assert FIGS_DIR.name == "figures"


def test_queries_dir():
    assert QUERIES_DIR.is_absolute()
    assert QUERIES_DIR.name == "queries"
    assert QUERIES_DIR.parent.name == "sql"


def test_queries_dir_contains_sql_files():
    sql_files = list(QUERIES_DIR.glob("*.sql"))
    assert len(sql_files) >= 5
