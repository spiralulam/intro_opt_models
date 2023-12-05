import pandas as pd
from mip import Model, minimize, xsum

# Data
costs = {
    "chicken": 0.013,
    "beef": 0.008,
    "mutton": 0.01,
    "rice": 0.002,
    "wheat bran": 0.005,
    "gel": 0.001,
}
lower_bounds = {"protein": 8, "fat": 6}
upper_bounds = {"fibers": 2, "salt": 0.4}
ingred_contrib = pd.read_csv("ingredient_contribution.csv", index_col=0)
ingreds = list(costs.keys())

# Model declaration
m = Model("Whiskas")

# Decision variables
x = {i: m.add_var(lb=0) for i in ingreds}

# Constraints
# Ingredients sum up to 100g
m += xsum(x[i] for i in ingreds) == 100
# Recipe fulfills lower and upper bounds
for c in lower_bounds:
    m += (
        xsum(ingred_contrib.loc[i, c] * x[i] for i in ingreds)
        >= lower_bounds[c]
    )
for c in upper_bounds:
    m += (
        xsum(ingred_contrib.loc[i, c] * x[i] for i in ingreds)
        <= upper_bounds[c]
    )

# Objective function
m.objective = minimize(xsum(costs[i] * x[i] for i in ingreds))

# Solve statement
m.optimize()

for name in x:
    print(f"{name}: {x[name].x:.3f}")
