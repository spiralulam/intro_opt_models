from gurobipy import GRB, Model, quicksum
import matplotlib.pyplot as plt
import random

# Create data

# Number warehouses
num_w = 3
# Number customers
num_c = 10
# Central warehouses (1. Layer)
W = [f'W{i}' for i in range(num_w)]
# Regional warehouses (2. Layer)
R = [f'R{i}' for i in range(2*num_w)]
# Customers (3. Layer)
C = [f'C{i}' for i in range(num_c)]

# Create edges in transport network (which you can use for
# instance in a network package like networkx, if you like to

# from central to regional warehouse
edges_wr = [(w, r) for w in W for r in R]
# from regional warehouse to customer
edges_rc = [(r, c) for r in R for c in C]

edges = edges_wr + edges_rc

# from central to regional warehouse
for w in W:
    for r in R:
        edges.append((w, r))

# from regional warehouse to customer
for r in R:
    for c in C:
        edges.append((r, c))
# Generate random, but reproducible demand and cost data
random.seed(73)
dem = {c: random.randint(50, 100) for c in C}
cost = {e: random.randint(1, 10) for e in edges}
dem_tot = sum(dem.values())
# Distribute total demand equally among all cetral warehouses
sup = {w: int((dem_tot + (3-dem_tot % 3))/3) for w in W}

# Optimization model

# Model declaration
m = Model()

# Decision variables
twr = m.addVars(W, R)
trc = m.addVars(R, C)
y = m.addVars(R, vtype=GRB.BINARY)

# Constraints
# Satisfy demand
m.addConstrs(dem[c] == quicksum(trc[r, c] for r in R) for c in C)
# Respect supply
m.addConstrs(sup[w] >= quicksum(twr[w, r] for r in R) for w in W)
# Flow equation
m.addConstrs(quicksum(twr[w, r] for w in W) == quicksum(trc[r, c] for c in C)
             for r in R)
# Big M
M = sum(dem.values())
m.addConstrs(quicksum(twr[w, r] for w in W) <= M*y[r] for r in R)

# First objective: Minimize total transportation costs
t_cost_total = m.addVar()
m.addConstr(
    t_cost_total ==
    quicksum(cost[w, r] * twr[w, r] for w in W for r in R) +
    quicksum(cost[r, c] * trc[r, c] for r in R for c in C)
)

# Second objective: Minimize total number of used regional warehouses
y_total = m.addVar()
m.addConstr(y_total == quicksum(y[r] for r in R))

# First, minimize only the first objective
m.setObjective(t_cost_total, sense=GRB.MINIMIZE)

# Run optimization
m.optimize()

# Solve
results = []

for i in range(len(R), 0, -1):
    m.addConstr(y_total <= i)
    m.optimize()
    results.append((y_total.X, m.ObjVal))

# Plot results
plt.scatter([e[0] for e in results], [e[1] for e in results])
plt.xlabel("Anzahl Regionallager")
plt.ylabel("Transportkosten")
plt.savefig("multiobj_example_solutions.pdf")
plt.show()
