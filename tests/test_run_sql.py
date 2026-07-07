import re

from src.analysis.run_sql import STATEMENT_RE


class TestStatementRegex:
    def test_matches_select(self) -> None:
        sql = "SELECT * FROM fact_performance;"
        match = STATEMENT_RE.match(sql)
        assert match is not None

    def test_matches_with_cte(self) -> None:
        sql = "WITH cte AS (SELECT * FROM fact) SELECT * FROM cte;"
        match = STATEMENT_RE.match(sql)
        assert match is not None

    def test_rejects_insert(self) -> None:
        sql = "INSERT INTO t VALUES (1);"
        match = STATEMENT_RE.match(sql)
        assert match is None

    def test_rejects_create(self) -> None:
        sql = "CREATE TABLE t (x INT);"
        match = STATEMENT_RE.match(sql)
        assert match is None

    def test_splits_multiple_selects(self) -> None:
        sql = "SELECT 1; SELECT 2;"
        stmts = [s.strip() for s in sql.split(";") if s.strip() and STATEMENT_RE.match(s.strip())]
        assert len(stmts) == 2

    def test_skips_comment_lines(self) -> None:
        sql = "-- comment\nSELECT 1;"
        fragments = [re.sub(r"--.*", "", f).strip() for f in sql.split(";") if f.strip()]
        matches = [f for f in fragments if STATEMENT_RE.match(f)]
        assert len(matches) == 1
        assert "SELECT" in matches[0]

    def test_handles_empty_string(self) -> None:
        sql = ""
        stmts = [s.strip() for s in sql.split(";") if s.strip() and STATEMENT_RE.match(s.strip())]
        assert len(stmts) == 0

    def test_cte_multi_table(self) -> None:
        sql = """WITH
top_scorers AS (
    SELECT player_name, goals FROM fact_performance ORDER BY goals DESC LIMIT 10
)
SELECT * FROM top_scorers;"""
        match = STATEMENT_RE.match(sql)
        assert match is not None
