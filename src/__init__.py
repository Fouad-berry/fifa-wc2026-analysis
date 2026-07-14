"""FIFA World Cup 2026 — Player Performance Analysis package."""

from importlib.metadata import version as _version

__version__: str
try:
    __version__ = _version("fifa-wc2026-analysis")
except Exception:
    __version__ = "1.0.0"

from src.logging_config import get_console, setup_logging  # noqa: E402
from src.paths import (  # noqa: E402
    DM_BASE,
    EXPORTS_DIR,
    FIGS_DIR,
    PROCESSED_PATH,
    PROJECT_ROOT,
    QUERIES_DIR,
    RAW_PATH,
)

__all__ = [
    "__version__",
    "DM_BASE",
    "EXPORTS_DIR",
    "FIGS_DIR",
    "PROCESSED_PATH",
    "PROJECT_ROOT",
    "QUERIES_DIR",
    "RAW_PATH",
    "get_console",
    "setup_logging",
]
