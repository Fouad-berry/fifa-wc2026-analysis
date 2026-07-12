from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).parent.parent

RAW_PATH: Path = PROJECT_ROOT / "data" / "raw" / "fifa_wc2026_player_performance.csv"
PROCESSED_PATH: Path = PROJECT_ROOT / "data" / "processed" / "wc2026_clean.csv"
DM_BASE: Path = PROJECT_ROOT / "data" / "datamarts"
EXPORTS_DIR: Path = PROJECT_ROOT / "data" / "exports"
FIGS_DIR: Path = PROJECT_ROOT / "figures"
QUERIES_DIR: Path = PROJECT_ROOT / "sql" / "queries"
