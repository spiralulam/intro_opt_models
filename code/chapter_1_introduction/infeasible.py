from mip import BINARY, CBC, Model, xsum

I = [1, 2, 3, 4]

# Model declaration
m = Model(solver_name=CBC)

# Decision variables
y = {i: m.add_var(var_type=BINARY) for i in I}

# Constraints
m += xsum(y[i] for i in I) == 1
m += y[2] == 1
m += y[4] == 1

# Solve optimization model
m.optimize()
