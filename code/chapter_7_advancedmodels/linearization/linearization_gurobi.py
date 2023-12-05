import numpy as np
from gurobipy import Model


# Nonlinear function
def f(x):
    return np.sqrt(x) + np.sin(x) + 10 * np.exp(-x)


# Supporting points
x_sup = range(2, 21, 2)
y_sup = [f(t) for t in x_sup]
intervals = range(len(x_sup) - 1)
# Lower and upper bounds on x
lb_x = 2
ub_x = 20

# Optimization model

# Model declaration
m = Model("Linearization comfort version")

# Decision variables
x = m.addVar(lb=lb_x, ub=ub_x)

# Piecewise-linear objective
m.setPWLObj(x, x_sup, y_sup)

# Solve statement
m.optimize()
