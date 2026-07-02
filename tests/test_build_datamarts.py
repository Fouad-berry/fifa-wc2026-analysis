import pytest

from src.datamarts.build_datamarts import (
    build_dim_players,
    build_dim_matches,
    build_dim_teams,
    build_dim_stadiums,
    build_fact_performance,
    build_exports,
    load_processed,
)


class TestDimPlayers:
    def test_one_row_per_player(self, clean_df):
        dim = build_dim_players(clean_df)
        assert dim["player_id"].is_unique
        assert len(dim) == clean_df["player_id"].nunique()

    def test_expected_columns(self, clean_df):
        dim = build_dim_players(clean_df)
        expected = {
            "player_id", "player_name", "age_group", "team",
            "goal_involvement_tournament", "bmi",
        }
        assert expected.issubset(dim.columns)

    def test_bmi_computed(self, clean_df):
        dim = build_dim_players(clean_df)
        first = dim.iloc[0]
        expected_bmi = round(first["weight_kg"] / ((first["height_cm"] / 100) ** 2), 1)
        assert first["bmi"] == expected_bmi


class TestDimMatches:
    def test_one_row_per_match(self, clean_df):
        dim = build_dim_matches(clean_df)
        assert dim["match_id"].is_unique
        assert len(dim) == clean_df["match_id"].nunique()

    def test_aggregate_stats_added(self, clean_df):
        dim = build_dim_matches(clean_df)
        expected = {
            "total_goals_in_match", "total_shots", "total_cards",
            "avg_player_rating", "players_in_match",
        }
        assert expected.issubset(dim.columns)


class TestDimTeams:
    def test_one_row_per_team(self, clean_df):
        dim = build_dim_teams(clean_df)
        assert dim["team"].is_unique
        assert len(dim) == clean_df["team"].nunique()

    def test_win_rate_computed(self, clean_df):
        dim = build_dim_teams(clean_df)
        for _, row in dim.iterrows():
            expected = round(row["wins"] / row["matches_played"] * 100, 1)
            assert row["win_rate"] == expected

    def test_goals_per_match_computed(self, clean_df):
        dim = build_dim_teams(clean_df)
        for _, row in dim.iterrows():
            if row["matches_played"] > 0:
                expected = round(row["total_goals"] / row["matches_played"], 2)
                assert row["goals_per_match"] == expected


class TestDimStadiums:
    def test_correct_rows(self, clean_df):
        dim = build_dim_stadiums(clean_df)
        assert len(dim) == clean_df[["stadium", "city"]].drop_duplicates().shape[0]

    def test_goals_per_match(self, clean_df):
        dim = build_dim_stadiums(clean_df)
        for _, row in dim.iterrows():
            expected = round(row["total_goals_scored"] / row["matches_hosted"], 2)
            assert row["goals_per_match"] == expected


class TestFactPerformance:
    def test_row_count_preserved(self, clean_df):
        fact = build_fact_performance(clean_df)
        assert len(fact) == len(clean_df)

    def test_expected_columns_present(self, clean_df):
        fact = build_fact_performance(clean_df)
        assert "player_id" in fact.columns
        assert "match_id" in fact.columns
        assert "goals" in fact.columns
        assert "player_rating" in fact.columns


class TestExports:
    def test_returns_dict(self, clean_df):
        exports = build_exports(clean_df)
        assert isinstance(exports, dict)

    def test_all_expected_keys(self, clean_df):
        exports = build_exports(clean_df)
        expected_keys = [
            "top_scorers", "agg_by_position", "agg_by_stage",
            "agg_team_attack", "agg_team_defense", "agg_physical",
            "agg_goalkeepers", "knockout_performers", "agg_stadiums",
            "agg_age_performance",
        ]
        for k in expected_keys:
            assert k in exports, f"Missing export: {k}"

    def test_top_scorers_limited_to_50(self, clean_df):
        exports = build_exports(clean_df)
        assert len(exports["top_scorers"]) <= 50

    def test_knockout_only_knockout(self, clean_df):
        exports = build_exports(clean_df)
        for _, row in exports["knockout_performers"].iterrows():
            match_rows = clean_df[
                (clean_df["player_id"] == row["player_id"])
                & (clean_df["is_knockout"] == 1)
            ]
            assert len(match_rows) > 0

    def test_goalkeepers_only(self, clean_df):
        exports = build_exports(clean_df)
        assert len(exports["agg_goalkeepers"]) == clean_df[
            clean_df["position"] == "Goalkeeper"
        ]["player_id"].nunique()


class TestLoadProcessed:
    def test_missing_file_raises(self, monkeypatch):
        from src.paths import PROCESSED_PATH

        monkeypatch.setattr(
            "src.datamarts.build_datamarts.PROCESSED_PATH",
            PROCESSED_PATH.parent / "nonexistent.csv",
        )
        with pytest.raises(FileNotFoundError):
            load_processed()
