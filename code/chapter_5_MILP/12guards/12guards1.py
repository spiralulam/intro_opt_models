from mip import INTEGER, Model, xsum

# Platforms
platforms = range(1, 13)

# Model declaration
m = Model("12 Guards")

# Decision variables
x = {p: m.add_var(var_type=INTEGER, lb=0) for p in platforms}

# Constraints
m += xsum(x[p] for p in platforms) == 12
m += x[1] + x[2] + x[3] + x[4] >= 5
m += x[1] + x[5] + x[7] + x[9] >= 5
m += x[9] + x[10] + x[11] + x[12] >= 5
m += x[4] + x[6] + x[8] + x[12] >= 5

# Optimize statement
m.optimize()

# Result inspection
for p in platforms:
    print(f"Platform {p}: {int(x[p].x)} guards")
