import pandas as pd
from gurobipy import GRB, Model

# Read data
data_raw = pd.read_csv("winequality-red.csv", delimiter=";")

# Preprocessing
# Drop duplicates
df = data_raw.drop_duplicates().reset_index(drop=True)
# Scale values
data = (df - df.mean()) / df.std()

# Data points
X = data[[d for d in data.columns if d != "quality"]]
N = len(X)
features = list(X.columns)
# Labels
y = data["quality"]

# Tuning parameter
l = 0.1

# Model declaration
m = Model("Linear Regression nD")

# Decision variables
intercept = m.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS)
beta = m.addVars(features, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS)

# Objective function
m.setObjective(
    1/N *
    sum(
        (intercept+sum(beta[j]*X.loc[i, j] for j in features) - y[i])**2
        + l*sum(beta[i]**2 for i in features)
        for i in range(N)
    )
)

# Solve statement
m.optimize()

for name in beta:
    print(f"{name}: {beta[name].X:.3f}")
