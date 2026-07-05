"""
run_sql.py
----------
Load datamarts into DuckDB and run SQL queries from sql/queries/.
"""

import logging
import re

import duckdb

from src.logging_config import setup_logging
from src.paths import DM_BASE, PROJECT_ROOT

log = logging.getLogger(__name__)

QUERIES_DIR = PROJECT_ROOT / "sql" / "queries"

TABLES = {
    "dim_players": DM_BASE / "dm_players/player_dim.csv",
    "dim_matches": DM_BASE / "dm_matches/match_dim.csv",
    "dim_teams": DM_BASE / "dm_teams/team_dim.csv",
    "dim_stadiums": DM_BASE / "dm_stadiums/stadium_dim.csv",
    "fact_performance": DM_BASE / "dm_performance/fact_performance.csv",
}

SELECT_RE = re.compile(r"(SELECT\b.+?;)", re.IGNORECASE | re.DOTALL)


def load_tables(conn: duckdb.DuckDBPyConnection) -> None:
    for table, path in TABLES.items():
        if not path.exists():
            log.warning("Skipping %s — file not found at %s", table, path)
            continue
        safe_path = str(path).replace("'", "''")
        conn.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{safe_path}')")
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        log.info("Loaded %s (%s rows)", table, f"{count:,}")


def run_queries(conn: duckdb.DuckDBPyConnection) -> None:
    sql_files = sorted(QUERIES_DIR.glob("*.sql"))
    if not sql_files:
        log.warning("No SQL files found in %s", QUERIES_DIR)
        return

    for sql_file in sql_files:
        print(f"\n{'=' * 60}")
        print(f"  Query: {sql_file.name}")
        print(f"{'=' * 60}")
        sql = sql_file.read_text()

        for match in SELECT_RE.finditer(sql):
            stmt = match.group(1).strip()
            try:
                result = conn.execute(stmt).fetchdf()
                if not result.empty:
                    print(result.to_string(index=False))
                else:
                    print("(empty result)")
            except Exception as e:
                log.error("Error running query from %s: %s", sql_file.name, e)


def run_all() -> None:
    conn = duckdb.connect()
    try:
        load_tables(conn)
        run_queries(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    setup_logging()
    run_all()
