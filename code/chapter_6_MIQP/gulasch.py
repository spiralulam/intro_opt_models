import numpy as np
from gurobipy import GRB, Model

circles = range(2)

m = Model("Gulasch")

m.Params.NonConvex = 2

a = m.addVar(ub=1)
b = m.addVar(ub=1)
x = m.addVars(circles, ub=1)
y = m.addVars(circles, ub=1)
r = m.addVar(ub=0.5)
z = m.addVars(circles, vtype=GRB.BINARY)
s = m.addVar()

m.addConstrs(r <= y[i] for i in circles)
m.addConstrs(y[i] <= 1 - r for i in circles)
m.addConstrs(r <= x[i] for i in circles)
m.addConstrs(x[i] <= 1 - r for i in circles)
m.addConstr((x[0] - x[1]) ** 2 + (y[0] - y[1]) ** 2 >= r**2)
m.addConstrs(a + r <= y[i] + (1 - z[i]) * 1.5 for i in circles)
m.addConstrs(b + r <= x[i] + z[i] * 1.5 for i in circles)
m.addConstr(b == 2 * np.pi * r)
m.addConstr(s == r**2)

m.setObjective(np.pi * s * a, sense=GRB.MAXIMIZE)

m.optimize()
