-- create_dimensions.sql
-- Dimension tables for the star-schema data warehouse.

CREATE TABLE IF NOT EXISTS dim_players (
    player_id                       VARCHAR PRIMARY KEY,
    player_name                     VARCHAR,
    age                             DOUBLE,
    age_group                       VARCHAR,
    nationality                     VARCHAR,
    team                            VARCHAR,
    jersey_number                   DOUBLE,
    position                        VARCHAR,
    height_cm                       DOUBLE,
    weight_kg                       DOUBLE,
    preferred_foot                  VARCHAR,
    club_name                       VARCHAR,
    market_value_eur                DOUBLE,
    market_value_tier               VARCHAR,
    total_goals_tournament          DOUBLE,
    total_assists_tournament        DOUBLE,
    total_minutes_tournament        DOUBLE,
    player_of_match_awards          DOUBLE,
    tournament_rating               DOUBLE,
    goal_involvement_tournament     DOUBLE,
    bmi                             DOUBLE
);

CREATE TABLE IF NOT EXISTS dim_matches (
    match_id                        VARCHAR PRIMARY KEY,
    match_date                      DATE,
    stadium                         VARCHAR,
    city                            VARCHAR,
    tournament_stage                VARCHAR,
    stage_order                     INTEGER,
    match_month                     INTEGER,
    match_dow                       VARCHAR,
    is_knockout                     INTEGER,
    total_goals_in_match            DOUBLE,
    total_shots                     DOUBLE,
    total_cards                     DOUBLE,
    avg_player_rating               DOUBLE,
    avg_distance_covered            DOUBLE,
    players_in_match                INTEGER
);

CREATE TABLE IF NOT EXISTS dim_teams (
    team                            VARCHAR PRIMARY KEY,
    nationality                     VARCHAR,
    squad_size                      INTEGER,
    avg_age                         DOUBLE,
    avg_height_cm                   DOUBLE,
    avg_weight_kg                   DOUBLE,
    avg_market_value_eur            DOUBLE,
    total_market_value_eur          DOUBLE,
    matches_played                  INTEGER,
    total_goals                     DOUBLE,
    total_assists                   DOUBLE,
    total_shots                     DOUBLE,
    avg_pass_accuracy               DOUBLE,
    total_yellow_cards              DOUBLE,
    total_red_cards                 DOUBLE,
    avg_player_rating               DOUBLE,
    avg_performance_score           DOUBLE,
    avg_distance_covered            DOUBLE,
    avg_top_speed                   DOUBLE,
    wins                            INTEGER,
    draws                           INTEGER,
    losses                          INTEGER,
    win_rate                        DOUBLE,
    goals_per_match                 DOUBLE
);

CREATE TABLE IF NOT EXISTS dim_stadiums (
    stadium                         VARCHAR,
    city                            VARCHAR,
    matches_hosted                  INTEGER,
    total_goals_scored              DOUBLE,
    avg_player_rating               DOUBLE,
    avg_top_speed                   DOUBLE,
    avg_distance_covered            DOUBLE,
    total_yellow_cards              DOUBLE,
    total_red_cards                 DOUBLE,
    unique_teams                    INTEGER,
    goals_per_match                 DOUBLE,
    PRIMARY KEY (stadium, city)
);
