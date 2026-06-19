-- team_performance.sql
-- Team attacking, defensive, and disciplinary analysis.

-- 1. Full team performance table
SELECT
    t.team,
    t.matches_played,
    t.wins,
    t.draws,
    t.losses,
    t.win_rate,
    t.total_goals,
    t.goals_per_match,
    t.total_shots,
    ROUND(t.avg_pass_accuracy * 100, 1)     AS pass_accuracy_pct,
    t.total_yellow_cards,
    t.total_red_cards,
    t.avg_player_rating,
    t.avg_performance_score,
    t.avg_distance_covered,
    t.avg_top_speed,
    t.total_market_value_eur
FROM dim_teams t
ORDER BY t.total_goals DESC;

-- 2. Attacking efficiency: goals vs xG
SELECT
    f.team,
    SUM(f.goals)                            AS total_goals,
    ROUND(SUM(f.expected_goals_xg), 2)      AS total_xg,
    ROUND(SUM(f.goals) - SUM(f.expected_goals_xg), 2) AS xg_diff,
    SUM(f.shots)                            AS total_shots,
    SUM(f.shots_on_target)                  AS shots_on_target,
    ROUND(AVG(f.creativity_score), 2)       AS avg_creativity
FROM fact_performance f
GROUP BY f.team
ORDER BY total_goals DESC;

-- 3. Defensive solidity
SELECT
    f.team,
    SUM(f.tackles)                          AS total_tackles,
    SUM(f.interceptions)                    AS total_interceptions,
    SUM(f.clearances)                       AS total_clearances,
    SUM(f.blocks)                           AS total_blocks,
    ROUND(AVG(f.defensive_index), 2)        AS avg_defensive_index,
    ROUND(AVG(f.defensive_contribution), 2) AS avg_def_contribution,
    SUM(f.goals_conceded)                   AS goals_conceded
FROM fact_performance f
GROUP BY f.team
ORDER BY avg_defensive_index DESC;