from mip import CBC, Model

# Model declaration
m = Model(solver_name=CBC)

# Decision variables
y = m.add_var()

# Constraints
m += y > 1

# Solve optimization model
m.optimize()
