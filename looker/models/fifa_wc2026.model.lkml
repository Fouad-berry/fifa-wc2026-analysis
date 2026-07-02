connection: "fifa_wc2026"

include: "/looker/views/*.view.lkml"
include: "/looker/explores/*.explore.lkml"

explore: fact_performance {
  label: "Performance Facts"
  join: dim_players {
    sql_on: ${fact_performance.player_id} = ${dim_players.player_id} ;;
    relationship: many_to_one
  }
  join: dim_matches {
    sql_on: ${fact_performance.match_id} = ${dim_matches.match_id} ;;
    relationship: many_to_one
  }
  join: dim_teams {
    sql_on: ${fact_performance.team} = ${dim_teams.team} ;;
    relationship: many_to_one
  }
}
