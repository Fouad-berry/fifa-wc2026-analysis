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
  dimension: team_a {
    type: string
    sql: ${TABLE}.team_a ;;
  }
  dimension: team_b {
    type: string
    sql: ${TABLE}.team_b ;;
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
    type: number
    sql: ${TABLE}.match_month ;;
  }

  dimension: total_goals_in_match {
    type: number
    sql: ${TABLE}.total_goals_in_match ;;
  }
  dimension: total_shots {
    type: number
    sql: ${TABLE}.total_shots ;;
  }
  dimension: total_cards {
    type: number
    sql: ${TABLE}.total_cards ;;
  }
  dimension: avg_player_rating {
    type: number
    sql: ${TABLE}.avg_player_rating ;;
  }
  dimension: avg_distance_covered {
    type: number
    sql: ${TABLE}.avg_distance_covered ;;
  }
  dimension: players_in_match {
    type: number
    sql: ${TABLE}.players_in_match ;;
  }
  measure: count {
    type: count
    drill_fields: [match_id, stadium, tournament_stage]
  }
}
