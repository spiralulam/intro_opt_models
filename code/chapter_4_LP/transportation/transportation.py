import pandas as pd
from mip import Model, minimize, xsum

# Data
df = pd.read_csv("data.csv", index_col=0)
cost = df.loc[
    [r for r in df.index if r != "Demand"],
    [c for c in df.columns if c != "Capacity"],
].to_dict()
demand = df.loc[
    "Demand", [c for c in df.columns if c != "Capacity"]
].to_dict()
capacity = df.loc[
    [r for r in df.index if r != "Demand"], "Capacity"
].to_dict()
customers = list(demand.keys())
warehouses = list(capacity.keys())

# Model declaration
m = Model("Transportation")
# Decision variables
x = {(w, c): m.add_var() for w in warehouses for c in customers}
# Constraints
for w in warehouses:
    m += xsum(x[w, c] for c in customers) <= capacity[w]
for c in customers:
    m += xsum(x[w, c] for w in warehouses) >= demand[c]
# Objective
m.objective = minimize(xsum(cost[c][w] * x[w, c] for (w, c) in x))

# Optimize and write results
m.optimize()
for (w, c) in x:
    print(f"Warehouse: {w}, Customer: {c}, Amount: {x[w, c].x}")
