from gurobipy import GRB, Model
from math import sqrt

# Coefficients hyperplane
a = [1, -1]
# RHS hyperplane
b = 1
# Point to be projected
x_bar = [1, 1]

# Number of dimensions
n = len(a)

# Model declaration
m = Model("Projection line")

# Decision variables
x = m.addVars(range(n), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS)

# Objective function
m.setObjective(
    sum((x[i] - x_bar[i]) ** 2 for i in range(n))
)

# Constraint
m.addConstr(sum(a[i]*x[i] for i in range(n)) == b)

# Solve statement
m.optimize()

# Print results
print(f"Distance from xbar to projection: {sqrt(m.ObjVal)}")
print(f"Coordinates projection: {[x[i].X for i in x]}")
