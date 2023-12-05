from gurobipy import GRB, Model, quicksum
import numpy as np

# Generate input data
np.random.seed(19680801)
N = 100
X1 = 100*np.random.rand(N)
X2 = 100*np.random.rand(N)
X = [tuple(x) for x in zip(X1, X2)]
num_points = range(1, N+1)
axes = [0, 1]

# Optimization model
m = Model('Fermat-Weber constrained')

x = m.addVars(axes, name='x')
w = m.addVars(num_points, name='w')
v = m.addVars(num_points, axes, name='v', lb=-GRB.INFINITY)
# Respect feasible construction region
m.addConstr(((x[0]-30)*(x[0]-30)+(x[1]-40)*(x[1]-40) <= 49))
# Definition v
m.addConstrs((v[i, j] == x[j]-X[i-1][j] for i in num_points for j in axes))
# SOC: Distance to regional warehouse
m.addConstrs((
    quicksum(v[i, j]*v[i, j] for j in axes) <= w[i]*w[i] for i in num_points
))
# Objective
m.setObjective(w.sum(), sense=GRB.MINIMIZE)

# Solve statement
m.optimize()
