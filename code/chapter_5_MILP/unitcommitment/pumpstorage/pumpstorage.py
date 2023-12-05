import pandas as pd
from mip import BINARY, Model, maximize, xsum

# Data
# Read hourly spot prices for electricity
df = pd.read_csv("elspot-prices_2021_hourly_eur.csv")
prices = [
    float(str(x).replace(",", "."))
    for x in df["DE-LU"]
    if not pd.isna(x)
]
hours = range(len(prices))
hours_with_inital_val = range(-1, len(prices))
# Technical specs
pump_max = 70
turb_max = 90
effic = 0.75
storage_capacity = 630
storage_lower_bound = 100
storage_level_init = 300
storage_level_final = 300

# Optimization model

# Model declaration
m = Model("Pump storage")

# Decision variables
pump = {h: m.add_var(var_type=BINARY) for h in hours}
turb = {h: m.add_var() for h in hours}
storage_level = {
    h: m.add_var(lb=storage_lower_bound, ub=storage_capacity)
    for h in hours_with_inital_val
}

# Constraints
# Initial and final storage level
m += storage_level[-1] == storage_level_init
m += storage_level[hours[-1]] == storage_level_final
# Flow conservation
for t in hours:
    m += (
        storage_level[t]
        == storage_level[t - 1] + pump_max * effic * pump[t] - turb[t]
    )
# Turbine and pump cannot run at the same time
for t in hours:
    m += turb[t] <= (1 - pump[t]) * turb_max

# Objective
m.objective = maximize(
    xsum((turb[t] - pump_max * pump[t]) * prices[t] for t in hours)
)

# Solve statement
m.optimize()

# Result validation
# Storage levels
storage_level_res = [storage_level[t].x for t in hours_with_inital_val]
assert min(storage_level_res) >= storage_lower_bound
assert max(storage_level_res) <= storage_capacity

# "Pump hours" are cheaper than "turbine hours"
pump_prices = [prices[t] for t in hours if pump[t].x > 0.1]
turb_prices = [prices[t] for t in hours if turb[t].x > 0.1]
assert sum(pump_prices) / len(pump_prices) <= sum(turb_prices) / len(
    turb_prices
)
