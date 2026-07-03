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
"""

import logging
import sys
from pathlib import Path

import fire

from src.logging_config import get_console, setup_logging

sys.path.insert(0, str(Path(__file__).parent))

setup_logging()
log = logging.getLogger(__name__)
console = get_console()


def ingest() -> None:
    from src.ingestion.load_data import load_raw

    df = load_raw()
    console.print(f"[bold green]OK[/] — {len(df):,} rows, {len(df.columns)} columns")


def transform() -> None:
    from src.transformation.clean_transform import run_pipeline

    run_pipeline()


def datamarts() -> None:
    from src.datamarts.build_datamarts import run_all

    run_all()


def metrics() -> None:
    from src.analysis.metrics import run_all

    run_all()


def visualize() -> None:
    from src.analysis.viz import run_all

    run_all()


def profile() -> None:
    from src.analysis.profiling import run_all

    run_all()


def sql() -> None:
    from src.analysis.run_sql import run_all

    run_all()


def pipeline() -> None:
    console.rule("[bold cyan]Step 1: Ingest[/]")
    ingest()
    console.rule("[bold cyan]Step 2: Transform[/]")
    transform()
    console.rule("[bold cyan]Step 3: Datamarts[/]")
    datamarts()
    console.rule("[bold cyan]Step 4: Metrics[/]")
    metrics()
    console.print("[bold green]✔ Pipeline complete[/]")


def all_cmds() -> None:
    """Run everything: pipeline + visualize + profile + sql."""
    pipeline()
    console.rule("[bold cyan]Step 5: Visualize[/]")
    visualize()
    console.rule("[bold cyan]Step 6: Profile[/]")
    profile()
    console.rule("[bold cyan]Step 7: SQL Queries[/]")
    sql()
    console.print("[bold green]✔ All tasks complete[/]")


if __name__ == "__main__":
    fire.Fire({
        "ingest": ingest,
        "transform": transform,
        "datamarts": datamarts,
        "metrics": metrics,
        "visualize": visualize,
        "profile": profile,
        "sql": sql,
        "pipeline": pipeline,
        "all": all_cmds,
    })
