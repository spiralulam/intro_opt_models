from mip import CBC, INTEGER, Model, maximize, xsum

# Data from problem description

# Coin types
T = ["2-Cent", "5-Cent", "20-Cent", "50-Cent", "2-Euro"]
# Content of the wallet
cont = {
    "2-Cent": 20,
    "5-Cent": 3,
    "20-Cent": 10,
    "50-Cent": 1,
    "2-Euro": 5,
}
# Coin value in cents
val = {
    "2-Cent": 2,
    "5-Cent": 5,
    "20-Cent": 20,
    "50-Cent": 50,
    "2-Euro": 200,
}
# Total price in cents
price = 777

# Optimization model

# Model declaration
m = Model(solver_name=CBC)

# Decision variables
coins = {t: m.add_var(var_type=INTEGER, lb=0) for t in T}

# Constraints
# x must not exceed the wallet's content
for t in T:
    m += coins[t] <= cont[t]
# The total amount of coins meets the prices
m += xsum(coins[t] * val[t] for t in T) == price

# Objective function
m.objective = maximize(xsum(coins[t] for t in T))

# Solve optimization model
m.optimize()

# Inspect results
print(f"Total number of coins: {int(m.objective_value)}")

for k in coins:
    if coins[k].x > 0:
        print(f"{k}: {int(coins[k].x)}")
