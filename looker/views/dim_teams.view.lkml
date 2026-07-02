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

  measure: squad_size {
    type: number
    sql: ${TABLE}.squad_size ;;
  }
  measure: total_goals {
    type: sum
    sql: ${TABLE}.total_goals ;;
  }
  measure: total_assists {
    type: sum
    sql: ${TABLE}.total_assists ;;
  }
  measure: win_rate {
    type: number
    sql: ${TABLE}.win_rate ;;
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
    drill_fields: [team, nationality]
  }
}
