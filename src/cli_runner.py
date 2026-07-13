"""
cli_runner.py
-------------
CLI dispatch logic for the FIFA WC 2026 pipeline.
"""

import sys

import fire
import pandas as pd
from rich.console import Console

from src.logging_config import get_console, setup_logging

setup_logging()
console: Console = get_console()


def ingest() -> pd.DataFrame:
    """Load raw CSV and validate columns."""
    from src.ingestion.load_data import load_raw

    df = load_raw()
    console.print(f"[bold green]OK[/] — {len(df):,} rows, {len(df.columns)} columns")
    return df


def transform() -> None:
    """Clean data and create engineered features."""
    from src.transformation.clean_transform import run_pipeline

    run_pipeline()


def datamarts() -> None:
    """Build star-schema dimension tables and export CSVs."""
    from src.datamarts.build_datamarts import run_all

    run_all()


def metrics() -> None:
    """Print top-level KPI summary to console."""
    from src.analysis.metrics import run_all

    run_all()


def visualize() -> None:
    """Generate all analysis figures as PNG files."""
    from src.analysis.viz import run_all

    run_all()


def profile() -> None:
    """Print statistical profile of every numeric column."""
    from src.analysis.profiling import run_all

    run_all()


def sql() -> None:
    """Run all SQL queries from sql/queries/ via DuckDB."""
    from src.analysis.run_sql import run_all

    run_all()


def pipeline() -> None:
    """Run ingest → transform → datamarts → metrics."""
    console.rule("[bold cyan]Step 1: Ingest[/]")
    df = ingest()

    console.rule("[bold cyan]Step 2: Transform[/]")
    from src.transformation.clean_transform import run_pipeline

    df = run_pipeline(df)
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


def main() -> None:
    if "--version" in sys.argv or "-V" in sys.argv:
        from src import __version__

        print(__version__)
        return
    fire.Fire(
        {
            "ingest": ingest,
            "transform": transform,
            "datamarts": datamarts,
            "metrics": metrics,
            "visualize": visualize,
            "profile": profile,
            "sql": sql,
            "pipeline": pipeline,
            "all": all_cmds,
        }
    )


if __name__ == "__main__":
    main()
