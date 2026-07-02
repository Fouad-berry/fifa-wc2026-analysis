from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "fifa_wc2026_player_performance.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "wc2026_clean.csv"
DM_BASE = PROJECT_ROOT / "data" / "datamarts"
EXPORTS_DIR = PROJECT_ROOT / "data" / "exports"
