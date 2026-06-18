-- top_scorers.sql
-- Golden Boot leaderboard + xG over/under-performance.

-- 1. Top 20 scorers
SELECT
    p.player_name,
    p.team,
    p.position,
    p.age,
    p.market_value_tier,
    SUM(f.goals)                            AS total_goals,
    SUM(f.assists)                          AS total_assists,
    SUM(f.goal_involvement)                 AS goal_involvement,
    ROUND(SUM(f.expected_goals_xg), 2)      AS total_xg,
    ROUND(SUM(f.goals) - SUM(f.expected_goals_xg), 2) AS xg_overperformance,
    SUM(f.shots)                            AS total_shots,
    ROUND(AVG(f.shot_efficiency), 3)        AS avg_shot_efficiency,
    COUNT(DISTINCT f.match_id)              AS matches_played,
    ROUND(AVG(f.player_rating), 2)          AS avg_rating
FROM fact_performance f
JOIN dim_players p ON f.player_id = p.player_id
GROUP BY p.player_name, p.team, p.position, p.age, p.market_value_tier
ORDER BY total_goals DESC, goal_involvement DESC
LIMIT 20;

-- 2. Best scorers in knockout rounds only
SELECT
    p.player_name,
    p.team,
    SUM(f.goals)                            AS knockout_goals,
    ROUND(AVG(f.clutch_performance_score), 2) AS avg_clutch_score,
    ROUND(AVG(f.pressure_resistance), 2)    AS avg_pressure_resistance
FROM fact_performance f
JOIN dim_players p ON f.player_id = p.player_id
WHERE f.is_knockout = 1
GROUP BY p.player_name, p.team
HAVING SUM(f.goals) > 0
ORDER BY knockout_goals DESC, avg_clutch_score DESC
LIMIT 15;