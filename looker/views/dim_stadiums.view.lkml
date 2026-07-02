view: dim_stadiums {
  sql_table_name: dim_stadiums ;;

  dimension: stadium {
    type: string
    primary_key: yes
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
  measure: count {
    type: count
    drill_fields: [stadium, city]
  }
}
