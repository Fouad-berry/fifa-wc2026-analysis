"""
cli.py
------
Convenience entry point for ``python cli.py <command>``.

Prefer the installed entry point instead::

    pip install -e .
    fifa-wc2026 pipeline
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.cli_runner import main  # noqa: E402

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
