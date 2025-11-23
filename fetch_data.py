from pybaseball import statcast
import pandas as pd

# Selecting full season
data = statcast(start_dt="2025-03-20", end_dt="2025-11-01")

# keep only home runs
hr = data[data["events"] == "home_run"].copy()

# group by player_name and compute leaders
leaders = (
    hr.groupby("player_name")
      .agg(
          hr_count=("events", "size"),
          avg_hr_distance=("hit_distance_sc", "mean"),
          max_hr_distance=("hit_distance_sc", "max"),

          # launch speed (exit velocity) metrics
          avg_launch_speed=("launch_speed", "mean"),
          max_launch_speed=("launch_speed", "max"),
      )
)

# filter to players with >= 5 home runs
leaders = leaders[leaders["hr_count"] >= 5]

# sort after filtering
leaders = leaders.sort_values("avg_hr_distance", ascending=False)

#Rounding values
leaders["avg_hr_distance"] = leaders["avg_hr_distance"].round(1)
leaders["max_hr_distance"] = leaders["max_hr_distance"].round(1)

leaders.to_csv("./data/hr_distance_leaders_2024.csv", index=True)

hr_leaders = pd.read_csv("./data/hr_distance_leaders_2024.csv")
barrel_leaders = pd.read_csv("./data/exit_velocity.csv")

#Combining last name and first name into one column so both datasets match
name_col = "last_name, first_name"
barrel_leaders["player_name"] = (
    barrel_leaders[name_col]
    .str.split(", ")
    .apply(lambda parts: f"{parts[1]} {parts[0]}" if len(parts) == 2 else barrel_leaders[name_col])
)

#Only keeping columns we want to use
savant_barrels = barrel_leaders[["player_name", "barrels", "brl_percent"]].copy()

#Combining datasets on player name
combined = leaders.merge(savant_barrels, on="player_name", how="left")

#Rounding values
combined["brl_percent"] = combined["brl_percent"].round(1)
combined["barrels"] = combined["barrels"].round(1)

combined.to_csv("./data/combined_leaders_2024.csv", index=False)
