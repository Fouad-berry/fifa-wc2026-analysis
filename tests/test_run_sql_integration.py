from pathlib import Path
from unittest.mock import patch

import duckdb
import pandas as pd
import pytest

from src.analysis.run_sql import load_tables, run_all, run_queries


@pytest.fixture
def conn():
    c = duckdb.connect()
    yield c
    c.close()


@pytest.fixture
def datamart_csvs(tmp_path):
    players = tmp_path / "dm_players"
    players.mkdir(parents=True)
    pd.DataFrame(
        {
            "player_id": [1, 2],
            "player_name": ["Alice", "Bob"],
            "team": ["Spain", "Brazil"],
            "position": ["Forward", "Defender"],
            "nationality": ["Spain", "Brazil"],
        }
    ).to_csv(players / "player_dim.csv", index=False)

    matches = tmp_path / "dm_matches"
    matches.mkdir()
    pd.DataFrame(
        {
            "match_id": [101, 102],
            "tournament_stage": ["Group Stage", "Final"],
            "stadium": ["Azteca", "Lusail"],
        }
    ).to_csv(matches / "match_dim.csv", index=False)

    teams = tmp_path / "dm_teams"
    teams.mkdir()
    pd.DataFrame(
        {
            "team": ["Spain", "Brazil"],
            "total_goals": [10, 5],
            "matches_played": [3, 3],
        }
    ).to_csv(teams / "team_dim.csv", index=False)

    stadiums = tmp_path / "dm_stadiums"
    stadiums.mkdir()
    pd.DataFrame(
        {
            "stadium": ["Azteca", "Lusail"],
            "city": ["Mexico City", "Lusail"],
        }
    ).to_csv(stadiums / "stadium_dim.csv", index=False)

    perf = tmp_path / "dm_performance"
    perf.mkdir()
    pd.DataFrame(
        {
            "player_id": [1, 1, 2],
            "match_id": [101, 102, 101],
            "team": ["Spain", "Spain", "Brazil"],
            "goals": [1, 2, 0],
            "assists": [0, 1, 1],
        }
    ).to_csv(perf / "fact_performance.csv", index=False)

    return tmp_path


class TestLoadTables:
    def test_loads_all_tables(self, conn, datamart_csvs, monkeypatch):
        monkeypatch.setattr(
            "src.analysis.run_sql.TABLES",
            {
                "dim_players": datamart_csvs / "dm_players/player_dim.csv",
                "dim_matches": datamart_csvs / "dm_matches/match_dim.csv",
                "dim_teams": datamart_csvs / "dm_teams/team_dim.csv",
                "dim_stadiums": datamart_csvs / "dm_stadiums/stadium_dim.csv",
                "fact_performance": datamart_csvs / "dm_performance/fact_performance.csv",
            },
        )
        load_tables(conn)
        tables = conn.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        ).fetchdf()
        expected = {"dim_players", "dim_matches", "dim_teams", "dim_stadiums", "fact_performance"}
        assert expected.issubset(set(tables["table_name"]))

    def test_skips_missing_table(self, conn, monkeypatch):
        monkeypatch.setattr(
            "src.analysis.run_sql.TABLES",
            {
                "dim_players": Path("/nonexistent/path.csv"),
            },
        )
        with patch("src.analysis.run_sql.log") as mock_log:
            load_tables(conn)
            mock_log.warning.assert_called_once()
            args = mock_log.warning.call_args[0]
            assert "Skipping" in args[0]
            assert args[1] == "dim_players"

    def test_data_queryable(self, conn, datamart_csvs, monkeypatch):
        monkeypatch.setattr(
            "src.analysis.run_sql.TABLES",
            {
                "dim_players": datamart_csvs / "dm_players/player_dim.csv",
                "dim_matches": datamart_csvs / "dm_matches/match_dim.csv",
                "dim_teams": datamart_csvs / "dm_teams/team_dim.csv",
                "dim_stadiums": datamart_csvs / "dm_stadiums/stadium_dim.csv",
                "fact_performance": datamart_csvs / "dm_performance/fact_performance.csv",
            },
        )
        load_tables(conn)
        result = conn.execute(
            "SELECT player_name, goals FROM fact_performance f "
            "JOIN dim_players p ON f.player_id = p.player_id "
            "ORDER BY goals DESC"
        ).fetchdf()
        assert len(result) == 3
        assert result["goals"].iloc[0] == 2


