from src.analysis.run_sql import STATEMENT_RE


class TestStatementRegex:
    def test_matches_select(self):
        sql = "SELECT * FROM fact_performance;"
        match = STATEMENT_RE.match(sql)
        assert match is not None

    def test_matches_with_cte(self):
        sql = "WITH cte AS (SELECT * FROM fact) SELECT * FROM cte;"
        match = STATEMENT_RE.match(sql)
        assert match is not None

    def test_rejects_insert(self):
        sql = "INSERT INTO t VALUES (1);"
        match = STATEMENT_RE.match(sql)
        assert match is None

    def test_rejects_create(self):
        sql = "CREATE TABLE t (x INT);"
        match = STATEMENT_RE.match(sql)
        assert match is None

    def test_splits_multiple_selects(self):
        sql = "SELECT 1; SELECT 2;"
        stmts = [s.strip() for s in sql.split(";") if s.strip() and STATEMENT_RE.match(s.strip())]
        assert len(stmts) == 2

    def test_skips_comment_lines(self):
        sql = "-- comment\nSELECT 1;"
        import re

        fragments = [re.sub(r"--.*", "", f).strip() for f in sql.split(";") if f.strip()]
        matches = [f for f in fragments if STATEMENT_RE.match(f)]
        assert len(matches) == 1
        assert "SELECT" in matches[0]

    def test_handles_empty_string(self):
        sql = ""
        stmts = [s.strip() for s in sql.split(";") if s.strip() and STATEMENT_RE.match(s.strip())]
        assert len(stmts) == 0

    def test_cte_multi_table(self):
        sql = """WITH
top_scorers AS (
    SELECT player_name, goals FROM fact_performance ORDER BY goals DESC LIMIT 10
)
SELECT * FROM top_scorers;"""
        match = STATEMENT_RE.match(sql)
        assert match is not None
