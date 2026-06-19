-- tournament_progression.sql
-- How stats evolve from group stage to the final.

SELECT
    m.tournament_stage,
    m.stage_order,
    COUNT(DISTINCT m.match_id)              AS matches,
    ROUND(AVG(m.total_goals_in_match), 2)   AS avg_goals_per_match,
    ROUND(AVG(m.total_shots), 1)            AS avg_shots_per_match,
    ROUND(AVG(f.player_rating), 2)          AS avg_player_rating,
    ROUND(AVG(f.performance_score), 2)      AS avg_performance,
    ROUND(AVG(f.clutch_performance_score), 2) AS avg_clutch,
    ROUND(AVG(f.pressure_resistance), 2)    AS avg_pressure_resistance,
    ROUND(AVG(f.distance_covered_km), 2)    AS avg_distance_km,
    ROUND(AVG(f.top_speed_kmh), 2)          AS avg_top_speed,
    SUM(f.yellow_cards)                     AS yellow_cards,
    SUM(f.red_cards)                        AS red_cards
FROM fact_performance f
JOIN dim_matches m ON f.match_id = m.match_id
GROUP BY m.tournament_stage, m.stage_order
ORDER BY m.stage_order;