-- stadium_analysis.sql
-- Venue-level analysis: goals, excitement, physical performance.

SELECT
    s.stadium,
    s.city,
    s.matches_hosted,
    s.total_goals_scored,
    s.goals_per_match,
    s.avg_player_rating,
    s.avg_top_speed,
    s.avg_distance_covered,
    s.total_yellow_cards,
    s.total_red_cards,
    s.unique_teams,
    -- Excitement index: goals + cards per match
    ROUND((s.total_goals_scored + s.total_yellow_cards * 0.5 + s.total_red_cards * 1.5)
          / s.matches_hosted, 2)                AS excitement_index
FROM dim_stadiums s
ORDER BY s.goals_per_match DESC;