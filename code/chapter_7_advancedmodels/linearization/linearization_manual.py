import numpy as np
from mip import BINARY, Model, minimize, xsum


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
m = Model("Linearization")

# Decision variables
x = m.add_var(lb=lb_x, ub=ub_x)
y = m.add_var(lb=-float("inf"))
z = {i: m.add_var(var_type=BINARY) for i in intervals}
s = {i: m.add_var(lb=0, ub=1) for i in intervals}

# Constraints
m += xsum(z[i] for i in z) == 1
for i in intervals:
    m += s[i] <= z[i]
m += x == xsum(
    z[i] * x_sup[i] + s[i] * (x_sup[i + 1] - x_sup[i]) for i in intervals
)
m += y == xsum(
    z[i] * y_sup[i] + s[i] * (y_sup[i + 1] - y_sup[i]) for i in intervals
)

# Objective
m.objective = minimize(y)

# Solve statement
m.optimize()