class TestRunQueries:
    def test_executes_sql_files(self, conn, datamart_csvs, monkeypatch, tmp_path):
        monkeypatch.setattr(
            "src.analysis.run_sql.TABLES",
            {
                "dim_players": datamart_csvs / "dm_players/player_dim.csv",
                "dim_matches": datamart_csvs / "dm_matches/match_dim.csv",
                "dim_teams": datamart_csvs / "dm_teams/team_dim.csv",
                "dim_stadiums": datamart_csvs / "dm_stadiums/stadium_dim.csv",
                "fact_performance": datamart_csvs / "dm_performance/fact_performance.csv",
            },
        )
        monkeypatch.setattr("src.analysis.run_sql.QUERIES_DIR", tmp_path)
        load_tables(conn)

        sql_file = tmp_path / "test_query.sql"
        sql_file.write_text(
            "SELECT team, SUM(goals) AS total_goals FROM fact_performance "
            "GROUP BY team ORDER BY total_goals DESC;"
        )
        with patch("src.analysis.run_sql.console") as mock_console:
            run_queries(conn)
            assert mock_console.print.call_count >= 2

    def test_handles_empty_sql_dir(self, conn, tmp_path, monkeypatch):
        monkeypatch.setattr("src.analysis.run_sql.TABLES", {})
        monkeypatch.setattr("src.analysis.run_sql.QUERIES_DIR", tmp_path / "empty_dir")
        with patch("src.analysis.run_sql.log") as mock_log:
            run_queries(conn)
            mock_log.warning.assert_called_once()

    def test_logs_error_on_bad_sql(self, conn, datamart_csvs, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.run_sql.TABLES", {})
        monkeypatch.setattr("src.analysis.run_sql.QUERIES_DIR", tmp_path)
        sql_file = tmp_path / "bad.sql"
        sql_file.write_text("SELECT * FROM nonexistent_table;")
        with patch("src.analysis.run_sql.log") as mock_log:
            run_queries(conn)
            assert mock_log.error.called
            args, kwargs = mock_log.error.call_args
            assert "Error running query from" in args[0]
            assert "bad.sql" in str(args[1])

    def test_prints_empty_result(self, conn, datamart_csvs, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.run_sql.TABLES", {})
        monkeypatch.setattr("src.analysis.run_sql.QUERIES_DIR", tmp_path)
        sql_file = tmp_path / "empty.sql"
        sql_file.write_text("SELECT * FROM (VALUES (1)) AS t WHERE 1=0;")
        with patch("src.analysis.run_sql.console") as mock_console:
            run_queries(conn)
            mock_console.print.assert_any_call("(empty result)")

    def test_skips_non_select_fragment(self, conn, datamart_csvs, monkeypatch, tmp_path):
        monkeypatch.setattr("src.analysis.run_sql.TABLES", {})
        monkeypatch.setattr("src.analysis.run_sql.QUERIES_DIR", tmp_path)
        sql_file = tmp_path / "mixed.sql"
        sql_file.write_text("SELECT 1 AS a;\nVALUES (1);\nSELECT 2 AS b;")
        with patch("src.analysis.run_sql.console") as mock_console:
            run_queries(conn)
            printed = [str(c[0][0]) for c in mock_console.print.call_args_list if c[0]]
            headers = [line.strip() for p in printed for line in p.split("\n") if line.strip()]
            assert "a" in headers
            assert "b" in headers


class TestRunAll:
    def test_run_all_creates_connection_and_loads(self, datamart_csvs, monkeypatch, tmp_path):
        monkeypatch.setattr(
            "src.analysis.run_sql.TABLES",
            {
                "dim_players": datamart_csvs / "dm_players/player_dim.csv",
                "dim_matches": datamart_csvs / "dm_matches/match_dim.csv",
                "dim_teams": datamart_csvs / "dm_teams/team_dim.csv",
                "dim_stadiums": datamart_csvs / "dm_stadiums/stadium_dim.csv",
                "fact_performance": datamart_csvs / "dm_performance/fact_performance.csv",
            },
        )
        monkeypatch.setattr("src.analysis.run_sql.QUERIES_DIR", tmp_path)

        sql_file = tmp_path / "test.sql"
        sql_file.write_text("SELECT COUNT(*) AS cnt FROM dim_players;")

        run_all()

    def test_run_all_no_sql_files(self, datamart_csvs, monkeypatch):
        monkeypatch.setattr("src.analysis.run_sql.TABLES", {})
        monkeypatch.setattr("src.analysis.run_sql.QUERIES_DIR", datamart_csvs / "no_sql")
        run_all()

    def test_all_sql_queries_run_without_error(self, monkeypatch) -> None:
        import duckdb
        from src.analysis.run_sql import TABLES, QUERIES_DIR, STATEMENT_RE

        missing = [p for p in TABLES.values() if not p.exists()]
        if missing:
            pytest.skip(f"Missing datamart files: {missing}")

        conn = duckdb.connect()
        try:
            from src.analysis.run_sql import load_tables
            load_tables(conn)
            for sql_file in sorted(QUERIES_DIR.glob("*.sql")):
                sql = sql_file.read_text(encoding="utf-8")
                for fragment in sql.split(";"):
                    fragment = fragment.strip()
                    if not fragment:
                        continue
                    clean = __import__("re").sub(r"--.*", "", fragment).strip()
                    if not clean or not STATEMENT_RE.match(clean):
                        continue
                    conn.execute(fragment + ";")
        finally:
            conn.close()
