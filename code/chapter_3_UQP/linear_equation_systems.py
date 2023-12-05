from gurobipy import GRB, Model
import numpy as np

# Coefficients linear equations system
A = np.array([[1, 1, 1], [1, 0, 1], [2, -1, 0]])
# RHS
b = np.array([2, 4, 4])
# Dimension
m = A.shape[0]
n = A.shape[1]

# Model declaration
model = Model("Linear equations system")

# Decision variables
x = model.addVars(range(n), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS)

# Objective function
model.setObjective(
    sum(
        (sum(A[i, j]*x[j] for j in x) - b[i]) *
        (sum(A[i, j]*x[j] for j in x) - b[i])
        for i in range(m)
    )
)

# Solve statement
model.optimize()

# Print results
print(f"Solution: {[x[i].X for i in x]}")
