from gurobipy import GRB, Model, quicksum
import numpy as np

# Generate input data
np.random.seed(73)

N = 20
X1 = 100*np.random.rand(N)
X2 = 100*np.random.rand(N)
X = [tuple(x) for x in zip(X1, X2)]

num_points = range(1, N+1)
axes = [0, 1]

# Optimization model
m = Model('Nuclear waste')
# Set nonconvexity parameter to 2 since the model is not convex
m.Params.NonConvex = 2

x = m.addVars(axes, name='x', lb=0, ub=100)
alpha = m.addVar(name='alpha', lb=-GRB.INFINITY)
v = m.addVars(num_points, axes, name='v', lb=-GRB.INFINITY)

m.addConstrs((v[i, j] == x[j]-X[i-1][j] for i in num_points for j in axes), name='Definition v')
m.addConstrs((
    quicksum(v[i, j]*v[i, j] for j in axes) >= alpha*alpha for i in num_points
), name='Distance to cities')
m.setObjective(alpha, sense=GRB.MAXIMIZE)

m.optimize()
