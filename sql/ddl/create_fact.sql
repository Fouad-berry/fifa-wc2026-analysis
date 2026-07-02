-- create_fact.sql
-- Central fact table — grain: one row per player × match.

CREATE TABLE IF NOT EXISTS fact_performance (
    -- Foreign keys
    player_id               VARCHAR REFERENCES dim_players(player_id),
    match_id                VARCHAR REFERENCES dim_matches(match_id),
    team                    VARCHAR REFERENCES dim_teams(team),

    -- Match context
    tournament_stage        VARCHAR,
    stage_order             INTEGER,
    match_result            VARCHAR,    -- W / D / L
    is_knockout             INTEGER,    -- 0 = group, 1 = KO
    minutes_played          DOUBLE,
    full_starter            INTEGER,    -- 1 if 90+ min

    -- Attacking
    goals                   DOUBLE,
    assists                 DOUBLE,
    shots                   DOUBLE,
    shots_on_target         DOUBLE,
    expected_goals_xg       DOUBLE,
    expected_assists_xa     DOUBLE,
    key_passes              DOUBLE,
    goal_involvement        DOUBLE,
    shot_efficiency         DOUBLE,

    -- Passing
    total_passes            DOUBLE,
    successful_passes       DOUBLE,
    pass_accuracy           DOUBLE,
    pass_completion_pct     DOUBLE,
    crosses                 DOUBLE,
    successful_crosses      DOUBLE,
    dribbles_attempted      DOUBLE,
    successful_dribbles     DOUBLE,
    dribble_success_pct     DOUBLE,

    -- Defensive
    tackles                 DOUBLE,
    interceptions           DOUBLE,
    clearances              DOUBLE,
    blocks                  DOUBLE,
    aerial_duels_won        DOUBLE,
    aerial_duels_lost       DOUBLE,
    recoveries              DOUBLE,
    defensive_actions       DOUBLE,
    defensive_index         DOUBLE,

    -- Discipline
    yellow_cards            DOUBLE,
    red_cards               DOUBLE,
    fouls_committed         DOUBLE,
    fouls_suffered          DOUBLE,
    offsides                DOUBLE,

    -- Goalkeeper
    saves                   DOUBLE,
    save_percentage         DOUBLE,
    clean_sheet             DOUBLE,
    goals_conceded          DOUBLE,
    penalty_saves           DOUBLE,

    -- Physical
    distance_covered_km     DOUBLE,
    sprint_distance_km      DOUBLE,
    top_speed_kmh           DOUBLE,
    accelerations           DOUBLE,
    decelerations           DOUBLE,
    stamina_score           DOUBLE,
    km_per_minute           DOUBLE,

    -- Composite scores
    player_rating           DOUBLE,
    rating_tier             VARCHAR,
    performance_score       DOUBLE,
    offensive_contribution  DOUBLE,
    defensive_contribution  DOUBLE,
    possession_impact       DOUBLE,
    pressure_resistance     DOUBLE,
    creativity_score        DOUBLE,
    consistency_score       DOUBLE,
    clutch_performance_score DOUBLE
);

-- Load from CSV (DuckDB)
-- COPY fact_performance FROM 'data/datamarts/dm_performance/fact_performance.csv' (HEADER TRUE);