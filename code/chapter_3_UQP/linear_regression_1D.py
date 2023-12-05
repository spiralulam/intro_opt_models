import numpy as np
from gurobipy import GRB, Model, xsum

# Raw data
data_raw = [
    (1.35, 8.1), (465, 423), (36.33, 119.5), (27.66, 115), (1.04, 5.5),
    (11700, 50), (2547, 4603), (187.1, 419), (521, 655), (10, 115),
    (3.3, 25.6), (529, 680), (207, 406), (62, 1320), (6654, 5712),
    (9400, 70), (6.8, 179), (35, 56), (0.12, 1), (0.023, 0.4),
    (2.5, 12.1), (55.5, 175), (100, 157), (52.16, 440), (0.28, 1.9),
    (87000, 154.5), (0.122, 3), (192, 180),(3.385, 44.5), (0.48, 15.5),
    (14.83, 98.2), (4.19, 58), (0.425, 6.4), (0.101, 4), (0.92, 5.7),
    (1, 6.6), (0.005, 0.14), (0.06, 1), (3.5, 10.8), (2, 12.3),
    (1.7, 6.3), (0.023, 0.3), (0.785, 3.5), (0.2, 5), (1.41, 17.5),
    (85, 325), (0.75, 12.3), (3.5, 3.9), (4.05, 17), (0.01, 0.25),
    (1.4, 12.5), (250, 490), (10.55, 179.5), (0.55, 2.4), (60, 81),
    (3.6, 21), (4.288, 39.2), (0.075, 1.2), (0.048, 0.33), (3, 25),
    (160, 169), (0.9, 2.6), (1.62, 11.4), (0.104, 2.5), (4.235, 50.4),
]
# Remove outliers
data = [d for d in data_raw if d[0] < 2000 and d[1] < 1000]

# Data points
x = [np.log(d[0]) for d in data]
N = len(x)
# Labels
y = [np.log(d[1]) for d in data]

# Model declaration
m = Model("Linear Regression 1D")

# Decision variables
intercept = m.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS)
slope = m.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS)

# Objective function
m.setObjective(
    1/N * xsum((intercept + slope * x[i] - y[i]) ** 2 for i in range(N))
)

# Solve statement
m.optimize()

# Print results
print(f"Optimal intercept: {intercept.X}")
print(f"Optimal slope: {slope.X}")
