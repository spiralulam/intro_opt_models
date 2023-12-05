import pandas as pd
from mip import Model, minimize, xsum

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

# Model declaration
m = Model("LAD nD")

# Decision variables
intercept = m.add_var(lb=-float("inf"))
beta = {f: m.add_var(lb=-float("inf")) for f in features}
z = {i: m.add_var() for i in range(N)}

# Constraints
for i in range(N):
    m += (
        intercept + xsum(beta[j] * X.loc[i, j] for j in features) - y[i]
        <= z[i]
    )
    m += (
        -(
            intercept
            + xsum(beta[j] * X.loc[i, j] for j in features)
            - y[i]
        )
        <= z[i]
    )

# Objective function
m.objective = minimize(1 / N * xsum(z[i] for i in range(N)))

# Solve statement
m.optimize()

for name in beta:
    print(f"{name}: {beta[name].x:.3f}")
