# FIFA World Cup 2026 — Looker Dashboard
# Generated automatically from the star-schema datamarts.
# Requires: fact_performance, dim_players, dim_matches, dim_teams, dim_stadiums

dashboard: fifa_wc2026_overview {

  title: "FIFA World Cup 2026 — Tournament Overview"
  description: "End-to-end performance analysis across 54,600 player-match records."
  layout: newspaper

  # ── Tile 1: Goals per stage ────────────────────────────────────────────────
  element: goals_per_stage {
    title: "Goals per Tournament Stage"
    explore: fact_performance
    type: looker_column
    fields: [dim_matches.tournament_stage, fact_performance.goals]
    sorts: [dim_matches.stage_order]
    limit: 50
  }

  # ── Tile 2: Top scorers table ──────────────────────────────────────────────
  element: top_scorers {
    title: "Top 10 Scorers"
    explore: fact_performance
    type: looker_table
    fields: [
      dim_players.player_name, dim_players.team,
      fact_performance.goals, fact_performance.assists,
      fact_performance.expected_goals_xg
    ]
    limit: 10
  }

  # ── Tile 3: Defensive index by team ────────────────────────────────────────
  element: defensive_index {
    title: "Defensive Index by Team"
    explore: fact_performance
    type: looker_bar
    fields: [dim_teams.team, fact_performance.defensive_contribution]
    sorts: [fact_performance.defensive_contribution desc]
    limit: 20
  }

  # ── Tile 4: Player rating distribution ─────────────────────────────────────
  element: rating_distribution {
    title: "Player Rating Distribution"
    explore: fact_performance
    type: looker_histogram
    fields: [fact_performance.player_rating]
  }

  # ── Tile 5: Stadium excitement index ───────────────────────────────────────
  element: stadium_excitement {
    title: "Goals per Match by Stadium"
    explore: dim_stadiums
    type: looker_bar
    fields: [dim_stadiums.stadium, dim_stadiums.goals_per_match]
    sorts: [dim_stadiums.goals_per_match desc]
    limit: 16
  }

  # ── Tile 6: Physical performance by nationality ────────────────────────────
  element: physical_heatmap {
    title: "Avg Distance Covered by Nationality"
    explore: fact_performance
    type: looker_scatter
    fields: [dim_players.nationality, fact_performance.distance_covered_km]
    limit: 48
  }

  # ── Tile 7: Goalkeeper leaderboard ─────────────────────────────────────────
  element: goalkeeper_leaderboard {
    title: "Goalkeeper Save % Leaderboard"
    explore: fact_performance
    type: looker_table
    fields: [
      dim_players.player_name, dim_players.team,
      fact_performance.saves, fact_performance.goals_conceded
    ]
    filters: [dim_players.position: "Goalkeeper"]
    limit: 10
  }

  # ── Tile 8: Win rate by team ───────────────────────────────────────────────
  element: win_rate {
    title: "Win / Draw / Loss by Team"
    explore: dim_teams
    type: looker_column
    fields: [dim_teams.team, dim_teams.wins, dim_teams.draws, dim_teams.losses]
    sorts: [dim_teams.wins desc]
    limit: 48
  }

  # ── Tile 9: Knockout performers ────────────────────────────────────────────
  element: knockout_heroes {
    title: "Knockout Stage — Clutch Performance"
    explore: fact_performance
    type: looker_table
    fields: [
      dim_players.player_name, dim_players.team, dim_players.position,
      fact_performance.clutch_performance_score, fact_performance.pressure_resistance
    ]
    filters: [dim_matches.is_knockout: "Yes"]
    limit: 15
  }
}
