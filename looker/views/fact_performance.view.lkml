view: fact_performance {
  sql_table_name: fact_performance ;;

  dimension: fact_key {
    type: string
    primary_key: yes
    sql: CONCAT(${TABLE}.player_id, '|', ${TABLE}.match_id) ;;
  }
  dimension: player_id {
    type: string
    sql: ${TABLE}.player_id ;;
  }
  dimension: match_id {
    type: string
    sql: ${TABLE}.match_id ;;
  }
  dimension: team {
    type: string
    sql: ${TABLE}.team ;;
  }
  dimension: tournament_stage {
    type: string
    sql: ${TABLE}.tournament_stage ;;
  }
  dimension: stage_order {
    type: number
    sql: ${TABLE}.stage_order ;;
  }
  dimension: match_result {
    type: string
    sql: ${TABLE}.match_result ;;
  }
  dimension: rating_tier {
    type: string
    sql: ${TABLE}.rating_tier ;;
  }
  dimension: is_knockout {
    type: yesno
    sql: ${TABLE}.is_knockout ;;
  }
  dimension: full_starter {
    type: yesno
    sql: ${TABLE}.full_starter ;;
  }
  dimension: minutes_played {
    type: number
    sql: ${TABLE}.minutes_played ;;
  }

  measure: total_goals {
    type: sum
    sql: ${TABLE}.goals ;;
  }
  measure: total_assists {
    type: sum
    sql: ${TABLE}.assists ;;
  }
  measure: total_shots {
    type: sum
    sql: ${TABLE}.shots ;;
  }
  measure: total_shots_on_target {
    type: sum
    sql: ${TABLE}.shots_on_target ;;
  }
  measure: total_key_passes {
    type: sum
    sql: ${TABLE}.key_passes ;;
  }
  measure: total_xg {
    type: sum
    sql: ${TABLE}.expected_goals_xg ;;
  }
  measure: total_xa {
    type: sum
    sql: ${TABLE}.expected_assists_xa ;;
  }
  measure: goal_diff {
    type: sum
    sql: ${TABLE}.goal_diff ;;
  }
  measure: avg_rating {
    type: average
    sql: ${TABLE}.player_rating ;;
  }
  measure: avg_performance_score {
    type: average
    sql: ${TABLE}.performance_score ;;
  }
  measure: avg_offensive_contribution {
    type: average
    sql: ${TABLE}.offensive_contribution ;;
  }
  measure: avg_defensive_contribution {
    type: average
    sql: ${TABLE}.defensive_contribution ;;
  }
  measure: avg_creativity_score {
    type: average
    sql: ${TABLE}.creativity_score ;;
  }
  measure: avg_clutch_score {
    type: average
    sql: ${TABLE}.clutch_performance_score ;;
  }
  measure: avg_shot_efficiency {
    type: average
    sql: ${TABLE}.shot_efficiency ;;
  }
  measure: avg_defensive_index {
    type: average
    sql: ${TABLE}.defensive_index ;;
  }
  measure: avg_pass_accuracy {
    type: average
    sql: ${TABLE}.pass_accuracy ;;
  }
  measure: total_tackles {
    type: sum
    sql: ${TABLE}.tackles ;;
  }
  measure: total_interceptions {
    type: sum
    sql: ${TABLE}.interceptions ;;
  }
  measure: total_clearances {
    type: sum
    sql: ${TABLE}.clearances ;;
  }
  measure: total_recoveries {
    type: sum
    sql: ${TABLE}.recoveries ;;
  }
  measure: total_fouls {
    type: sum
    sql: ${TABLE}.fouls_committed ;;
  }
  measure: total_distance_km {
    type: sum
    sql: ${TABLE}.distance_covered_km ;;
  }
  measure: total_sprint_distance_km {
    type: sum
    sql: ${TABLE}.sprint_distance_km ;;
  }
  measure: total_yellow_cards {
    type: sum
    sql: ${TABLE}.yellow_cards ;;
  }
  measure: total_red_cards {
    type: sum
    sql: ${TABLE}.red_cards ;;
  }
  measure: total_saves {
    type: sum
    sql: ${TABLE}.saves ;;
  }
  measure: avg_save_percentage {
    type: average
    sql: ${TABLE}.save_percentage ;;
  }
  measure: avg_top_speed_kmh {
    type: average
    sql: ${TABLE}.top_speed_kmh ;;
  }
  measure: avg_stamina_score {
    type: average
    sql: ${TABLE}.stamina_score ;;
  }
  measure: avg_km_per_minute {
    type: average
    sql: ${TABLE}.km_per_minute ;;
  }
  measure: count {
    type: count
    drill_fields: [player_id, match_id, team, tournament_stage]
  }
}
