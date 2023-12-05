from gurobipy import GRB, Model
import pandas as pd

# Data

# Create pandas dataframes from input data
df = pd.read_csv('edges.csv', header=None,
                 names=['Start', 'Destination', 'Costs'])
df_cap = pd.read_csv('capacities.csv', header=None,
                     names=['Nodes', 'Capacity'])

# Build sets, lists and dictionaries that contain input data for the
# optimization model from these data frames
capacities = {n: cap for (n, cap) in df_cap.values}
edges = set([tuple(x) for x in df[['Start', 'Destination']].values])
costs = {(n, n1): w for (n, n1, w) in df.values}
nodes = set(df['Start'].append(df['Destination']))
nodes_intermed = [n for n in nodes if n[0] == 'T']

# Optimization model

# Model declaration
m = Model('flow')

# Decision variables
x = m.addVars(edges, name='Transport on edge')

# Constraints
# 30 units have to be transported from source to sink
m.addConstr(
    sum(x[n, 'S'] for n in nodes if (n, 'S') in edges) == 30
)
m.addConstr(
    sum(x['Q', n] for n in nodes if ('Q', n) in edges) == 30
)
# Capacity constraints
cap_restr = m.addConstrs(
    sum(x[n1, n] for n1 in nodes if (n1, n) in edges) <= capacities[n]
    for n in nodes_intermed
)
# Flow conservation equation
m.addConstrs(
    sum(
        x[n1, n] for n1 in nodes if (n1, n) in edges) ==
    sum(x[n, n2] for n2 in nodes if (n, n2) in edges)
    for n in nodes_intermed
)

# Objective function
m.setObjective(
    sum(costs[e] * x[e] for e in edges), sense=GRB.MINIMIZE
)

# Solve optimization model
m.optimize()

# Print results
print(f"Total transportation costs: {m.ObjVal}")
for e in x:
    if x[e].X > 0.1:
        print(f"Edge: {e}, Transported units: {x[e].X}")
