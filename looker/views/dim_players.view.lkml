view: dim_players {
  sql_table_name: dim_players ;;

  dimension: player_id {
    type: string
    primary_key: yes
    sql: ${TABLE}.player_id ;;
  }
  dimension: player_name {
    type: string
    sql: ${TABLE}.player_name ;;
  }
  dimension: age_group {
    type: string
    sql: ${TABLE}.age_group ;;
  }
  dimension: nationality {
    type: string
    sql: ${TABLE}.nationality ;;
  }
  dimension: team {
    type: string
    sql: ${TABLE}.team ;;
  }
  dimension: position {
    type: string
    sql: ${TABLE}.position ;;
  }
  dimension: preferred_foot {
    type: string
    sql: ${TABLE}.preferred_foot ;;
  }
  dimension: market_value_tier {
    type: string
    sql: ${TABLE}.market_value_tier ;;
  }

  measure: total_goals_tournament {
    type: sum
    sql: ${TABLE}.total_goals_tournament ;;
  }
  measure: total_assists_tournament {
    type: sum
    sql: ${TABLE}.total_assists_tournament ;;
  }
  measure: avg_bmi {
    type: average
    sql: ${TABLE}.bmi ;;
  }
  measure: count {
    type: count
    drill_fields: [player_name, team, position]
  }
}
