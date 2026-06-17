# Data Dictionary

## Source: `fifa_wc2026_player_performance.csv`
54 600 rows · 75 columns | Grain: one row per player × match

---

### Player Profile

| Column | Type | Description |
|---|---|---|
| `player_id` | str | Unique player identifier |
| `player_name` | str | Full name |
| `age` | int | Age at tournament time |
| `nationality` | str | Country of origin |
| `team` | str | National team represented |
| `jersey_number` | int | Shirt number |
| `position` | str | Goalkeeper / Defender / Midfielder / Forward |
| `height_cm` | float | Height in centimetres |
| `weight_kg` | float | Weight in kilograms |
| `preferred_foot` | str | Left / Right |
| `club_name` | str | Club team at time of tournament |
| `market_value_eur` | float | Transfer market value in EUR |

### Match Context

| Column | Type | Description |
|---|---|---|
| `match_id` | str | Unique match identifier |
| `match_date` | date | Date of the match |
| `stadium` | str | Venue name |
| `city` | str | Host city |
| `opponent_team` | str | Name of the opposing team |
| `tournament_stage` | str | Group Stage / Round of 32 / R16 / QF / SF / 3rd / Final |
| `match_result` | str | W / D / L (from team's perspective) |
| `goals_team` | int | Goals scored by the player's team |
| `goals_opponent` | int | Goals scored by the opponent |
| `minutes_played` | int | Minutes on the pitch (0–120) |

### Attacking Stats

| Column | Type | Description |
|---|---|---|
| `goals` | int | Goals scored |
| `assists` | int | Goal assists |
| `shots` | int | Total shots |
| `shots_on_target` | int | Shots on target |
| `expected_goals_xg` | float | Expected goals (model-derived) |
| `expected_assists_xa` | float | Expected assists |
| `key_passes` | int | Passes leading to a shot |

### Passing

| Column | Type | Description |
|---|---|---|
| `total_passes` | int | Passes attempted |
| `successful_passes` | int | Passes completed |
| `pass_accuracy` | float | Completion rate (0–1) |
| `crosses` | int | Crosses attempted |
| `successful_crosses` | int | Crosses completed |
| `dribbles_attempted` | int | Dribbles attempted |
| `successful_dribbles` | int | Dribbles completed |

### Defensive Stats

| Column | Type | Description |
|---|---|---|
| `tackles` | int | Tackles made |
| `interceptions` | int | Interceptions |
| `clearances` | int | Clearances |
| `blocks` | int | Blocks |
| `aerial_duels_won` | int | Aerial duels won |
| `aerial_duels_lost` | int | Aerial duels lost |
| `recoveries` | int | Ball recoveries |
| `defensive_actions` | int | Total defensive actions |

### Discipline

| Column | Type | Description |
|---|---|---|
| `yellow_cards` | int | Yellow cards received |
| `red_cards` | int | Red cards received |
| `fouls_committed` | int | Fouls given away |
| `fouls_suffered` | int | Fouls won |
| `offsides` | int | Offside traps caught |

### Goalkeeper

| Column | Type | Description |
|---|---|---|
| `saves` | int | Saves made |
| `save_percentage` | float | Save % (0–1) |
| `punches` | int | Punch clearances |
| `clean_sheet` | int | 1 if clean sheet, 0 otherwise |
| `goals_conceded` | int | Goals let in |
| `penalty_saves` | int | Penalty kicks saved |

### Physical

| Column | Type | Description |
|---|---|---|
| `distance_covered_km` | float | Total km covered |
| `sprint_distance_km` | float | Km covered at sprint pace |
| `top_speed_kmh` | float | Maximum speed recorded |
| `accelerations` | int | Number of accelerations |
| `decelerations` | int | Number of decelerations |
| `stamina_score` | float | Stamina index (0–100) |

### Composite Scores

| Column | Type | Range | Description |
|---|---|---|---|
| `player_rating` | float | 0–10 | Overall match rating |
| `performance_score` | float | 0–100 | Composite performance index |
| `offensive_contribution` | float | 0–100 | Attacking impact score |
| `defensive_contribution` | float | 0–100 | Defensive impact score |
| `possession_impact` | float | 0–100 | Influence when in possession |
| `pressure_resistance` | float | 0–100 | Performance under pressure |
| `creativity_score` | float | 0–100 | Creative play index |
| `consistency_score` | float | 0–100 | Consistency across the match |
| `clutch_performance_score` | float | 0–100 | Performance in key moments |

### Tournament Totals (player-level, repeated across match rows)

| Column | Type | Description |
|---|---|---|
| `total_goals_tournament` | int | Total goals in full tournament |
| `total_assists_tournament` | int | Total assists in full tournament |
| `total_minutes_tournament` | int | Total minutes played in tournament |
| `player_of_match_awards` | int | Number of PoM awards |
| `tournament_rating` | float | Overall tournament rating (0–10) |

---

### Engineered Columns (added in `clean_transform.py`)

| Column | Formula | Description |
|---|---|---|
| `stage_order` | map | 1=Group … 7=Final |
| `match_month` | date extract | Month number |
| `match_dow` | date extract | Day of week |
| `age_group` | cut | U21 / 21-24 / 25-28 / 29-32 / 33+ |
| `market_value_tier` | cut | <€5M / €5-20M / €20-60M / €60-150M / €150M+ |
| `rating_tier` | cut | Poor / Below Avg / Good / Excellent / World Class |
| `shot_efficiency` | goals/shots | Conversion rate per match |
| `pass_completion_pct` | pass_accuracy×100 | Pass % (0–100) |
| `dribble_success_pct` | successful/attempted×100 | Dribble success % |
| `goal_involvement` | goals+assists | Direct goal contributions |
| `defensive_index` | weighted sum | tackles×1.5 + interceptions×1.5 + clearances + blocks×1.2 + recoveries×0.8 |
| `is_knockout` | stage_order≥2 | 1 = KO stage match |
| `goal_diff` | goals_team − goals_opponent | Match goal difference |
| `km_per_minute` | distance/minutes | Distance efficiency |
| `full_starter` | minutes≥90 | 1 = full game played |
| `bmi` | weight/(height/100)² | Body Mass Index (dim_players only) |
| `goal_involvement_tournament` | total_goals + total_assists | Career total (dim_players only) |