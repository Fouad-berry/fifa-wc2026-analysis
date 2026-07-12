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

  dimension: matches_hosted {
    type: number
    sql: ${TABLE}.matches_hosted ;;
  }
  dimension: total_goals_scored {
    type: number
    sql: ${TABLE}.total_goals_scored ;;
  }
  dimension: goals_per_match {
    type: number
    sql: ${TABLE}.goals_per_match ;;
  }
  dimension: avg_player_rating {
    type: number
    sql: ${TABLE}.avg_player_rating ;;
  }
  dimension: avg_top_speed {
    type: number
    sql: ${TABLE}.avg_top_speed ;;
  }
  dimension: avg_distance_covered {
    type: number
    sql: ${TABLE}.avg_distance_covered ;;
  }
  dimension: total_yellow_cards {
    type: number
    sql: ${TABLE}.total_yellow_cards ;;
  }
  dimension: total_red_cards {
    type: number
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
