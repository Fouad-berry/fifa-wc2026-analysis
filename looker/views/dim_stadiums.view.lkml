view: dim_stadiums {
  sql_table_name: dim_stadiums ;;

  dimension: stadium_city_key {
    type: string
    primary_key: yes
    sql: ${TABLE}.stadium || '||' || ${TABLE}.city ;;
  }
  dimension: stadium {
    type: string
    sql: ${TABLE}.stadium ;;
  }
  dimension: city {
    type: string
    sql: ${TABLE}.city ;;
  }

  measure: matches_hosted {
    type: number
    sql: ${TABLE}.matches_hosted ;;
  }
  measure: total_goals_scored {
    type: sum
    sql: ${TABLE}.total_goals_scored ;;
  }
  measure: goals_per_match {
    type: number
    sql: ${TABLE}.goals_per_match ;;
  }
  measure: avg_player_rating {
    type: average
    sql: ${TABLE}.avg_player_rating ;;
  }
  measure: avg_top_speed {
    type: average
    sql: ${TABLE}.avg_top_speed ;;
  }
  measure: avg_distance_covered {
    type: average
    sql: ${TABLE}.avg_distance_covered ;;
  }
  measure: total_yellow_cards {
    type: sum
    sql: ${TABLE}.total_yellow_cards ;;
  }
  measure: total_red_cards {
    type: sum
    sql: ${TABLE}.total_red_cards ;;
  }
  dimension: unique_teams {
    type: number
    sql: ${TABLE}.unique_teams ;;
  }
  measure: count {
    type: count
    drill_fields: [stadium, city]
  }
}
