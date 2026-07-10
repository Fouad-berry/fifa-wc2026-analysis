"""
cli.py
------
Entry point for the FIFA WC 2026 pipeline.

Usage:
    python cli.py pipeline        # Run full pipeline
    python cli.py ingest          # Load & validate raw data
    python cli.py transform       # Clean & feature engineer
    python cli.py datamarts       # Build star-schema datamarts
    python cli.py metrics         # Print KPI summary
    python cli.py visualize       # Generate plot figures
    python cli.py profile         # Statistical profiling
    python cli.py sql             # Run SQL queries via DuckDB
    python cli.py all             # Run everything
    python cli.py --version       # Show version
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
