view: dim_matches {
  sql_table_name: dim_matches ;;

  dimension: match_id {
    type: string
    primary_key: yes
    sql: ${TABLE}.match_id ;;
  }
  dimension: match_date {
    type: date
    sql: ${TABLE}.match_date ;;
  }
  dimension: stadium {
    type: string
    sql: ${TABLE}.stadium ;;
  }
  dimension: city {
    type: string
    sql: ${TABLE}.city ;;
  }
  dimension: tournament_stage {
    type: string
    sql: ${TABLE}.tournament_stage ;;
  }
  dimension: match_dow {
    type: string
    sql: ${TABLE}.match_dow ;;
  }
  dimension: is_knockout {
    type: yesno
    sql: ${TABLE}.is_knockout ;;
  }
  dimension: stage_order {
    type: number
    sql: ${TABLE}.stage_order ;;
  }
  dimension: match_month {
    type: string
    sql: ${TABLE}.match_month ;;
  }

  measure: total_goals_in_match {
    type: sum
    sql: ${TABLE}.total_goals_in_match ;;
  }
  measure: total_shots {
    type: sum
    sql: ${TABLE}.total_shots ;;
  }
  measure: total_cards {
    type: sum
    sql: ${TABLE}.total_cards ;;
  }
  measure: avg_player_rating {
    type: average
    sql: ${TABLE}.avg_player_rating ;;
  }
  measure: avg_distance_covered {
    type: average
    sql: ${TABLE}.avg_distance_covered ;;
  }
  measure: players_in_match {
    type: number
    sql: ${TABLE}.players_in_match ;;
  }
  measure: count {
    type: count
    drill_fields: [match_id, stadium, tournament_stage]
  }
}
