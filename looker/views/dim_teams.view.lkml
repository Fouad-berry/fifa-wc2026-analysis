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

  dimension: total_goals {
    type: number
    sql: ${TABLE}.total_goals ;;
  }
  dimension: total_assists {
    type: number
    sql: ${TABLE}.total_assists ;;
  }
  dimension: total_shots {
    type: number
    sql: ${TABLE}.total_shots ;;
  }
  dimension: avg_pass_accuracy {
    type: number
    sql: ${TABLE}.avg_pass_accuracy ;;
  }
  dimension: total_yellow_cards {
    type: number
    sql: ${TABLE}.total_yellow_cards ;;
  }
  dimension: total_red_cards {
    type: number
    sql: ${TABLE}.total_red_cards ;;
  }
  dimension: avg_player_rating {
    type: number
    sql: ${TABLE}.avg_player_rating ;;
  }
  dimension: avg_performance_score {
    type: number
    sql: ${TABLE}.avg_performance_score ;;
  }
  dimension: avg_distance_covered {
    type: number
    sql: ${TABLE}.avg_distance_covered ;;
  }
  dimension: avg_top_speed {
    type: number
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
