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
  dimension: age {
    type: number
    sql: ${TABLE}.age ;;
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
  dimension: jersey_number {
    type: number
    sql: ${TABLE}.jersey_number ;;
  }
  dimension: position {
    type: string
    sql: ${TABLE}.position ;;
  }
  dimension: height_cm {
    type: number
    sql: ${TABLE}.height_cm ;;
  }
  dimension: weight_kg {
    type: number
    sql: ${TABLE}.weight_kg ;;
  }
  dimension: preferred_foot {
    type: string
    sql: ${TABLE}.preferred_foot ;;
  }
  dimension: club_name {
    type: string
    sql: ${TABLE}.club_name ;;
  }
  dimension: market_value_eur {
    type: number
    sql: ${TABLE}.market_value_eur ;;
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
  measure: total_minutes_tournament {
    type: sum
    sql: ${TABLE}.total_minutes_tournament ;;
  }
  measure: player_of_match_awards {
    type: sum
    sql: ${TABLE}.player_of_match_awards ;;
  }
  dimension: tournament_rating {
    type: number
    sql: ${TABLE}.tournament_rating ;;
  }
  measure: goal_involvement_tournament {
    type: sum
    sql: ${TABLE}.goal_involvement_tournament ;;
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
