view: fact_performance {
  sql_table_name: fact_performance ;;

  dimension: player_id {
    type: string
    sql: ${TABLE}.player_id ;;
  }
  dimension: match_id {
    type: string
    sql: ${TABLE}.match_id ;;
  }
  dimension: team {
    type: string
    sql: ${TABLE}.team ;;
  }
  dimension: tournament_stage {
    type: string
    sql: ${TABLE}.tournament_stage ;;
  }
  dimension: match_result {
    type: string
    sql: ${TABLE}.match_result ;;
  }
  dimension: rating_tier {
    type: string
    sql: ${TABLE}.rating_tier ;;
  }
  dimension: is_knockout {
    type: yesno
    sql: ${TABLE}.is_knockout ;;
  }
  dimension: full_starter {
    type: yesno
    sql: ${TABLE}.full_starter ;;
  }

  measure: total_goals {
    type: sum
    sql: ${TABLE}.goals ;;
  }
  measure: total_assists {
    type: sum
    sql: ${TABLE}.assists ;;
  }
  measure: total_shots {
    type: sum
    sql: ${TABLE}.shots ;;
  }
  measure: avg_rating {
    type: average
    sql: ${TABLE}.player_rating ;;
  }
  measure: avg_performance_score {
    type: average
    sql: ${TABLE}.performance_score ;;
  }
  measure: avg_clutch_score {
    type: average
    sql: ${TABLE}.clutch_performance_score ;;
  }
  measure: total_distance_km {
    type: sum
    sql: ${TABLE}.distance_covered_km ;;
  }
  measure: total_yellow_cards {
    type: sum
    sql: ${TABLE}.yellow_cards ;;
  }
  measure: total_red_cards {
    type: sum
    sql: ${TABLE}.red_cards ;;
  }
  measure: count {
    type: count
    drill_fields: [player_id, match_id, team, tournament_stage]
  }
}
