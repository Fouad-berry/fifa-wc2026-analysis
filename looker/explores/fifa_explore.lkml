include: "/looker/views/*.view.lkml"

explore: fact_performance {
  label: "Player Performance"
  group_label: "FIFA WC 2026"
  description: "Central fact table — one row per player per match"

  join: dim_players {
    sql_on: ${fact_performance.player_id} = ${dim_players.player_id} ;;
    relationship: many_to_one
    label: "Player"
  }

  join: dim_matches {
    sql_on: ${fact_performance.match_id} = ${dim_matches.match_id} ;;
    relationship: many_to_one
    label: "Match"
  }

  join: dim_teams {
    sql_on: ${fact_performance.team} = ${dim_teams.team} ;;
    relationship: many_to_one
    label: "Team"
  }
}

explore: dim_teams {
  label: "Teams Overview"
  group_label: "FIFA WC 2026"
}

explore: dim_stadiums {
  label: "Stadiums"
  group_label: "FIFA WC 2026"
}
