view: dim_teams {
  sql_table_name: dim_teams ;;

  dimension: team {
    type: string
    primary_key: yes
    sql: ${TABLE}.team ;;
  }
  dimension: nationality {
    type: string
    sql: ${TABLE}.nationality ;;
  }
  dimension: squad_size {
    type: number
    sql: ${TABLE}.squad_size ;;
  }
  dimension: avg_age {
    type: number
    sql: ${TABLE}.avg_age ;;
  }
  dimension: avg_height_cm {
    type: number
    sql: ${TABLE}.avg_height_cm ;;
  }
  dimension: avg_weight_kg {
    type: number
    sql: ${TABLE}.avg_weight_kg ;;
  }
  dimension: avg_market_value_eur {
    type: number
    sql: ${TABLE}.avg_market_value_eur ;;
  }
  dimension: total_market_value_eur {
    type: number
    sql: ${TABLE}.total_market_value_eur ;;
  }
  dimension: matches_played {
    type: number
    sql: ${TABLE}.matches_played ;;
  }
  dimension: wins {
    type: number
    sql: ${TABLE}.wins ;;
  }
  dimension: draws {
    type: number
    sql: ${TABLE}.draws ;;
  }
  dimension: losses {
    type: number
    sql: ${TABLE}.losses ;;
  }

  measure: total_goals {
    type: sum
    sql: ${TABLE}.total_goals ;;
  }
  measure: total_assists {
    type: sum
    sql: ${TABLE}.total_assists ;;
  }
  measure: total_shots {
    type: sum
    sql: ${TABLE}.total_shots ;;
  }
  measure: avg_pass_accuracy {
    type: average
    sql: ${TABLE}.avg_pass_accuracy ;;
  }
  measure: total_yellow_cards {
    type: sum
    sql: ${TABLE}.total_yellow_cards ;;
  }
  measure: total_red_cards {
    type: sum
    sql: ${TABLE}.total_red_cards ;;
  }
  measure: avg_player_rating {
    type: average
    sql: ${TABLE}.avg_player_rating ;;
  }
  measure: avg_performance_score {
    type: average
    sql: ${TABLE}.avg_performance_score ;;
  }
  measure: avg_distance_covered {
    type: average
    sql: ${TABLE}.avg_distance_covered ;;
  }
  measure: avg_top_speed {
    type: average
    sql: ${TABLE}.avg_top_speed ;;
  }
  measure: win_rate {
    type: number
    sql: ${TABLE}.win_rate ;;
  }
  measure: goals_per_match {
    type: number
    sql: ${TABLE}.goals_per_match ;;
  }
  measure: count {
    type: count
    drill_fields: [team, nationality]
  }
}
