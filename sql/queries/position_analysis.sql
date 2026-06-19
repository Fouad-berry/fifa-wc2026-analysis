-- position_analysis.sql
-- Statistical profile per playing position.

-- 1. Average stats by position
SELECT
    f.position,
    COUNT(DISTINCT f.player_id)             AS unique_players,
    ROUND(AVG(f.player_rating), 2)          AS avg_rating,
    ROUND(AVG(f.goals), 3)                  AS avg_goals,
    ROUND(AVG(f.assists), 3)                AS avg_assists,
    ROUND(AVG(f.key_passes), 2)             AS avg_key_passes,
    ROUND(AVG(f.pass_completion_pct), 1)    AS avg_pass_completion,
    ROUND(AVG(f.distance_covered_km), 2)    AS avg_distance_km,
    ROUND(AVG(f.top_speed_kmh), 2)          AS avg_top_speed,
    ROUND(AVG(f.defensive_index), 2)        AS avg_defensive_index,
    ROUND(AVG(f.offensive_contribution), 2) AS avg_offensive,
    ROUND(AVG(f.defensive_contribution), 2) AS avg_defensive,
    ROUND(AVG(f.creativity_score), 2)       AS avg_creativity,
    ROUND(AVG(f.stamina_score), 1)          AS avg_stamina
FROM fact_performance f
JOIN dim_players p ON f.player_id = p.player_id
GROUP BY f.position
ORDER BY avg_rating DESC;

-- 2. Best player per position by avg rating
SELECT position, player_name, team, avg_rating, goals, assists
FROM (
    SELECT
        p.position,
        p.player_name,
        p.team,
        ROUND(AVG(f.player_rating), 2)      AS avg_rating,
        SUM(f.goals)                        AS goals,
        SUM(f.assists)                      AS assists,
        ROW_NUMBER() OVER (
            PARTITION BY p.position
            ORDER BY AVG(f.player_rating) DESC
        )                                   AS rn
    FROM fact_performance f
    JOIN dim_players p ON f.player_id = p.player_id
    GROUP BY p.position, p.player_name, p.team
    HAVING COUNT(DISTINCT f.match_id) >= 3
)
WHERE rn = 1
ORDER BY position;