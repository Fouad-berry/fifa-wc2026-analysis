-- create_dimensions.sql
-- Dimension tables for the star-schema data warehouse.

CREATE TABLE IF NOT EXISTS dim_players (
    player_id                       VARCHAR PRIMARY KEY,
    player_name                     VARCHAR,
    age                             DOUBLE,
    age_group                       VARCHAR,
    nationality                     VARCHAR,
    team                            VARCHAR,
    jersey_number                   INTEGER,
    position                        VARCHAR,
    height_cm                       DOUBLE,
    weight_kg                       DOUBLE,
    preferred_foot                  VARCHAR,
    club_name                       VARCHAR,
    market_value_eur                DOUBLE,
    market_value_tier               VARCHAR,
    total_goals_tournament          INTEGER,
    total_assists_tournament        INTEGER,
    total_minutes_tournament        INTEGER,
    player_of_match_awards          INTEGER,
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
    total_goals_in_match            INTEGER,
    total_shots                     INTEGER,
    total_cards                     INTEGER,
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
    total_goals                     INTEGER,
    total_assists                   INTEGER,
    total_shots                     INTEGER,
    avg_pass_accuracy               DOUBLE,
    total_yellow_cards              INTEGER,
    total_red_cards                 INTEGER,
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
    total_goals_scored              INTEGER,
    avg_player_rating               DOUBLE,
    avg_top_speed                   DOUBLE,
    avg_distance_covered            DOUBLE,
    total_yellow_cards              INTEGER,
    total_red_cards                 INTEGER,
    unique_teams                    INTEGER,
    goals_per_match                 DOUBLE,
    PRIMARY KEY (stadium, city)
);
