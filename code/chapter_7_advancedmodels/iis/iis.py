from gurobipy import GRB, Model

# Model declaration
m = Model("IIS")

# Decision variable
x = m.addVars(range(2), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="x")

# Constraints
m.addConstr(x[0] >= 1, name="lower bound 1")
m.addConstr(x[1] >= 2, name="lower bound 2")
m.addConstr(x[0]+x[1] <= 2.5)
m.addConstr(x[0] <= -1, name="upper bound -1")

# Solve statement
m.optimize()

# m.Status == 4 indicates that the model is infeasible or unbounded.
if m.Status == 4:
    # Set DualReductions to zero, so the solver can determine if the model is infeasible or unbounded.
    m.Params.DualReductions = 0
    # reset all information from previous model runs
    m.reset()
    # reoptimize
    m.optimize()

# m.Status == 3 indicates that the model is infeasible.
if m.Status == 3:
    # Compute an IIS
    m.computeIIS()
    # Write IIS
    m.write("IIS.ilp")
